from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - human readable
        return f"{self.name} ({self.quantity} available)"

    def in_stock(self) -> bool:
        return self.quantity > 0


class Order(models.Model):
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - human readable
        return f"Order #{self.id} - {self.customer_name}"

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="order_items", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("order", "item")

    def __str__(self) -> str:  # pragma: no cover - human readable
        return f"{self.quantity} x {self.item.name}"
