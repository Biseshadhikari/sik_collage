from django.shortcuts import render,redirect
from core.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import StudentForms
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import PasswordChangingForm
from django.template.loader import render_to_string
# from .forms import CollageForm
@login_required(login_url = 'core:login')
def deletecollage(request,pk):
    if request.user.is_superuser:
        collage = Collage.objects.get(id = pk)
        collage.delete()
        return redirect('core:home')
    return render(request,'core/index.html')
@login_required(login_url = 'core:login')
def student(request,slug):
    if request.user.is_superuser:
        collage = Collage.objects.get(slug = slug)
        students = CollageForm.objects.filter(collage = collage)
        page = request.GET.get('page')
        paginator = Paginator(students,2)
        try:
            students = paginator.page(page)
        except Exception as  PageNotAnInteger:
            students = paginator.page(1)

        except Exception as  EmptyPage:
            collageform = paginator.page(paginator.num_pages)
        return render(request,'core/registeredStudent.html',{'students':students,"page":page})
    return redirect('core:home')
    
@login_required(login_url = 'core:login')
def index(request):
    print(request.user.last_login)
    print(request.user.date_joined)
    # if request.user.last_login == request.user.date_joined:
    #     print(True)
    # else:
    #     print(False)

    # page_obj = None

    if request.user.is_superuser:
        collage = Collage.objects.all()
        p = Paginator(collage, 6)
        page_number = request.GET.get("page",1)
        page_obj = p.get_page(page_number)
        if request.htmx:
            return render(request, 'core/partial/list.html', {'data':page_obj})
    else:
        
        x= Collage.objects.filter(user = request.user).first()
        if x:
            page_obj = Collage.objects.get(user = request.user)
        else:
            page_obj = None
    # print(collage)
    
    return render(request,'core/index.html',{'data':page_obj})
    
def viewStudents(request):
    collage= Collage.objects.filter(user = request.user).first()
    collageform = None
    if collage:
        collageform = CollageForm.objects.filter(collage = collage)
        verification = request.GET.get('status')
        status = 0
        if verification == "verified":
            collageform = CollageForm.objects.filter(collage = collage,is_verified = True)
            
        elif verification == "Not_verified":
            collageform = CollageForm.objects.filter(collage = collage,is_verified = False)
        
        if verification == "verified":
            status = 1
        elif verification == "Not_verified":
            status = 2
        page = request.GET.get('page')
        paginator = Paginator(collageform,10)
        try:
            collageform = paginator.page(page)
        except Exception as  PageNotAnInteger:
            collageform = paginator.page(1)

        except Exception as  EmptyPage:
            collageform = paginator.page(paginator.num_pages)
        

        
    
        return render(request,'core/viewStudents.html',{"students":collageform,'status':status,"page":page})
    return render(request,'core/viewStudents.html',{"students":collageform,})
def register(request):
    if request.user.is_superuser:
        if request.method == "POST":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            cpassword = request.POST.get('confirmpassword')
            print(username,email,password,cpassword)
            context =  {
                "username":username,
                "email":email,


            }
            if User.objects.filter(username = username).first():
                messages.success(request,'Username is taken')
                return redirect('/register')
            if User.objects.filter(email = email).first():
                messages.success(request,'Email is taken')
                return redirect('/register')
            if cpassword!=password:
                messages.success(request,"Passwords didn't match!! Please enter same password")
                return redirect('/register')
            
            user_obj = User.objects.create_user(username = username,email = email,password=password)
            user_obj.save()
        
            return redirect('core:home')
        else:
            return render(request,'core/register.html')
    else:
        return redirect('core:login')
        
        

    
def user_login(request):
    if  not request.user.is_authenticated:
        
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(username = username)
            
           
            # print(username,password)
            user_obj = User.objects.filter(username = username).first()
            if  user_obj is None:
                messages.success(request,'User not found!!! please signin with correct username')
                return redirect('/login')
           
            user = authenticate(username = username,password= password)
            if user is not None:
                if user.last_login:
                    login(request,user)
                    # print(False)
                    return redirect('core:home')
                else:
                    login(request,user)
                    print(True)
                    return redirect('core:change')
            else:
                messages.success(request,'Wrong password')
                return redirect('/login')
            # return redirect('core:home')
            

        return render(request,'core/login.html')
    else:
        return redirect('/')
    
