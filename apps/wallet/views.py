from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from apps.courses.models import Course, Enrollment

from .forms import AddBalanceForm
from .models import Transaction
from .services import add_balance, get_wallet_for_user, purchase_course


@login_required
def wallet_dashboard(request):
    wallet = get_wallet_for_user(request.user)
    transactions = wallet.transactions.all()[:10]
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course').order_by('-enrolled_at')
    total_spent = wallet.transactions.filter(transaction_type=Transaction.PURCHASE).aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'wallet/dashboard.html', {
        'wallet': wallet,
        'transactions': transactions,
        'enrollments': enrollments,
        'total_spent': total_spent,
    })


@login_required
def add_balance_view(request):
    wallet = get_wallet_for_user(request.user)

    if request.method == 'POST':
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            try:
                add_balance(request.user, form.cleaned_data['amount'])
            except ValidationError as exc:
                messages.error(request, exc.messages[0])
            else:
                messages.success(request, 'Wallet balance updated successfully.')
                return redirect('wallet:dashboard')
        else:
            messages.error(request, 'Please enter a valid positive amount.')
    else:
        form = AddBalanceForm()

    return render(request, 'wallet/add_balance.html', {'form': form, 'wallet': wallet})


@login_required
def purchase_course_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)

    if request.method != 'POST':
        return redirect('courses:detail', slug=course.slug)

    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, 'You have already purchased this course.')
        return redirect('courses:detail', slug=course.slug)

    try:
        purchase_course(request.user, course)
    except ValidationError as exc:
        messages.error(request, exc.messages[0])
        return redirect('courses:detail', slug=course.slug)

    messages.success(request, 'Course purchased successfully.')
    return redirect('dashboard:my_courses')
