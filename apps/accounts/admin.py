from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Wallet, Transaction, UserLevel, Badge, UserBadge, PaymentCard


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin
    """
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_verified', 'is_staff', 'created_at')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'avatar', 'bio', 'date_of_birth')}),
        ('Role & Status', {'fields': ('role', 'is_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """
    Wallet admin
    """
    list_display = ('user', 'balance', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Transaction admin
    """
    list_display = ('user', 'transaction_type', 'amount', 'status', 'description', 'created_at')
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('user__email', 'user__username', 'description')
    readonly_fields = ('created_at',)


@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    """
    User Level admin
    """
    list_display = ('user', 'level', 'points', 'xp', 'streak_days', 'last_activity_date')
    list_filter = ('level', 'created_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    """
    Badge admin
    """
    list_display = ('name', 'slug', 'badge_type', 'points_required', 'is_active', 'created_at')
    list_filter = ('badge_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    """
    User Badge admin
    """
    list_display = ('user', 'badge', 'earned_at')
    list_filter = ('badge__badge_type', 'earned_at')
    search_fields = ('user__email', 'badge__name')
    readonly_fields = ('earned_at',)


@admin.register(PaymentCard)
class PaymentCardAdmin(admin.ModelAdmin):
    """
    Payment Card admin
    """
    list_display = ('user', 'card_type', 'get_masked_number', 'balance', 'is_default', 'is_active', 'created_at')
    list_filter = ('card_type', 'is_default', 'is_active', 'created_at')
    search_fields = ('user__email', 'card_holder', 'card_number')
    readonly_fields = ('created_at', 'updated_at')
