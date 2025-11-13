from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.utils import timezone
import random
from django.core.mail import send_mail
# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def facilities(request):
    return render(request, 'facility.html')


def studentlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        data=StudentModel.objects.filter(email=email,password=password,status='Approved').exists()
        if data:
            request.session['email']=email
            request.session['login']='student'
            return redirect('home')
        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('studentlogin')
    return render(request, 'studentlogin.html')

def facultylogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # print(email)
        data=FacultyModel.objects.filter(email=email,password=password,status='Approved').exists()
        if data:
            dd = FacultyModel.objects.get(email=email)
            request.session['fname']=dd.firstname
            request.session['lname']=dd.lastname
            request.session['sub']=dd.designation
            request.session['email']=email
            request.session['login']='faculty'

            return redirect('home')
        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('facultylogin')
    return render(request, 'facultylogin.html')

def adminlogin(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == 'admin@gmail.com' and password == 'admin':
            request.session['email'] =email
            request.session['login']='admin'
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            redirect('adminlogin')
    return render(request, 'adminlogin.html')

def home(request):
    login =  request.session['login']
    workshops = WorkShopModel.objects.all()
    return render(request, 'home.html',{'login':login,'data':workshops})


def studentregister(request):
    login =  request.session['login']
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        gender = request.POST['gender']
        contact = request.POST['phone']
        address = request.POST['address']
       
        dept = request.POST['department']
        rollid = request.POST['id']
        dateofbirth = request.POST['dateofbirth']
        sem = request.POST['semester']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if StudentModel.objects.filter(email=email,rollid=rollid).exists():
                messages.error(request, 'Email or Roll ID are already exists')
                return redirect('studentregister')
            else:
                Student = StudentModel(firstname=firstname, lastname=lastname, 
                                       email=email, gender=gender
                                       , contact=contact, address=address, 
                                        dept=dept, 
                                       rollid=rollid, password=password,
                                       dateofbirth=dateofbirth,sem=sem)
                Student.save()
                
                email_subject = 'Your Register Details'
                email_message = f'Hello {email}\n\nWelcome To Our Website!\n\nHere are your Account Details:\nEmail: {email}\nPassword: {password}\n\nPlease keep this information safe.\n\nBest regards,\nYour Website Team'
                send_mail(email_subject, email_message, 'appcloud887@gmail.com', [email])
                messages.success(request, 'Student Registered Successfully')
                return redirect('studentregister')
        else:
            messages.error(request, 'Password does not match')
            return redirect('studentregister')
    return render(request, 'studentregister.html',{'login':login})

def facultyregister(request):
    login =  request.session['login']
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        gender = request.POST['gender']
        contact = request.POST['contact']
        address = request.POST['address']
        designation = request.POST['designation']
        dept = request.POST['dept']
        empid = request.POST['empid']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if FacultyModel.objects.filter(email=email,empid=empid).exists():
                messages.error(request, 'Email or Emp ID are already exists')
                return redirect('facultyregister')
            else:
                faculty = FacultyModel(firstname=firstname, lastname=lastname, 
                                       email=email, gender=gender
                                       , contact=contact, address=address, 
                                       designation=designation, dept=dept, 
                                       empid=empid, password=password)
                faculty.save()
                
                email_subject = 'Your Register Details'
                email_message = f'Hello {email}\n\nWelcome To Our Website!\n\nHere are your Account Details:\nEmail: {email}\nPassword: {password}\n\nPlease keep this information safe.\n\nBest regards,\nYour Website Team'
                send_mail(email_subject, email_message, 'appcloud887@gmail.com', [email])
                messages.success(request, 'Faculty Registered Successfully')
                return redirect('facultyregister')
        else:
            messages.error(request, 'Password does not match')
            return redirect('facultyregister')

    return render(request, 'facultyregister.html',{'login':login})

def logout(request):
    del request.session['login']
    return redirect('index')





def viewfaculty(request):
    login = request.session.get('login')
    faculty_list = FacultyModel.objects.all()

    # Paginate with 4 records per page
    paginator = Paginator(faculty_list, 4)  # Show 4 records per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)

    return render(request, 'viewfaculty.html', {'login': login, 'page_obj': page_obj})

def removefaculty(request,id):
    data = FacultyModel.objects.filter(id=id)
    data.delete()
    return redirect('viewfaculty')


def updatefaculty(request,id):
    faculty = FacultyModel.objects.get(id=id)
    if request.method == 'POST':
        pass



def viewstudent(request):
    login = request.session.get('login')
    student_list = StudentModel.objects.all()

    # Paginate with 4 records per page
    paginator = Paginator(student_list, 4)  # Show 4 records per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)

    return render(request, 'viewstudents.html', {'login': login, 'page_obj': page_obj})


def removestudent(request,id):
    data = FacultyModel.objects.filter(id=id)
    data.delete()
    return redirect('viewfaculty')


def updatestudentprofile(request):
    email = request.session['email']
    login = request.session['login']
    if request.method == 'POST':
        contact = request.POST['contact']
        address = request.POST['address']
        desc = request.POST['desc']
        profile = request.FILES['file']
        if login == 'student':
            student = StudentModel.objects.get(email=email)
            student.contact = contact
            student.address = address
            student.profile = profile
            student.desc = desc
            student.save()
            return redirect('profile')
        else:
            faculty = FacultyModel.objects.get(email=email)
            faculty.contact = contact
            faculty.address = address
            faculty.profile = profile
            faculty.desc = desc
            faculty.save()
            return redirect('profile')
    return render(request, 'updatestudentprofile.html',{'login':login})


def workshops(request):
    login = request.session['login']
    workshop_list = WorkShopModel.objects.all()
    return render(request, 'workshops.html',{'login':login,'data':workshop_list})

def addworkshop(request):
    login = request.session['login']
    if request.method == 'POST':
        workshopanme =  request.POST['workshopName']
        workshopdate = request.POST['date']
        workshopimage = request.FILES['workshopImage']
        workshopfile = request.FILES['file']
        dept = request.POST['dept'] 
        sem = request.POST['sem']
        WorkShopModel.objects.create(workshopname=workshopanme,workshopdate=workshopdate
                                     ,workshopimage=workshopimage,workshopfiles=workshopfile,
                                     dept=dept,sem=sem).save()
        messages.success(request, 'Workshop Added Successfully!')
        return redirect('addworkshop')
                                

    return render(request, 'addworkshops.html',{'login':login})


def profile(request):
    login = request.session['login']
    email = request.session['email']
    if login == 'student':
        data = StudentModel.objects.filter(email=email)
    else:
        data = FacultyModel.objects.filter(email=email)
    return render(request, 'profile.html',{'login':login,'data':data})


def downloadfile(request,id):
    login = request.session['login']
    data = WorkShopModel.objects.get(id=id)
    file_path = data.workshopfiles.path
        
        # Check if the file exists
    if os.path.exists(file_path):
        # Create a FileResponse to serve the file
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
        return response
    else:
        raise Http404("File does not exist")
    

def updateworkshop(request,id):
    login = request.session['login']
    
    if request.method == 'POST':
        workshopanme =  request.POST['workshopName']
        workshopdate = request.POST['date']
        workshopimage = request.FILES['workshopImage']
        workshopfile = request.FILES['file']
        dept = request.POST['dept'] 
        sem = request.POST['sem']
        data = WorkShopModel.objects.get(id=id)
        data.workshopname = workshopanme
        data.workshopdate = workshopdate
        data.workshopimage = workshopimage
        data.workshopfiles = workshopfile
        data.dept = dept
        data.sem = sem
        data.save()
        messages.success(request, 'Workshop Updated Successfully!')
        return redirect('workshops')
    return render(request, 'updateworkshop.html',{'login':login,'id':id})



def removeworkshop(request,id):
    data = WorkShopModel.objects.filter(id=id)
    data.delete()
    messages.success(request, 'Workshop Removed Successfully!')
    return redirect('workshops')



def attendance(request):
    login = request.session['login']
    if request.method == 'POST':
        date = request.POST['date']
        sem = request.POST['semester']
        dept = request.POST['dept']
        sub = request.session['sub']
        dat= AttendanceModel.objects.filter(date=date,sem=sem,dept=dept,subject=sub).exists()
        if dat:
            messages.success(request, 'Attendance Already Taken!')
            s=1
            data = AttendanceModel.objects.filter(date=date,sem=sem,dept=dept,subject=sub)
            return render(request,'attendance.html',{'login':login,'data':data, 'date':date,'s':s})
        else:
            data = StudentModel.objects.filter(sem=sem,dept=dept)
           
            return render(request,'attendance.html',{'login':login,'data':data,'date':date})
    # data = StudentModel.objects.all()
    return render(request,'attendance.html',{'login':login})



def submitattendance(request):
    if request.method == 'POST':
        date = timezone.now().date()  
        subject = request.session['sub']  
        ffname = request.session['fname']  
        flname = request.session['lname']  
        
        for roll_id, attendance in request.POST.items():
            if roll_id.startswith('attendance_'):
                roll_id = roll_id.replace('attendance_', '')
                
                try:
                    data = StudentModel.objects.get(rollid=roll_id)
                    
                    # Create attendance record
                    AttendanceModel.objects.create(
                        rollid=roll_id,
                        firstname=data.firstname,
                        lastname=data.lastname,  
                        email=data.email,  
                        date=date,
                        gender=data.gender,  
                        dept=data.dept,  
                        sem=data.sem, 
                        contact=data.contact,  
                        subject=subject,
                        attendance=attendance,
                        ffname=ffname,
                        flname=flname,
                    )

                except StudentModel.DoesNotExist:
                    messages.error(request, f'Student with roll ID {roll_id} does not exist.')

        messages.success(request, 'Attendance Posted Successfully!')
        return redirect('attendance')

def myattendance(request):
    login= request.session['login']
    email= request.session['email']
    if request.method == 'POST':
        date = request.POST['date']
        data = AttendanceModel.objects.filter(email=email,date=date)
        return render(request, 'myattendance.html',{'login':login,'data':data, 'date':date})
    return render(request, 'myattendance.html',{'login':login})

def viewattendance(request):
   
    sub = FacultyModel.objects.values('designation').distinct().values_list('designation', flat=True)
    print(sub)
    login= request.session['login']
    email= request.session['email']
    if request.method == 'POST':
        date = request.POST['date']
        subject = request.POST['subject']
        sem = request.POST['semester']
        dept =request.POST['dept']
        data = AttendanceModel.objects.filter(dept=dept,sem=sem,date=date,subject=subject)
        return render(request, 'viewattendance.html',{'login':login,'data':data, 'date':date, 'sub':sub})
    return render(request, 'viewattendance.html', {'login':login, 'sub':sub})



def marks(request):
    # StudentMarksModel.objects.all().delete()
    login= request.session['login']
    # sub = request.session['sub']
    if request.method == 'POST':
        date = timezone.now().date()
        sem = request.POST['semester']
        dept = request.POST['dept']
        sub = request.session['sub']
        data = StudentModel.objects.filter(dept=dept,sem=sem)
        return render(request, 'marks.html',{'login':login,'data':data, 'date':date,'sub':sub})

    return render(request, 'marks.html',{'login':login})


def uploadmarks(request,rollid):
    
    login= request.session['login']
    email= request.session['email']
    faculty = request.session['fname']
    sub = request.session['sub']
    if request.method == 'POST':
        date = timezone.now().date()
        test1 = request.POST['test1']
        test2 = request.POST['test2']
        midterm = request.POST['midterm']
        finalsem = request.POST['finalsem']
        student = StudentModel.objects.get(rollid=rollid)
        if StudentMarksModel.objects.filter(rollid=rollid,subject=sub).exists():
            messages.success(request, f'Marks are already Uploaded for {student.firstname} {student.lastname} in {sub}!')
            return redirect('uploadmarks',rollid)
        else:
            data = StudentMarksModel.objects.create(
                firstname = student.firstname,
                lastname = student.lastname,
                rollid = student.rollid,
                date = date,
                faculty= faculty,
                subject = sub,
                test1=test1,
                test2=test2,
                mid=midterm,
                finalsem=finalsem,
                email = student.email,
                sem = student.sem,
                dept = student.dept
            )
            data.save()
            student.marks='Posted'
            student.save()
            messages.success(request, f'Marks Uploaded Successfully for {student.firstname} {student.lastname}!')
            return redirect('uploadmarks',rollid)

    return render(request,'uploadmarks.html',{'login':login, 'rollid':rollid})

def updatemarks(request,rollid):
    login= request.session['login']
    if request.method == 'POST':
        date = timezone.now().date()
        test1 = request.POST['test1']
        test2 = request.POST['test2']
        midterm = request.POST['midterm']
        finalsem = request.POST['finalsem']
        data = StudentMarksModel.objects.get(rollid=rollid)
        data.test1 = test1
        data.test2 = test2
        data.mid = midterm
        data.finalsem = finalsem
        data.date = date
        data.save()
        messages.success(request, f'Marks are Successfully Updated for {data.firstname} {data.lastname}!')
        return redirect('updatemarks',rollid)
    return render(request, 'updatemarks.html',{'login':login, 'rollid':rollid})


def viewmarks(request):
    login= request.session['login']
    subjects = FacultyModel.objects.values('designation').distinct().values_list('designation', flat=True)
    if request.method == 'POST':
      
        print(subjects)
        sem = request.POST['semester']
        dept = request.POST['dept']
        sub = request.POST['sub']
        student = StudentMarksModel.objects.filter(dept=dept,sem=sem,subject=sub)
        paginator = Paginator(student, 3)  # Show 4 records per page
        page_number = request.GET.get('page')  # Get the current page number
        page_obj = paginator.get_page(page_number)
        return render(request, 'viewstudentmarks.html',{'login':login,'sub':subjects, 'data':student,'subj':sub,'page_obj':page_obj})
    return render(request, 'viewstudentmarks.html',{'login':login, 'sub':subjects, })


def viewstudentmarks(request):
    login = request.session['login']
    email = request.session['email']
    students = FacultyModel.objects.all()
    subjects = []
    for i in students:
        subjects.append(i.designation)
    if request.method == 'POST':
        sem = request.POST['semester']
        dept = request.POST['dept']
        if login == 'admin':
            sub = request.POST['subject']  
        else:
            sub = request.session['sub']
        student = StudentMarksModel.objects.filter(dept=dept,sem=sem,subject=sub)
        paginator = Paginator(student, 4)  # Show 4 records per page
        page_number = request.GET.get('page')  # Get the current page number
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'viewstudentmarks.html',{'login':login,'data':page_obj, 'sub':subjects})
    return render(request, 'viewstudentmarks.html',{'login':login, 'sub':subjects})


