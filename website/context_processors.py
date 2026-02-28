from .models import CartItem, Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            count = CartItem.objects.filter(cart=cart).count()
            return {'cart_count': count}
    return {'cart_count': 0}