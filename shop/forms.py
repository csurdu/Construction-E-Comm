from django import forms

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

        order = Order.objects.create(
            customer_name=self.cleaned_data["customer_name"],
            customer_email=self.cleaned_data.get("customer_email", ""),
        )
        OrderItem.objects.create(
            order=order,
            item=item,
            quantity=quantity,
            unit_price=item.price,
        )

        item.quantity = max(item.quantity - quantity, 0)
        item.save(update_fields=["quantity", "last_updated"])
        return order
