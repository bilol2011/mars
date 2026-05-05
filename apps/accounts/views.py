from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, PaymentCardForm
from .models import User, Wallet, Transaction, PaymentCard, ShopItem, Purchase


def register_view(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Ro\'yxatdan muvaffaqiyatli o\'tdingiz! Tizimga kirishingiz mumkin.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Xush kelibsiz, {user.get_full_name()}!')
            return redirect('dashboard:home')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'Tizimdan muvaffaqiyatli chiqdingiz.')
    return redirect('courses:home')


@login_required
def profile_view(request):
    """
    User profile view
    """
    user = request.user
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil ma\'lumotlari yangilandi.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'accounts/profile.html', {'form': form, 'user': user})


@login_required
def profile_detail_view(request, username):
    """
    Public profile view for mentors
    """
    user = get_object_or_404(User, username=username, role='mentor')
    return render(request, 'accounts/profile_detail.html', {'profile_user': user})


@login_required
def wallet_view(request):
    """
    Wallet view showing balance and transaction history
    """
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:20]
    cards = PaymentCard.objects.filter(user=request.user, is_active=True)
    
    context = {
        'wallet': wallet,
        'transactions': transactions,
        'cards': cards,
    }
    return render(request, 'accounts/wallet.html', context)


@login_required
def add_balance_view(request):
    """
    Add balance to wallet from card
    """
    if request.method == 'POST':
        amount = request.POST.get('custom_amount')
        card_id = request.POST.get('card_id')
        
        # Validate amount
        if not amount:
            messages.error(request, 'Summa kiritilmadi.')
            return redirect('accounts:wallet')
        
        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, 'Summa musbat bo\'lishi kerak.')
                return redirect('accounts:wallet')
        except ValueError:
            messages.error(request, 'Noto\'g\'ri summa formati.')
            return redirect('accounts:wallet')
        
        # Get selected card
        if not card_id:
            messages.error(request, 'Karta tanlanmadi.')
            return redirect('accounts:wallet')
        
        try:
            card = PaymentCard.objects.get(id=card_id, user=request.user)
        except PaymentCard.DoesNotExist:
            messages.error(request, 'Karta topilmadi.')
            return redirect('accounts:wallet')
        
        # Check card balance
        if card.balance < amount:
            messages.error(request, f'Kartada yetarli mablag\' yo\'q. Kerak: {amount} so\'m, Kartada: {card.balance} so\'m')
            return redirect('accounts:wallet')
        
        # Process top-up
        with transaction.atomic():
            # Deduct from card
            card.deduct_balance(amount)
            
            # Get or create wallet
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            
            # Add to wallet
            wallet.add_balance(amount)
            
            # Create transaction record
            Transaction.objects.create(
                user=request.user,
                transaction_type='topup',
                amount=amount,
                status='success',
                description=f'Hisobni to\'ldirish (karta orqali): {amount} so\'m'
            )
        
        messages.success(request, f'{amount} so\'m hisobingizga qo\'shildi! Kartadan {amount} so\'m yechildi.')
        return redirect('accounts:wallet')
    
    return redirect('accounts:wallet')


@login_required
def add_card_view(request):
    """
    Add payment card view with auto balance detection
    """
    if request.method == 'POST':
        form = PaymentCardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            
            # Auto-detect card balance (simulated - in production use bank API)
            # For demo purposes, set a realistic random balance
            import random
            from decimal import Decimal
            detected_balance = Decimal(str(random.randint(500000, 5000000) / 1000))
            card.balance = detected_balance
            
            # If this is the first card, make it default
            if not request.user.payment_cards.exists():
                card.is_default = True
            
            card.save()
            messages.success(request, f'Karta muvaffaqiyatli qo\'shildi! Kartadagi balans: {card.balance} so\'m')
            return redirect('accounts:wallet')
    else:
        form = PaymentCardForm()
    
    return render(request, 'accounts/add_card.html', {'form': form})


@login_required
def set_default_card_view(request, card_id):
    """
    Set a card as default
    """
    card = get_object_or_404(PaymentCard, id=card_id, user=request.user)
    
    # Remove default from all cards
    request.user.payment_cards.update(is_default=False)
    
    # Set this card as default
    card.is_default = True
    card.save()
    
    messages.success(request, 'Karta asosiy qilib belgilandi!')
    return redirect('accounts:wallet')


@login_required
def delete_card_view(request, card_id):
    """
    Delete a payment card
    """
    card = get_object_or_404(PaymentCard, id=card_id, user=request.user)
    
    if card.is_default:
        messages.error(request, 'Asosiy kartani o\'chirib bo\'lmaydi!')
        return redirect('accounts:wallet')
    
    card.delete()
    messages.success(request, 'Karta o\'chirildi!')
    return redirect('accounts:wallet')


@login_required
def shop_view(request):
    """
    Shop page with items for purchase
    """
    items = ShopItem.objects.filter(is_active=True, stock__gt=0)
    user_purchases = Purchase.objects.filter(user=request.user).values_list('item_id', flat=True)
    
    context = {
        'items': items,
        'user_purchases': user_purchases,
        'user_coins': request.user.coins,
    }
    return render(request, 'accounts/shop.html', context)


@login_required
def purchase_item_view(request, item_slug):
    """
    Purchase an item from shop
    """
    item = get_object_or_404(ShopItem, slug=item_slug, is_active=True)
    
    # Check if already purchased
    if Purchase.objects.filter(user=request.user, item=item).exists():
        messages.warning(request, 'Siz allaqachon bu mahsulotni sotib olgansiz.')
        return redirect('accounts:shop')
    
    # Check if user has enough coins
    if request.user.coins < item.price_coins:
        messages.error(request, f'Yetarli coin yo\'q. Kerak: {item.price_coins}, Sizda: {request.user.coins}')
        return redirect('accounts:shop')
    
    # Check stock
    if item.stock <= 0:
        messages.error(request, 'Mahsulot tugadi.')
        return redirect('accounts:shop')
    
    # Process purchase
    with transaction.atomic():
        # Deduct coins
        request.user.deduct_coins(item.price_coins)
        
        # Create purchase record
        Purchase.objects.create(
            user=request.user,
            item=item,
            coins_spent=item.price_coins
        )
        
        # Reduce stock
        item.stock -= 1
        item.save()
    
    messages.success(request, f'{item.name} muvaffaqiyatli sotib olindi!')
    return redirect('accounts:shop')


@login_required
def my_purchases_view(request):
    """
    User's purchase history
    """
    purchases = Purchase.objects.filter(user=request.user, status='completed').select_related('item')
    
    context = {
        'purchases': purchases,
    }
    return render(request, 'accounts/my_purchases.html', context)
