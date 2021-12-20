from django.shortcuts import render, redirect
from product.models import shop_categories, shop_products, reviews

from .forms import product_filter_form

from django.core.paginator import Paginator

import datetime
from django.db.models import Q

from cart.models import cart
from itertools import chain


# Create your views here.
def shop(request):
    if request.method == "POST": #POST REQUEST

        search = request.POST.get('shop_product_name')
        request.session['search'] = search
        cat = request.POST.get('category')
        request.session['cat'] = cat
        sortcondition = request.POST.get('sort_order')
        request.session['sort'] = sortcondition

        cat_titles = shop_categories.objects.all().filter(category_name__contains = search)
        print('THE CATEGORY TITLES AREeeeeeeeeeeeeeeeeeeeee' , cat_titles )

        form = product_filter_form(initial = {'shop_product_name' : search , 'category' : cat , 'sort_order' : sortcondition })
        all_shop_products = shop_products.objects.all()

        #FILTERING BASED ON SEARCH FILTERS

        if search:
            print('Yes there is search filteraaaaaaaaaaa', search)
            all_shop_products = all_shop_products.filter(Q(category__in = cat_titles) | Q(shop_product_name__contains = request.POST.get('shop_product_name')) )
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaall shop pdts are ' , all_shop_products)

        if cat != '2':
            print('sort by category')
            search_cat = shop_categories.objects.all().filter(id = cat)
            all_shop_products = all_shop_products.filter(category__in = search_cat)
            category_title = search_cat.first().category_name
        else:
            category_title= None

        if sortcondition == "SortAscending":
            print('Yes there is ascending filter')
            all_shop_products = all_shop_products.order_by('shop_product_cost')

        if sortcondition == "SortDescending":
            print('Yes there is desc filter')
            all_shop_products = all_shop_products.order_by('-shop_product_cost')


        #FILTER OVER

        per_page = 9
        product_paginator = Paginator(all_shop_products , per_page)
        page_num = request.GET.get('page')
        print('ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss',page_num)
        products_page = product_paginator.get_page(page_num)

        context = {
            #'all_shop_products' : all_shop_products,
            'all_shop_products' : products_page,
            'form' : form,
            'pgcount' : product_paginator.num_pages,
            'per_page' : per_page,
            'category_title' : category_title,
        }
        return render(request, 'shopproducts/allproducts.html' , context)

    else: # GET REQUEST

        all_shop_products = shop_products.objects.all()
        

        if 'search' in request.session:
            cat_titles = shop_categories.objects.all().filter(category_name__contains =  request.session['search'])
            print('Yes there is search filterbbbb')
            all_shop_products = all_shop_products.filter(Q(category__in = cat_titles) | Q(shop_product_name__contains = request.session['search']))

        
        if 'cat' in request.session and request.session['cat'] != '2':
            print('sort by category')
            search_cat = shop_categories.objects.all().filter(id = request.session['cat'])
            all_shop_products = all_shop_products.filter(category__in = search_cat)
            category_title = search_cat.first().category_name
        else:
            category_title = None

        if 'sort' in request.session:
            if request.session['sort'] == "SortAscending":
                print('Yes there is ascending filter')
                all_shop_products = all_shop_products.order_by('shop_product_cost')
            elif request.session['sort'] == "SortDescending":
                print('Yes there is desc filter')
                all_shop_products = all_shop_products.order_by('-shop_product_cost')
        
        if 'cat' in request.session:
            form = product_filter_form(initial = {'category':request.session['cat']})
        else:
            form = product_filter_form()

        per_page = 9
        product_paginator = Paginator(all_shop_products , per_page)
        page_num = request.GET.get('page')
        products_page = product_paginator.get_page(page_num)
        
        context= {
            #'all_shop_products' : all_shop_products,
            'all_shop_products' : products_page,   #passing the paginated products

            'form': form,
            'pgcount' : product_paginator.num_pages,
            'per_page' : per_page,
            'category_title' : category_title
        }

        
        return render(request, 'shopproducts/allproducts.html' , context)


