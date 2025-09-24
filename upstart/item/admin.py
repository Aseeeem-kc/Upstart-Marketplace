from django.contrib import admin
from .models import Category, Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_sold', 'created_by', 'created_at')
    list_filter = ('category', 'is_sold', 'created_at')
    search_fields = ('name', 'description', 'category__name', 'created_by__username')
    list_editable = ('price', 'is_sold')
    date_hierarchy = 'created_at'

    def category_name(self, obj):
        return obj.category.name
    category_name.short_description = 'Category'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'n_products')
    search_fields = ['name']

    def n_products(self, obj):
        return obj.items.count()

    n_products.short_description = 'Number of Products'

# Registering the models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
