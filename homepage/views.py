from django.shortcuts import redirect, render
from registration.models import user_profile
from .models import subscribe
from django.contrib.auth.decorators import login_required
import datetime

from product.models import shop_categories, shop_products

# Create your views here.
@login_required
def home(request):
    print('Lets delete all cookies')
    
    request.session.pop("search", None)
    request.session.pop("cat", None)
    request.session.pop("sort", None)
    request.session.modified = True

    print('deleted the cookies')

    if request.user.is_authenticated:
        curruser = request.user
        products = shop_products.objects.order_by("-created_at")[:6]


        return render(request,'landing/homepage.html',{'curr_user' : curruser , 'products':products})
    else:
        print('authenticate to login page from inside the view and not the decorator')
        return redirect('registration:signin')

@login_required
def categories(request):

    categories = shop_categories.objects.all()

    context = {

        'categories' : categories

    }
    return render(request, 'landing/categories.html', context)


@login_required
def contactus(request):
    return render(request, 'landing/contactus.html')

@login_required
def subscription(request):

    if request.method == "POST":
        print(request.POST)

        current_time = datetime.datetime.now() 
        hours_added = datetime.timedelta(hours = 9)
        corrected_datetime = current_time + hours_added

        subs_instance = subscribe.objects.create(
            name = request.user,
            email = request.POST.get('subsemail'),
            created_on = corrected_datetime,
        )
        subs_instance.save()
        print('subs created is ', subs_instance)

        return redirect('homepage:home')

    else:
        return redirect('homepage:home')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def privacy(request):
    today = datetime.datetime.now()

    context = {
        'today' : today
    }
    return render(request, 'landing/privacy_policy.html' , context)


@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def singleproduct(request):
    return render(request, 'single-product.html')

