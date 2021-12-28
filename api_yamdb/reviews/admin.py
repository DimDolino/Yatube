from django.contrib import admin

from .models import (Title, Category, Genre,
                     User, Review, Comment)


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role', 'bio')
    search_fields = ('username',)
    empty_value_display = '-пусто-'
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
