from django.shortcuts import render,redirect, HttpResponseRedirect,get_object_or_404
from .models import Blogmodel,Message,Profile
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView


from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import Blogdetails, BlogForm,UserForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import PasswordResetForm


import os
# Create your views here.

def searchBlog(request):
    
     
     if request.method == "GET":
       searched = request.GET.get('searched')
       user_prof = Profile.objects.get(Profileowner = request.user.id)

       
       Blog = Blogmodel.objects.filter(Q(title__icontains = searched) | Q(description__icontains=searched) )
       if searched:
        return render(request,'search.html',{'blog_value':Blog,'searched':searched,'userprofile':user_prof})
       
        

     return render(request,'search.html',{'userprofile':user_prof})

def Home(request):
    
    
        blogs= Blogmodel.objects.all().order_by('-id')
 
        p = Paginator(blogs,2)
        page_number = request.GET.get('page')

      
        page_obj = p.get_page(page_number)
        try:
            user_prof = Profile.objects.get(Profileowner = request.user.id)
            return render(request,"Home.html",{'blog_value':page_obj,'userprofile':user_prof})

        except:  return render(request,"Home.html",{'blog_value':page_obj
                                            })
def Details(request, id):
    
    list = Blogmodel.objects.get(id=id)
    user_prof = Profile.objects.get(Profileowner = request.user.id)

    blog_message= list.message_set.all()
    blog_message.order_by('id')
    if request.method=="POST":
        message=Message.objects.create(
            user= request.user,
            blog= list,
            body= request.POST.get('body')
        )
       
      
        return redirect('details',id= list.id)
    return render(request,'Details.html',{
        'details':list,'blog':blog_message,
        'userprofile':user_prof,
       
        
   })
    
    

    
def User_login( request):
   page= 'login'
  
   if request.user.is_authenticated:
        return redirect('home')

   if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    
    
   context = {'page': page}
   return render(request, 'User_login.html', context)
@login_required(login_url='login')
def CreateBlog(request):

 form = BlogForm()
 user_prof = Profile.objects.get(Profileowner = request.user.id)
   
 if request.method=="POST":
     Blogmodel.objects.create(
            User_ID=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            BlogIm = request.FILES['BlogIm'],
        )
     return redirect('home')
    
    
    
 context={
    'form':form,
    'userprofile':user_prof
   }
 return render(request, 'Createblog.html',context)     
def user_logout(request):
    
       logout(request)
       return redirect('home')
def Register(request):
    form = UserCreationForm()
  
    if request.method == 'POST':
                      
     password1 = request.POST.get('password1')
     
     password2 = request.POST.get('password2')
     usernme = request.POST.get('username')       
     if password1 != password2:
      messages.error(request,"Password doesn't match")

      return redirect('register')
     elif User.objects.filter(username = usernme).exists():
        messages.info(request, "Username Already taken ,please use another one!")
        return redirect('register')
     else:   
   
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
          
            use_profile = User.objects.get(username = usernme)
            Newprofile = Profile.objects.create(Profileowner = use_profile,
                                      
                 
            )
            Newprofile.save()
           
           


             
            
            
            login(request, user)
            return redirect('home')
    else: 
        return render(request, 'Register.html', {'form': form})
@login_required(login_url='login')
def Update_blog(request,id):
   
    blogupdate= Blogmodel.objects.get(id=id)
    user_prof = Profile.objects.get(Profileowner = request.user.id)

    Notath="auth"
    if request.user != blogupdate.User_ID:
        Notath="NA"
    if request.method == 'POST':
        if request.FILES:
     
          blogupdate.BlogIm = request.FILES['image']
        blogupdate.title = request.POST.get('title')
        blogupdate.description = request.POST.get('Description')
        blogupdate.save()
   
    context = {'form': blogupdate,'Notath':Notath ,'userprofile':user_prof}
    return render(request, 'blog_update.html', context)

@login_required(login_url='login')
def DeletBlog( request,id):
      blogdele= Blogmodel.objects.get(id=id)
   
      blogdele.delete()
      return redirect('home')  
@login_required(login_url='login') 
def User_profile(request,username):
      
    if  username == request.user.username:
       
        user_prof = User.objects.get(username = username)
        profile = Profile.objects.get(Profileowner = user_prof)
        user_profile = Profile.objects.get(Profileowner = request.user.id)

                
                #if user_prof.username != request.user   :
                #  authenticated = "auth"
                # else:
                #    authenticated = "Nauth"
        if request.method == "POST":
                
            
            update_user = request.POST.get('username')
            print(update_user)
            Bio = request.POST.get('bio')
            user_prof.username = update_user
            profile.Bio = Bio

        #  Profile.Image =Image
            user_prof.save()
            profile.save()
            if request.FILES:
                profile.Image = request.FILES['image']
                profile.save()
                return redirect('home')
                
        else:

            return render(request, 'Userprofile.html',{
                    
                    'form':user_prof,
                    "profile":profile,
                    'userprofile':user_profile 
                    
                })
    else:   
        return redirect('home')      



        
    return render(request, 'Userprofile.html',{
              
              'form':user_prof,
              "profile":profile,
             
          })

@login_required(login_url='login') 
def delete_message(request,id):
        blog_list= Message.objects.get(id=id)
        blog= blog_list.blog.id

        blog_list.delete()
        return HttpResponse("")
@login_required(login_url='login') 
def Updatemesags( request,id):
    comment = Message.objects.get(id=id)
    user_prof = Profile.objects.get(Profileowner = request.user.id)

   
    if request.method == "POST":
        
        newcomm = request.POST.get('msg')
        
        comment.body = newcomm
        
        comment.save()
        return redirect('details',comment.blog.id)
    return render(request, 'updatemessage.html',{
        
        'mesgb':comment.body,
        'userprofile':user_prof,
    }) 
@login_required(login_url='login') 
def BlogLike(request,id) :
     blog_P = Blogmodel.objects.get(id=id)
     if request.user.is_authenticated:
      if blog_P.Likes.filter(id=request.user.id):
         blog_P.Likes.remove(request.user)
      else:
         blog_P.Likes.add(request.user)  
      
       
         blog_P.save()
         
      return redirect('home')
     else: 
          messages.success(request,"You need to login")
          return redirect(request, 'Home.html')
def SendEmail(request):

     if request.method == "POST":
         subject = request.POST.get('email')
         message =  request.POST.get('body')
         fromk_email= f"{request.POST.get('email')}"
         recipient_list = ['wondimagegnatr96@gmail.com' ] # Or use DEFAULT_FROM_EMAIL from settings
         try:
           send_mail(subject, message, fromk_email, recipient_list)

           return render(request,'EmailSender.html',{'send':message })
         
         except Exception as e:
           return HttpResponse(f'Email sending failed: {e}')
     return render(request,'EmailSender.html',{'send':'Nooting' })

  
    