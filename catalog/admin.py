from django.contrib import admin

from catalog.models import Headphones, HeadphonesCategory, Brand, HeadPhonesPhoto

class PhotoInline(admin.StackedInline):
    model = HeadPhonesPhoto

admin.site.register(HeadPhonesPhoto)

class HeadphonesAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    list_display = ('name', 'price', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Headphones, HeadphonesAdmin)

class HeadphonesCategoryadmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description',]
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(HeadphonesCategory, HeadphonesCategoryadmin)

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Brand, BrandAdmin)
