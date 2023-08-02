from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from record_api.models import record
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


from django.shortcuts import render
def loginpage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect("list")
        
        else:
            messages.success(request,("There Was An Error Logging In,Try Again...."))

    return render(request,'loginpage.html')

def logout_user(request):
    logout(request)
    print('hello')
    messages.success(request,("You Were Successfully logout"))
    return redirect('login')


def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        print(username)
        if password1!=password2:
            return HttpResponse("Your password and confirm password are not same")
        else:
            data=User.objects.create_user(username=username,email=email,password=password1)
            data.save()
            return redirect('login')
    
    return render(request,'signup.html')


@login_required(login_url="/login/")
def list(request):
    current_user=request.user
    user_id=current_user.id
    print(user_id)
    if User.is_authenticated:
        data=User.objects.get(id=user_id)
        data1=record.objects.filter(user=data)
        return render(request,'record_list.html',{'data1':data1})
    else:
        return redirect('login')

def update_record(request,id):
    queryset=record.objects.get(id=id)
    if request.method=="POST":
        data=request.POST

        title=request.POST['title']
        description=request.POST['description']
          
        queryset.title=title
        queryset.description=description
        queryset.save()
        return redirect('/list/')

    context={
        'record':queryset
    }
    return render(request,'edit_record.html',context)


# this function is created for deleting the record from database 
def delete_record(request,id):
    queryset=record.objects.get(id=id)
    queryset.delete()
    return redirect('/list/')


# this function is created for adding the record in database 
def add_record(request):
    current_user=request.user
    user_id=current_user.id
    if request.method=="POST":
        data=request.POST

        title=request.POST['title']
        description=request.POST['description']
        data=record.objects.create(title=title,description=description,user_id=user_id)
        data.save()
        return redirect('/list/')

    return render(request,'add_record.html')

