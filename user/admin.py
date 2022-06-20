from django.contrib import admin
from .models import User as UserModel, UserProfile as UserProfileModel, Hobby as HobbyModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# TabularInline / StackedInline
# class UserProfileInline(admin.TabularInline):
class UserProfileInline(admin.StackedInline):
    model = UserProfileModel
    filter_horizontal = ["hobby"]

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'name', 'email')
    list_display_links = ('username', )
    list_filter = ('username', )
    search_fields = ('username', 'email', )
    
    fieldsets = (
        ("info", {"fields": ("username", "password", "email", "name", "join_data", )}),
        ("Permissions", {"fields": ("is_admin", "is_active", )}),)
    
    filter_horizontal = []
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_data',)
        else:
            return ('join_data', )
        
    # 여기에 인라인을 지정해준다.
    inlines = (
            UserProfileInline,
        )
    
    # def has_add_permission(self, request, obj=None): # 추가 권한
    #     print(request.user)
    #     return False

    # def has_delete_permission(self, request, obj=None): # 삭제 권한
    #     print(request.user)
    #     return False

    # def has_change_permission(self, request, obj=None): # 수정 권한
    #     print(request.user)
    #     return False
        

# Register your models here.
admin.site.register(UserModel, UserAdmin)
admin.site.register(UserProfileModel)
admin.site.register(HobbyModel)