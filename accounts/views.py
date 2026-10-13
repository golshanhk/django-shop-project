from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout , update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from random import randint

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterform(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            User.objects.create_user(
                username=data['username'],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                password=data["password1"])

            messages.success(request, "register done",'success')

            
            return redirect('home:home')
    
    else:
        
        form = UserRegisterform()
    context = {'form':form}
    return render (request, "accounts/register.html", context)

def user_login(request):
    if request.method == "POST":
        form = UserLoginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
           

            if user is not None:
                login(request, user)
                messages.success(request, "login successful", 'success')
                return redirect("home:home")
            else:
                messages.error(request, "try again,password or username is not correct",'danger')
    else:
        form = UserLoginform()

    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "logout successfully",'success')
    return redirect ("home:home")

@login_required(login_url='accounts:login')
def user_profile(request):
    profile = Profile.objects.get(user_id= request.user.id)
    return render(request,"accounts/profile.html", {'profile':profile})


@login_required(login_url='accounts:login')
def user_update_profile(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"update successfully",'success')
            return redirect ("accounts:profile")
    else:
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.profile)
    context={'user_form':user_form,'profile_form':profile_form}
    return render(request,'accounts/Update.html',context)

def change_password(request):
    if request.method =="POST":
        form =PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,"password change",'success')
            return redirect ('accounts:login')
        else:
            messages.error(request,"your password is not correct",'danger')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'accounts/Change_password.html',{'form':form})

