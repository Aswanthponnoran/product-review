from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

#Register
def register(request):
    if(request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        e = request.POST['e']
        f = request.POST['f']
        l = request.POST['l']
        if(p==cp):
            u=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
            u.save()
        else:
            return HttpResponse("Password should be same")
        return redirect('books:home')
    return render(request, 'register.html')


#Request
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
def user_login(request):
    if (request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']

        User=authenticate(username=u,password=p)#checks weather the details entered by the user is correct or not
        if User:#if user already exist
            login(request,User)
            return redirect('books:home')
        else:#If user does not exist
            return HttpResponse('Invalid')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('users:login')