def viewmymarks(request):
    login = request.session['login']
    email = request.session['email']
    student = StudentMarksModel.objects.filter(email=email)
    paginator = Paginator(student, 4)  # Show 4 records per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)
    return render(request, 'viewmymarks.html',{'login':login,'data':student,'page_obj':page_obj})



def forgotpassword(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        otp = random.randint(10000,999999)
        if FacultyModel.objects.filter(email=email).exists():
            data = FacultyModel.objects.get(email=email)
            data.otp = otp
            data.save()
        elif StudentModel.objects.filter(email=email).exists():
            data = StudentModel.objects.get(email=email)
            data.otp = otp
            data.save()
       

        email_subject = 'Reset Your Password'
        email_message = f'Hello {email}\n\nWelcome To Our Website!\n\nHere are your Account Details:\nEmail: {email}\nOTP: {otp}\n\nPlease keep this information safe.\n\nBest regards,\nYour Website Team'
        send_mail(email_subject, email_message, 'appcloud887@gmail.com', [email])
        messages.success(request, 'OTP sent Successfully!')
        return redirect('resetpassword')

    return render(request, 'forgotpassword.html')


def resetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(type(otp))
        # data = OfficersModel.objects.get(email=email,otp=int(otp))
        # print(data.firstname)
        if password == confirm_password:
            if FacultyModel.objects.filter(email=email).exists():
                data = FacultyModel.objects.get(email=email)
                if data.otp == int(otp):
                    data.password = password
                    data.save()
                else:
                    messages.error(request, 'Invalid OTP!')
                    return redirect('resetpassword')
            elif StudentModel.objects.filter(email=email).exists():
                data = StudentModel.objects.get(email=email)
                if data.otp == int(otp):
                    data.password = password
                    data.save()
                else:
                    messages.error(request, 'Invalid OTP')
                    return redirect('resetpassword')
       
           
            messages.success(request, 'Password Reset Successfully!')
            return redirect('resetpassword')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('resetpassword')
    return render(request, 'resetpassword.html')