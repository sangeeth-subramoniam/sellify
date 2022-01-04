from django.shortcuts import redirect, render

from registration.models import user_profile
from .forms import User_form , user_profile_form


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import ensure_csrf_cookie

import datetime


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import logs

from django.contrib.auth.models import User
from .forms import *

# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print('xforw is ', x_forwarded_for)
    if x_forwarded_for:
        #ip = x_forwarded_for.split(',')[-1]
        ip = str(x_forwarded_for)
        print('xforward')
    else:
        ip = request.META.get('REMOTE_ADDR')
        print('remote addr')
    return ip


def signup(request):
    if request.user.is_authenticated:
        return redirect('homepage:home')
    else:
        registered = False

        if request.method == "POST":

            print('Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' , request.POST)
            
            user_form = User_form(data=request.POST)
            user_profileform = user_profile_form(data=request.POST)


            if(user_form.is_valid() and user_profileform.is_valid()):
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                profile = user_profileform.save(commit=False)
                profile.user = user

                        
                if 'profile_picture' in request.FILES:
                    profile.profile_picture = request.FILES['profile_picture']
                
                profile.save()

                registered = True

                username = request.POST.get('username')
                password = request.POST.get('password')

                user_inst = authenticate(username=username, password = password)

                getip = get_client_ip(request)
                print('the ip used is ', getip)

                current_time = datetime.datetime.now() 
                hours_added = datetime.timedelta(hours = 9)
                corrected_datetime = current_time + hours_added

                user_log = logs.objects.create(logger = username , start_time = corrected_datetime , ip = getip, location = 'Japan' , status = 'pending' )
                user_log.save()

                login(request,user_inst)
                return HttpResponseRedirect(reverse('homepage:home'))


            
            else:
                print(user_form.errors, user_profileform.errors)
        
        else:
            user_form = User_form()
            user_profileform = user_profile_form
        
            return render(request, "registration/signup.html", {'user_form': user_form , 'user_profileform' : user_profileform, 'registered' : registered  } )


@ensure_csrf_cookie
def signin(request):
    if request.user.is_authenticated:
        return redirect('homepage:home')
    else:
        
        if(request.method == "POST"): 
            print('entering post heeeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')           
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password = password)

            if user:
                if user.is_active:
                    getip = get_client_ip(request)
                    print('the ip used is ', getip)

                    current_time = datetime.datetime.now() 
                    hours_added = datetime.timedelta(hours = 9)
                    corrected_datetime = current_time + hours_added

                    user_log = logs(logger = username , start_time = corrected_datetime , ip = getip, location = 'Japan' , status = 'pending' )
                    user_log.save()
                    login(request,user)
                    return redirect('homepage:home')
                
                else:
                    return HttpResponse('account is NOT Active')
                
            else:
                print("someone tried to login and failed")
                print("username: {} and password {}".format(username,password))
                context = {
                    'signin_error' : 'INVALID SIGNIN CREDENTIALS. PLEASE TRY AGAIN!'
                }
                return render(request,'registration/signin.html', context)
        
        else:
            print('enter getttttttttttttttttttttttttttttttttttttttt of signin')
            return render(request,'registration/signin.html')

@login_required
def signout(request):

    try:
        log = logs.objects.all().filter(logger = request.user.username, status = 'pending').order_by('-start_time').first()
        
        current_time = datetime.datetime.now() 
        hours_added = datetime.timedelta(hours = 9)
        corrected_datetime = current_time + hours_added
        
        log.end_time = corrected_datetime
        log.status = 'over'
        log.save()
    except:
        print('log not found')

    logout(request)
    return HttpResponseRedirect(reverse("homepage:home"))

def change_password1(request):
    if request.method == "POST":
        print(request.POST)
        user = request.POST.get('username')
        verification_mail = request.POST.get('email_check')
        try:
            user = User.objects.get(username = user , email = verification_mail)            
        except:
            errormessage = "The username/email you entered is wrong or doesnt exist ..."
            return render(request, 'registration/change_password1.html' , {'errormessage' : errormessage})

        print('user in pwd1 test is ' , user , ' sending it to pwd2 with params ' , user.id)
        request.session['userchange'] = user.id
        return redirect('registration:change_password2')
        
    else:
        return render(request, 'registration/change_password1.html')


def change_password2(request):   

    if request.method == 'POST':
        print(request.POST)        
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')
        userchangeid =  request.session['userchange']
        userchange = User.objects.get(id = userchangeid)
        if pw1 != pw2:
            errormessage = "Passwords Does not match !"
            return render(request, 'registration/change_password2.html', {'errormessage' : errormessage})

        else:
            try:
                userchange.set_password(pw1)      
                userchange.save()         
            except:
                errormessage = " oops , error in password change... Contact Admin !"
                return render(request, 'registration/change_password2.html', {'errormessage' : errormessage})
            update_session_auth_hash(request, userchange)  # Important!
            successmessage = "user password changed successfully !! please login to continue"
            return render(request , 'registration/signin.html', {'successmessage' : successmessage})
    else:
        userchangeid =  request.session['userchange']
        userchange = User.objects.get(id = userchangeid)
        return render(request, 'registration/change_password2.html')

def user_profile_update(request):
    
    if request.method == "GET":
        userprofileinst = user_profile.objects.get(user__id = request.user.id)        
        form = user_profile_update_form(instance=userprofileinst)

        context = {
            'form' : form
        }

        return render(request , 'registration/userprofile_update.html' , context)

    if request.method == "POST":
        userprofileinst = user_profile.objects.get(user__id = request.user.id)
        form = user_profile_update_form(request.POST , instance=userprofileinst )

        if(form.is_valid()):
            form.save()
        
        return redirect('homepage:profile')

    

def user_profile_picture_update(request):
    
    if request.method == "GET":
        userprofileinst = user_profile.objects.get(user__id = request.user.id)        
        form = user_profile_picture_update_form(instance=userprofileinst)

        context = {
            'form' : form
        }

        return render(request , 'registration/userprofile_update.html' , context)

    if request.method == "POST":
        print(request.POST , request.FILES)
        userprofileinst = user_profile.objects.get(user__id = request.user.id)
        form = user_profile_picture_update_form(request.POST ,  request.FILES ,instance=userprofileinst )

        if(form.is_valid()):
            form.save(commit=False)
            if 'profile_picture' in request.FILES:
                print('enter')
                form.profile_picture = request.FILES['profile_picture']        
                form.save()
        
        return redirect('homepage:profile')