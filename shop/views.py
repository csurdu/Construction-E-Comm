from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ItemForm, OrderForm
from .models import Item


def home(request):
    items = Item.objects.all()
    order_form = OrderForm(request.POST or None)
    submitted_item_id = request.POST.get("item") if request.method == "POST" else None
    if request.method == "POST" and order_form.is_valid():
        order = order_form.create_order()
        messages.success(
            request,
            f"Order #{order.id} placed for {order.total_items} item(s). We will contact you soon!",
        )
        return redirect(reverse("home"))

    context = {
        "items": items,
        "order_form": order_form,
        "submitted_item_id": submitted_item_id,
    }
    return render(request, "shop/home.html", context)


def inventory(request):
    items = Item.objects.all()
    context = {
        "items": items,
    }
    return render(request, "shop/inventory.html", context)


def add_item(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Item added to inventory.")
        return redirect("inventory")
    return render(
        request,
        "shop/item_form.html",
        {"form": form, "title": "Add Item"},
    )


def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, "Item updated successfully.")
        return redirect("inventory")
    return render(
        request,
        "shop/item_form.html",
        {"form": form, "title": f"Edit {item.name}"},
    )
