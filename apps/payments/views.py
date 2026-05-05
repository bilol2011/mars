from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Payment, PaymentPlan, InstallmentPayment
from apps.courses.models import Course, Enrollment
from .services import PaymentService


@login_required
def payment_view(request, course_slug):
    """
    Payment page for a course
    """
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    
    # Check if already enrolled
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, 'Siz allaqachon bu kursga yozilgansiz.')
        return redirect('courses:detail', slug=course.slug)
    
    payment_plans = PaymentPlan.objects.filter(course=course, is_active=True)
    
    context = {
        'course': course,
        'payment_plans': payment_plans,
    }
    return render(request, 'payments/payment.html', context)


@login_required
def process_payment_view(request, course_slug):
    """
    Process payment with Payme/Click integration
    """
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        months = request.POST.get('months')
        
        # Calculate amount
        amount = course.get_discounted_price()
        if months and months != '0':
            payment_plan = PaymentPlan.objects.filter(course=course, months=int(months)).first()
            if payment_plan:
                amount = payment_plan.get_total_amount()
        
        # Create pending payment record
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=amount,
            status='pending',
            payment_method=payment_method,
            transaction_id=f'TRX-{int(timezone.now().timestamp())}',
        )
        
        # If Payme or Click, redirect to payment gateway
        if payment_method in ['payme', 'click']:
            payment_service = PaymentService()
            order_id = f"ORDER-{payment.id}"
            description = f"Kurs: {course.title}"
            return_url = request.build_absolute_uri(f'/payments/success/{payment.id}/')
            
            payment_url = payment_service.create_payment(
                payment_method=payment_method,
                amount=float(amount),
                order_id=order_id,
                description=description,
                return_url=return_url
            )
            
            return redirect(payment_url)
        
        # For wallet payment, process immediately
        elif payment_method == 'wallet':
            from apps.accounts.models import Wallet
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            
            if wallet.balance >= amount:
                wallet.deduct_balance(amount)
                payment.status = 'paid'
                payment.payment_date = timezone.now()
                payment.save()
                
                # Create enrollment
                Enrollment.objects.create(user=request.user, course=course)
                course.students_count += 1
                course.save()
                
                # Handle installment
                if months and months != '0' and payment_plan:
                    payment.payment_plan = payment_plan
                    payment.save()
                    
                    monthly_amount = payment_plan.get_monthly_payment()
                    for i in range(1, payment_plan.months + 1):
                        from datetime import timedelta
                        due_date = timezone.now().date() + timedelta(days=30 * i)
                        
                        InstallmentPayment.objects.create(
                            payment=payment,
                            installment_number=i,
                            amount=monthly_amount,
                            due_date=due_date
                        )
                
                messages.success(request, 'To\'lov muvaffaqiyatli amalga oshirildi!')
                return redirect('dashboard:home')
            else:
                payment.status = 'failed'
                payment.save()
                messages.error(request, 'Hisobda yetarli mablag\' yo\'q!')
                return redirect('payments:payment', course_slug=course_slug)
    
    return redirect('payments:payment', course_slug=course_slug)


@login_required
def payment_success_view(request, payment_id):
    """
    Payment success callback
    """
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    if payment.status == 'pending':
        # Mark as paid (in production, verify with payment gateway)
        payment.status = 'paid'
        payment.payment_date = timezone.now()
        payment.save()
        
        # Create enrollment
        if not Enrollment.objects.filter(user=request.user, course=payment.course).exists():
            Enrollment.objects.create(user=request.user, course=payment.course)
            payment.course.students_count += 1
            payment.course.save()
        
        messages.success(request, 'To\'lov muvaffaqiyatli amalga oshirildi!')
    else:
        messages.info(request, 'To\'lov allaqachon qayta ishlangan.')
    
    return redirect('dashboard:home')


@login_required
def payment_cancel_view(request, payment_id):
    """
    Payment cancel callback
    """
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    if payment.status == 'pending':
        payment.status = 'cancelled'
        payment.save()
        messages.warning(request, 'To\'lov bekor qilindi.')
    
    return redirect('payments:payment', course_slug=payment.course.slug)


@login_required
def payment_history_view(request):
    """
    User payment history
    """
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'payments': payments,
    }
    return render(request, 'payments/payment_history.html', context)