def shop_product_category(request, pk):

    cat = shop_categories.objects.get(id = pk)
    request.session['cat'] = cat.category_name

    all_shop_products = shop_products.objects.all()
    search_cat = shop_categories.objects.all().filter(id = pk)
    all_shop_products = all_shop_products.filter(category__in = search_cat)

    form = product_filter_form()

    per_page = 6
    product_paginator = Paginator(all_shop_products , per_page)
    page_num = request.GET.get('page')
    products_page = product_paginator.get_page(page_num)

    context = {
        #'all_shop_products' : all_shop_products,
        'all_shop_products' : products_page,
        'form' : form,
        'pgcount' : product_paginator.num_pages,
        'per_page' : per_page,
        'category_title' : search_cat.first().category_name
    }
    return render(request, 'shopproducts/allproducts.html' , context)


def shop_product_detail(request, pk):

    shop_product_detail = shop_products.objects.get(id = pk)

    if request.method == "POST":
        print(request.POST)

        current_time = datetime.datetime.now() 
        hours_added = datetime.timedelta(hours = 9)
        corrected_datetime = current_time + hours_added

        review_inst = reviews.objects.create(
            reviewed_pdt = shop_product_detail,
            reviewed_by = request.user,
            rating = request.POST.get('review-rating'),
            review = request.POST.get('review-content'),
            created_on = corrected_datetime
        )

        review_inst.save()
        print(review_inst)
        return redirect('product:shop_product_detail',shop_product_detail.id ) 
        

    else:
        print('sssssssssssssssssssssssssssssssss' , shop_product_detail)
        print(shop_product_detail.category.all())
        related_cat = shop_categories.objects.get(id = shop_product_detail.category.first().id)
        print(related_cat)
        related_pdts = shop_products.objects.all().filter(category = related_cat)
        shop_pdt_review = reviews.objects.all().filter(reviewed_pdt = shop_product_detail) 
        print('related pdts is sssssssssssssssssssssssss' , related_pdts)
        context = {
            'shop_product_detail' : shop_product_detail,
            'related_pdts' : related_pdts,
            'review' : shop_pdt_review
        }
        return render(request, 'shopproducts/shop_singleproduct.html', context)


def add_to_cart(request, pk):
    print('creating cart object')
    
    pdt = shop_products.objects.get(id=pk)
    user_inst = request.user

    current_time = datetime.datetime.now() 
    hours_added = datetime.timedelta(hours = 9)
    corrected_datetime = current_time + hours_added

    cart_inst = cart.objects.create(cart_product = pdt , cart_user = user_inst, created_at = corrected_datetime, cart_status = "pending" )
    cart_inst.save()

    print('cart created ' , cart_inst)

    return redirect('cart:cart_home')


def sell(request):
    if request.method == "POST":
        print('post is ', request.POST)
        print('files is ', request.FILES)

        current_time = datetime.datetime.now() 
        hours_added = datetime.timedelta(hours = 9)

        corrected_datetime = current_time + hours_added

        image1 = request.FILES.get('image1')
        
        try:
            image2 = request.FILES.get('image2')
        except:
            image2 = None
        
        try:
            image3 = request.FILES.get('image3')
        except:
            image3 = None

        try:
            image4 = request.FILES.get('image4')
        except:
            image4 = None

        category_ids = request.POST.getlist('category')
        print('cat ids is  ', category_ids)
        if not category_ids:
            print('nothing available')
            category_ids = shop_categories.objects.all().filter(category_name = "None")
            print('CAt id after alteration is ', category_ids)
            
        new_pdt = shop_products.objects.create(
            shop_product_name = request.POST.get('pdtname'),
            shop_product_desc = request.POST.get('pdtdesc'),
            shop_product_cost = request.POST.get('pdtcost'),
            created_at = corrected_datetime,
            created_by = request.user,
            shop_product_image = image1,
            shop_product_image2 = image2,
            shop_product_image3 = image3,
            shop_product_image4 = image4,
        )   
        for cat_ids in category_ids:
            if cat_ids == None:
                print('adding none')
                cat_inst = shop_categories.objects.get(category_name = "None")
                new_pdt.category.add(cat_inst)
            else:
                print('222222222222222222222222222222222222222222222222',cat_ids)
                cat_inst = shop_categories.objects.get(id = cat_ids)
                new_pdt.category.add(cat_inst)
                print('added ', cat_inst.category_name)
                print(new_pdt.category)
        
        new_pdt.save()

        return redirect('product:shop')

    all_cat = shop_categories.objects.all().filter(~Q(category_name = "None"))

    context = {
        'cats' : all_cat
    }
    return render(request, 'shopproducts/sell.html', context)