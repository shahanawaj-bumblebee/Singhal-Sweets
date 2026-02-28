from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem


# ---------------- HOME ----------------
def home(request):
    products = Product.objects.all()[:4]
    return render(request, "home.html", {"products": products})


# ---------------- ALL PRODUCTS ----------------
def products(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})


# ---------------- PRODUCT DETAIL ----------------
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product_detail.html", {"product": product})



# ---------------- ADD TO CART ----------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


# ---------------- VIEW CART ----------------
@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


# ---------------- REMOVE ITEM ----------------
@login_required
def remove_from_cart(request, id):
    cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=cart, product_id=id).delete()
    return redirect("cart")


# ---------------- UPDATE QUANTITY ----------------
@login_required
def update_quantity(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == "increase":
        item.quantity += 1
    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1

    item.save()
    return redirect("cart")


# ---------------- REGISTER ----------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cart.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


# ---------------- CHECKOUT (Simple Working Version) ----------------
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)

    if request.method == "POST":
        items.delete()  # Clear cart after order
        return redirect("home")

    return render(request, "checkout.html", {"total": total})

def contact(request):
    return render(request, "contact.html")