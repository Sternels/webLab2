from django.contrib import admin
from .models import Product, Category, Cart, CartDetails, Orders, OrderDetails, Status

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartDetails)


class OrderDetailsTabularInline(admin.TabularInline):
    model = OrderDetails
    extra = 0
    can_delete = False
    verbose_name_plural = 'Детали заказа'

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    inlines = [OrderDetailsTabularInline]
    readonly_fields = ('id', 'guest_session_id', 'zip', 'mail', 'address', 'fname', 'lname', 'total_sum', 'date_create')
    list_filter = ('date_create', 'status')

    def has_add_permission(self, request):
        return False
# Register your models here.
