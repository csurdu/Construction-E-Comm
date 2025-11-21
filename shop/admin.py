from django.contrib import admin

from .models import Item, Order, OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "last_updated")
    search_fields = ("name",)
    ordering = ("name",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "customer_email", "created_at", "item_count")
    search_fields = ("customer_name", "customer_email")
    inlines = [OrderItemInline]

    def item_count(self, obj):  # pragma: no cover - display helper
        return obj.total_items


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "item", "quantity", "unit_price")
    raw_id_fields = ("order", "item")