def user_logout(request):
     logout(request)
     return redirect('/login/')
    

def add(request):
    if request.user.is_superuser:
        user = User.objects.all()
        if request.method == 'POST':
            name = request.POST.get('collage')
            address = request.POST.get('address')
            image = request.FILES.get('image')
            username = request.POST.get('username')
            
            if image == None:
                messages.success(request,'Please fill image field') 
                return redirect('/add')
                

            collage = Collage.objects.filter(name = name).first()
            if name == "":
                messages.success(request,'Enter the name of the collage!!!')
            else:
                if collage:
                    messages.success(request,'Collage Already exists')
                else: 
                    x = Collage.objects.create(user = User.objects.get(username = username),name = name,address = address,image = image)
                    collage= Collage.objects.filter(user = request.user).first()
        

                
        return render(request,'core/addCollage.html',{'user':user})
    else:
        return redirect("core:home")

def forms(request,slug):
    
    if request.method == "POST":
        name = request.POST.get('Name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gpa = request.POST.get('gpa')
        faculty= request.POST.get('faculty')
        CollageForm.objects.create(collage = Collage.objects.get(slug = slug),name = name,phone = phone,address = address,gpa = gpa,faculty = faculty)
        


    return render(request,'core/forms.html',{"collage":Collage.objects.filter(slug = slug).first()})




def detailview(request,pk):
    student = CollageForm.objects.get(id = pk)

    form = StudentForms(instance=student)
    if request.method == "POST":
        form = StudentForms(request.POST,instance = student)
        if form.is_valid():
            form.save()
            return redirect('core:viewStudents')
    context = {'form':form}
    return render(request,'core/studentDetail.html',context)

def searchdata(request):
    
    if request.method == "POST":
        
        collage= Collage.objects.filter(user = request.user).first()
        data = request.POST.get('livesearch')
        students = CollageForm.objects.filter(collage = collage, name__icontains = data)
        print(students)
        t = render_to_string('core/partial/search-list.html',{'students':students})

        
        
        return JsonResponse({'data':t})
    return JsonResponse({})

@login_required(login_url = 'core:login')
def change(request):
    # user = User.objects.get(username = request.user.username)
    
    fm = PasswordChangingForm(user = request.user)
    if request.method == 'POST':
        fm = PasswordChangingForm(user = request.user,data = request.POST)
        print(request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            messages.success(request,"Password changed successfully")
            return redirect("core:change")
    

    
    return render(request,'core/change.html',{"form":fm})

def searchcollage(request):
    
    if request.method == "POST":
        
        # collage= Collage.objects.filter(name__icontains = data)
        data = request.POST.get('livesearch')
        collage= Collage.objects.filter(name__icontains = data)
        
        print(collage)
        t = render_to_string('core/partial/collage-list.html',{'data':collage})

        
        
        return JsonResponse({'data':t})
    return JsonResponse({})
@login_required(login_url="core:login")
def changepassword(request):
    fm = PasswordChangingForm(user = request.user)
    if request.method == 'POST':
        fm = PasswordChangingForm(user = request.user,data = request.POST)
        print(request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            messages.success(request,"Password changed successfully")
            return redirect("core:changepassword")
        

    
    return render(request,'core/changepassword.html',{"form":fm})

def updateuser(request,pk):
    user = User.objects.get(id = pk)
    if request.method == 'POST': 
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        user.username = username
        user.email = email
        user.save()
        messages.success(request,"updated successfully")
        return redirect(f"/updateuser/{pk}")
        
    
    return render(request,'core/updateuser.html',{'user':user})



def deleteuser(request,pk):
    user = User.objects.get(id = pk)
    user.delete()
    return redirect('core:viewuser')

def viewuser(request):
    users = User.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(users,10)
    try:
        users = paginator.page(page)
    except Exception as  PageNotAnInteger:
        users = paginator.page(1)

    except Exception as  EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'core/collageuserlist.html',{'users':users})