@login_required
def installment_detail_view(request, payment_id):
    """
    Installment payment detail
    """
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    installments = payment.installments.all()
    
    context = {
        'payment': payment,
        'installments': installments,
    }
    return render(request, 'payments/installment_detail.html', context)


@csrf_exempt
def payme_webhook_view(request):
    """
    Payme webhook handler
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Verify the request
            service = PaymentService()
            if not service.payme.verify_webhook(data):
                return JsonResponse({'error': 'Invalid signature'}, status=400)
            
            # Handle different Payme commands
            command = data.get('method')
            
            if command == 'CheckPerformTransaction':
                # Check if transaction can be performed
                return JsonResponse({'result': {'allow': True}})
            
            elif command == 'CreateTransaction':
                # Create transaction
                order_id = data.get('params', {}).get('account', {}).get('order_id')
                payment = Payment.objects.filter(transaction_id=order_id).first()
                if payment:
                    return JsonResponse({'result': {'transaction': str(payment.id), 'state': 1}})
                return JsonResponse({'error': 'Order not found'}, status=404)
            
            elif command == 'PerformTransaction':
                # Complete transaction
                order_id = data.get('params', {}).get('account', {}).get('order_id')
                payment = Payment.objects.filter(transaction_id=order_id).first()
                if payment and payment.status == 'pending':
                    payment.status = 'paid'
                    payment.payment_date = timezone.now()
                    payment.save()
                    
                    # Create enrollment
                    if not Enrollment.objects.filter(user=payment.user, course=payment.course).exists():
                        Enrollment.objects.create(user=payment.user, course=payment.course)
                        payment.course.students_count += 1
                        payment.course.save()
                    
                    return JsonResponse({'result': {'transaction': str(payment.id), 'state': 2}})
                return JsonResponse({'error': 'Transaction not found'}, status=404)
            
            elif command == 'CancelTransaction':
                # Cancel transaction
                order_id = data.get('params', {}).get('account', {}).get('order_id')
                payment = Payment.objects.filter(transaction_id=order_id).first()
                if payment:
                    payment.status = 'cancelled'
                    payment.save()
                    return JsonResponse({'result': {'transaction': str(payment.id), 'state': -1}})
                return JsonResponse({'error': 'Transaction not found'}, status=404)
            
            elif command == 'CheckTransaction':
                # Check transaction status
                order_id = data.get('params', {}).get('account', {}).get('order_id')
                payment = Payment.objects.filter(transaction_id=order_id).first()
                if payment:
                    state = 2 if payment.status == 'paid' else 1 if payment.status == 'pending' else -1
                    return JsonResponse({'result': {'transaction': str(payment.id), 'state': state}})
                return JsonResponse({'error': 'Transaction not found'}, status=404)
            
            else:
                return JsonResponse({'error': 'Unknown command'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def click_webhook_view(request):
    """
    Click webhook handler
    """
    if request.method == 'POST':
        try:
            data = request.POST
            
            # Verify the request
            service = PaymentService()
            if not service.click.verify_webhook(data):
                return JsonResponse({'error': 'Invalid signature'}, status=400)
            
            # Handle Click commands
            action = data.get('action')
            
            if action == 'prepare':
                # Prepare transaction
                order_id = data.get('merchant_trans_id')
                payment = Payment.objects.filter(transaction_id=order_id).first()
                if payment:
                    return JsonResponse({'click_trans_id': data.get('click_trans_id'), 'merchant_trans_id': order_id})
                return JsonResponse({'error': 'Order not found'}, status=404)
            
            elif action == 'complete':
                # Complete transaction
                order_id = data.get('merchant_trans_id')
                payment = Payment.objects.filter(transaction_id=order_id).first()
                if payment and payment.status == 'pending':
                    payment.status = 'paid'
                    payment.payment_date = timezone.now()
                    payment.save()
                    
                    # Create enrollment
                    if not Enrollment.objects.filter(user=payment.user, course=payment.course).exists():
                        Enrollment.objects.create(user=payment.user, course=payment.course)
                        payment.course.students_count += 1
                        payment.course.save()
                    
                    return JsonResponse({'click_trans_id': data.get('click_trans_id'), 'merchant_trans_id': order_id})
                return JsonResponse({'error': 'Transaction not found'}, status=404)
            
            else:
                return JsonResponse({'error': 'Unknown action'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
