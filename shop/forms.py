from django import forms
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import Item, Order, OrderItem


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "price", "quantity"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }


class OrderForm(forms.Form):
    customer_name = forms.CharField(max_length=150)
    customer_email = forms.EmailField(required=False)
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    quantity = forms.IntegerField(min_value=1, label="Quantity")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["item"].queryset = Item.objects.filter(quantity__gt=0)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control mb-2"})
            if name == "item":
                field.widget = forms.HiddenInput()

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        item = self.cleaned_data.get("item")
        if item and quantity > item.quantity:
            raise forms.ValidationError(
                f"Only {item.quantity} item(s) left in stock. Please reduce the quantity."
            )
        return quantity

    def create_order(self) -> Order:
        item = self.cleaned_data["item"]
        quantity = self.cleaned_data["quantity"]

        with transaction.atomic():
            # Lock the row to prevent overselling during concurrent orders.
            locked_item = (
                Item.objects.select_for_update()
                .filter(pk=item.pk)
                .first()
            )
            if locked_item is None or locked_item.quantity < quantity:
                raise forms.ValidationError(
                    "The item is no longer available in the requested quantity."
                )

            order = Order.objects.create(
                customer_name=self.cleaned_data["customer_name"],
                customer_email=self.cleaned_data.get("customer_email", ""),
            )
            OrderItem.objects.create(
                order=order,
                item=locked_item,
                quantity=quantity,
                unit_price=locked_item.price,
            )

            Item.objects.filter(pk=locked_item.pk).update(
                quantity=F("quantity") - quantity,
                last_updated=timezone.now(),
            )
        return order
