import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from student_management_app.forms import AddStudentForm

# from student_management_app.forms import AddStudentForm, EditStudentForm
from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students


def admin_home(request):
    return render(request,"hod_template/home_content.html")

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_course(request):
   
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("method not allowed ")
    else:
        course= request.POST.get("course")
        
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request,"succeful added")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request,"fail to save")
            return HttpResponseRedirect("/add_course")

def add_student(request):
    courses = Courses.objects.all()
    return render(request,"hod_template/add_student_template.html", {"courses":courses})
def add_student(request):
    form=AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        session_start=request.POST.get("session_start")
        session_end=request.POST.get("session_end")
        course_id=request.POST.get("course")
        sex=request.POST.get("sex")
        
        profile_pic = request.FILES['profile_pic']
        fsn = FileSystemStorage()
        filename=fsn.save(profile_pic.name,profile_pic)
        profile_pic_url=fsn.url(filename)
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
            user.students.address=address
            course_obj=Courses.objects.get(id=course_id)
            user.students.course_id=course_obj
            user.students.session_start_year=session_start
            user.students.session_end_year=session_end
            user.students.gender=sex
            user.students.profile_pic=profile_pic_url
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect(reverse("add_student"))
        except:
            messages.error(request,"Failed to Add Student")
            return HttpResponseRedirect(reverse("add_student"))

def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/add_subject_template.html", {"courses":courses, "staffs":staffs}) 

def add_subject_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(" <h2> Method Not Allowed</h2>")
    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
    
        staff_id  = request.POST.get("staff")
        staff= CustomUser.objects.get(id=staff_id)
        
        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()              
            messages.success(request,"Successfully Added subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add subject")
            return HttpResponseRedirect(reverse("add_subject"))
            
            
def manage_staff(request):
    staffs= Staffs.objects.all()
    return render(request, "hod_template/manage_staff_template.html", {"staffs":staffs})
def manage_student(request):
    students = Students.objects.all()
    return render (request, "hod_template/manage_student_template.html", {"students":students,})

def manage_course(request):
    courses = Courses.objects.all()
    return render (request, "hod_template/manage_course_template.html", {"courses":courses,})

def manage_subject(request):
    subjects = Subjects.objects.all()
    return render (request, "hod_template/manage_subject_template.html", {"subjects":subjects,})

def edit_staff (request, staff_id):
    staff= Staffs.objects.get(admin=staff_id)
    return render(request, "hod_template/edit_staff_template.html", {"staff":staff})
def edit_staff_save(request ):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed </h2>")
    else:
        staff_id = request.POST.get("staff_id")
        user_email=request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        adress = request.POST.get("address")
        
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name=first_name 
            user.last_name=last_name 
            user.username=username
            user.email=user_email
            user.save()
            
            newaddres = Staffs.objects.get(admin=staff_id)
            newaddres.address= adress
            newaddres.save()
            messages.success(request,"Successfully edited staff")
            return HttpResponseRedirect("/edit_staff/" + staff_id)
        except:
            messages.success(request,"Successfully edited staff")
            return HttpResponseRedirect("/edit_staff/" + staff_id)
        
def edit_student(request, student_id):
    courses = Courses.objects.all()
    student = Students.objects.get(admin=student_id)
    return render(request, "hod_template/edit_student_template.html", {"student":student,"courses":courses})
def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2> Method not allowed</h2>")
    else:
        student_id= request.POST.get("student_id")
        email =request.POST.get("email") 
        first_name= request.POST.get("first_name")
        last_name =request.POST.get("last_name")
        username =request.POST.get("username")
        Adress= request.POST.get("address")
        course_name =request.POST.get("course") 
        sex= request.POST.get("sex")
        session_start =request.POST.get("session_start")
        session_end =request.POST.get("session_end")
        
        
        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fsn = FileSystemStorage()
            filename=fsn.save(profile_pic.name,profile_pic)
            profile_pic_url=fsn.url(filename)
        else: 
            profile_pic_url= None
        
        
        try:
            user= CustomUser.objects.get(id=student_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()
            
            studentuser = Students.objects.get(admin=student_id)
            studentuser.address=Adress
            studentuser.course_name=course_name
            studentuser.gender=sex
            studentuser.session_start_year=session_start
            studentuser.session_end_year=session_end
            if profile_pic_url != None:
                studentuser.profile_pic=profile_pic_url
            
            course= Courses.objects.get(id=course_name)
            studentuser.course_id=course
            studentuser.save()
            messages.success(request,"Successfully edited student")
            return HttpResponseRedirect("/edit_student/" + student_id)
        except :
            messages.error(request,"Failed edited student")
            return HttpResponseRedirect("/edit_student/" + student_id)
        


def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        suject_id=request.POST.get("subject_id")
        subjectname=request.POST.get("subject_name")
        coursename=request.POST.get("course")
        staffname=request.POST.get("staff")

        try:
            subject=Subjects.objects.get(id=suject_id)
            course = Courses.objects.get(id=coursename)
            staff =CustomUser.objects.get(id=staffname)
            subject.subject_name=subjectname
            subject.staff_id=staff
            subject.course_id=course
            subject.save()
            messages.success(request,"Successfully Edited subject")
            return HttpResponseRedirect("/edit_subject/" + suject_id)
        except:
            messages.error(request,"Failed to Edit subject")
            return HttpResponseRedirect("/edit_subject/" + suject_id)


    pass


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        coursename=request.POST.get("course")

        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=coursename
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect("/edit_course/" + course_id)
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect("/edit_course/" + course_id)

