from cart.models import cart

def cart_count_context_processor(request):
    if request.user.is_authenticated:
        print('context processor main')
        cart_count = cart.objects.all().filter(cart_user = request.user, cart_status = "pending").count()
        return {'cart_count' : cart_count}
    else:
        print('context processor else')
        return {'cart_count' : 1}