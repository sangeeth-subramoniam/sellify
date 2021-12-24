from django.shortcuts import redirect, render

from registration.models import user_profile
from .forms import User_form , user_profile_form


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.

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
    logout(request)
    return HttpResponseRedirect(reverse("homepage:home"))