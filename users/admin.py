from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Message
from .models import Offer

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'type', 'credits', 'is_staff', 'is_active')
    list_filter = ('type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Infos supplémentaires', {'fields': ('type', 'credits')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'type', 'credits', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


    class OfferAdmin(admin.ModelAdmin):
        list_display = ('user', 'ma_devise', 'taux_souhaite', 'ma_devise', 'status', 'date_creation')
        list_filter = ('status', 'ma_devise', 'ma_devise')
        search_fields = ('user__username', 'ma_devise', 'ma_devise')

    admin.site.register(Offer, OfferAdmin)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Message)
