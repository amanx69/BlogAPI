from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'username', 'email', 'country', 'created_at']
    list_filter = [ 'is_public', 'gender', 'country', 'created_at']
    search_fields = [ 'user__email', 'bio', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user']
    
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'
    
    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'


# Register your models here.
