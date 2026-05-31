from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    coins = models.PositiveIntegerField(default=0)  # Coins for shop
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def add_coins(self, amount):
        """Add coins to user"""
        self.coins += amount
        self.save()
    
    def deduct_coins(self, amount):
        """Deduct coins from user"""
        if self.coins >= amount:
            self.coins -= amount
            self.save()
            return True
        return False


class Wallet(models.Model):
    """
    User wallet for balance management
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='legacy_wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
    
    def __str__(self):
        return f"{self.user.email} - {self.balance} so'm"
    
    def add_balance(self, amount):
        """Add balance to wallet"""
        self.balance += Decimal(str(amount))
        self.save()
    
    def deduct_balance(self, amount):
        """Deduct balance from wallet"""
        amount = Decimal(str(amount))
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False


class Transaction(models.Model):
    """
    Transaction history for wallet operations
    """
    TRANSACTION_TYPES = [
        ('topup', 'Top Up'),
        ('purchase', 'Purchase'),
        ('refund', 'Refund'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount} so'm"


class UserLevel(models.Model):
    """
    User level for gamification
    """
    LEVEL_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_level')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='bronze')
    points = models.PositiveIntegerField(default=0)
    xp = models.PositiveIntegerField(default=0)  # Experience points
    streak_days = models.PositiveIntegerField(default=0)  # Consecutive learning days
    last_activity_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Level'
        verbose_name_plural = 'User Levels'
    
    def __str__(self):
        return f"{self.user.email} - {self.level} ({self.points} points)"
    
    def add_points(self, points):
        """Add points to user and check for level up"""
        self.points += points
        self.xp += points
        self.check_level_up()
        self.save()
    
    def check_level_up(self):
        """Check if user should level up based on points"""
        level_thresholds = {
            'bronze': 0,
            'silver': 500,
            'gold': 2000,
            'platinum': 5000,
            'diamond': 10000,
        }
        
        for level, threshold in reversed(level_thresholds.items()):
            if self.points >= threshold:
                if self.level != level:
                    self.level = level
                break


class Badge(models.Model):
    """
    Badge model for achievements
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True, null=True)
    points_required = models.PositiveIntegerField(default=0)
    badge_type = models.CharField(max_length=50)  # course, lesson, streak, referral, etc.
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'
        ordering = ['points_required']
    
    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """
    User badge earned
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='earned_by')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Badge'
        verbose_name_plural = 'User Badges'
        unique_together = ('user', 'badge')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.badge.name}"


class PaymentCard(models.Model):
    """
    User payment card for payments
    """
    CARD_TYPE_CHOICES = [
        ('uzcard', 'Uzcard'),
        ('humo', 'Humo'),
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('click', 'Click'),
        ('payme', 'Payme'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_cards')
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES)
    card_number = models.CharField(max_length=19)  # Encrypted in production
    card_holder = models.CharField(max_length=100)
    expiry_date = models.CharField(max_length=5)  # MM/YY
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Payment Card'
        verbose_name_plural = 'Payment Cards'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        masked_number = f"**** **** **** {self.card_number[-4:]}"
        return f"{self.user.email} - {self.get_card_type_display()} - {masked_number}"
    
    def get_masked_number(self):
        """Return masked card number for display"""
        return f"**** **** **** {self.card_number[-4:]}"
    
    def add_balance(self, amount):
        """Add balance to card"""
        self.balance += Decimal(str(amount))
        self.save()
    
    def deduct_balance(self, amount):
        """Deduct balance from card"""
        amount = Decimal(str(amount))
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False


class ShopItem(models.Model):
    """
    Shop items for coin-based purchases
    """
    CATEGORY_CHOICES = [
        ('stationery', 'Qog\'oz mahsulotlari'),
        ('electronics', 'Elektronika'),
        ('clothing', 'Kiyim-kechak'),
        ('accessories', 'Aksessuarlar'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='accessories')
    price_coins = models.PositiveIntegerField()  # Price in coins
    price_som = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional real price
    image = models.ImageField(upload_to='shop/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Shop Item'
        verbose_name_plural = 'Shop Items'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.price_coins} coins"


class Purchase(models.Model):
    """
    User purchases from shop
    """
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('completed', 'Bajarildi'),
        ('cancelled', 'Bekor qilindi'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE, related_name='purchases')
    coins_spent = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.item.name}"
