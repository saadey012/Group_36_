from django.shortcuts import render
from django.contrib.auth import authenticate 
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from .decorators import is_user
import json
from core.models import *
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect
# Create your views here.

def logout(request):
    request.session["logged_in"] = False
    return redirect('signin')
def signin(request):
    response_data ={}
    rp = request.POST.get
    print(rp)
    # logout(request)
    if request.POST:
        is_user = False
        try:

            if rp('password'):

                user = WebsiteUser.objects.get(user_id=rp('username'))
                if user.user_password == rp('password'):
                    print(user)
                    is_user = True
            else:
                user = WebsiteUser.objects.get(user_id=rp('username'))
                response_data['user'] = user.user_type
                response_data['user_id'] = user.user_id
                response_data['status'] = 'password'
                if user.user_type != "P":
                # is_user = True
                    return HttpResponse(json.dumps(response_data), content_type='application/json')    
                else:
                    is_user = True
                
            if is_user:
                response_data['user'] = user.user_type
                response_data['password_verified'] = True
                response_data['status'] = "success"
                request.session["logged_in"] = True
                request.session["id"] = user.id
                request.session["user_id"] = user.user_id
                request.session["user_name"] = user.user_name
                request.session["user_last_name"] = user.user_last_name
                request.session["user_address"] = user.user_address
                request.session["user_phone"] = user.user_phone
                request.session["user_status"] = user.user_status
                request.session["user_type"] = user.get_user_type_display()
                request.session["user_type_value"] = user.user_type
                request.session["added"] = str(user.added.strftime('%Y-%m-%d %H:%M'))
                request.session["salary"] = user.salary
                request.session["user_birthday"] = user.user_birthday


                print(response_data)
                return HttpResponse(json.dumps(response_data), content_type='application/json')    
        except:
            response_data['message'] = 'User ID or Password is Wrong Please Try Again'
            response_data['status'] = 'error'
            return HttpResponse(json.dumps(response_data,cls=DjangoJSONEncoder), content_type='application/json')

    return render(request,'common/signin.html')

@is_user
def patients(request):
    rp = request.POST.get
    print(rp , "patients")
    response_data ={}
    if request.POST:
        if rp('type') == "delete":

            user = WebsiteUser.objects.get(id=rp('id')).delete()
            print("deleted")
        if rp('type') == "add":
            try:
                user = WebsiteUser.objects.create(user_id=rp('user_id'),user_name=rp('user_name'),user_last_name=rp('user_last_name'),user_address=rp('user_address'),user_phone=rp('user_phone'),user_status=rp('user_status'),user_type="P",user_password=rp('password'))
                response_data['status'] = "success"

            except:
                response_data['status'] = "failed"
                response_data['message'] = "Patient with Same User Id Exists"

            return HttpResponse(json.dumps(response_data,cls=DjangoJSONEncoder), content_type='application/json')

    c = {"patients":WebsiteUser.objects.filter(user_type="P")}
    print(c)
    return render(request,'common/table.html',c)
@is_user
def doctors(request):
    rp = request.POST.get
    print(rp)
    response_data ={}
    if request.POST:
        if rp('type') == "delete":

            user = WebsiteUser.objects.get(id=rp('id')).delete()
        if rp('type') == "add":
            try:
                user = WebsiteUser.objects.create(salary = rp('salary'),user_birthday=rp('user_birthday'),user_id=rp('user_id'),user_name=rp('user_name'),user_last_name=rp('user_last_name'),user_address=rp('user_address'),user_phone=rp('user_phone'),user_status=rp('user_status'),user_type="D",user_password=rp('password'))
                response_data['status'] = "success"

            except:
                response_data['status'] = "failed"
                response_data['message'] = "Doctor with Same User Id Exists"

            return HttpResponse(json.dumps(response_data,cls=DjangoJSONEncoder), content_type='application/json')

    c = {"doctors":WebsiteUser.objects.filter(user_type="D")}
    
    return render(request,'common/doctors.html',c)


@is_user
def tests(request):
    rp = request.POST.get
    print(rp)
    response_data ={}
    if request.POST:
        if rp('type') == "delete":

            user = Test.objects.get(id=rp('id')).delete()
        if rp('type') == "add":
            try:
                try:
                    if request.session["user_type_value"] == "P":
                        patient = WebsiteUser.objects.get(id=request.session["id"]) 
                    else:
                        patient = WebsiteUser.objects.get(id=rp("patient")) 

                except:
                    patient = WebsiteUser.objects.get(id=rp("patient")) 

                print(patient)
                if patient.tests.filter(test_date=rp('test_date')).count() == 1:
                    print("if")
                    response_data['status'] = "failed"
                    response_data['message'] = "Patient All ready has a test in the selected day"
                else:
                    print("else")

                    test = Test.objects.create(test_id = rp('test_id'),test_number=rp('test_number'),patient=patient,test_date=rp('test_date'),test_type=rp('test_type'))
                    response_data['status'] = "success"

            except:
                response_data['status'] = "failed"
                response_data['message'] = "Test with Same Test Id or Test Number Exists"

            return HttpResponse(json.dumps(response_data,cls=DjangoJSONEncoder), content_type='application/json')
    tests =  Test.objects.filter()
    if request.session["user_type_value"] == "P":
        tests = tests.filter(patient__id=request.session["id"])
    c = {   
        
        "tests":tests,
       "patients": WebsiteUser.objects.filter(user_type="P")
        }
    
    return render(request,'common/tests.html',c)

@is_user
def drugs(request):
    rp = request.POST.get
    print(rp)
    response_data ={}
    if request.POST:
        if rp('type') == "delete":

            user = Drug.objects.get(id=rp('id')).delete()
        if rp('type') == "add":
            try:
                user = Drug.objects.create(drug_name = rp('drug_name'))
                response_data['status'] = "success"

            except:
                response_data['status'] = "failed"
                response_data['message'] = "Doctor with Same User Id Exists"

            return HttpResponse(json.dumps(response_data,cls=DjangoJSONEncoder), content_type='application/json')

    c = {"drugs":Drug.objects.filter()}
    
    return render(request,'common/drugs.html',c)


@is_user
def orders(request):
    rp = request.POST.get
    print(rp,"orders")
    response_data ={}
    if request.POST:
        if rp('type') == "delete":

            user = Order.objects.get(id=rp('id')).delete()
        if rp('type') == "add":
            try:
                user = Order.objects.create(order_id = rp('order_id'),order_name=rp('order_name'),order_description=rp('order_description'),order_amount=rp('order_amount'),order_quantity=rp('order_quantity'),order_price=rp('order_price'))
                response_data['status'] = "success"

            except:
                response_data['status'] = "failed"
                response_data['message'] = "Doctor with Same User Id Exists"

            return HttpResponse(json.dumps(response_data,cls=DjangoJSONEncoder), content_type='application/json')

    c = {"orders":Order.objects.filter()}
    
    return render(request,'common/order.html',c)


@is_user
def profile(request):
    print("profile")
    return render(request,"common/profile.html")
def blank(request):
    return render(request,'common/blank.html',)

@is_user
def work_schedule(request):
    rp = request.POST.get
    print(rp,"work_schedule")
    response_data ={}
    if request.POST:
        if rp('type') == "add":
            ws = WorkSchedule.objects.create(doctor=WebsiteUser.objects.get(id=rp("doctor")),start=rp("start"),end=rp('end'))

        if rp('type') == "edit":
            ws = WorkSchedule.objects.get(id=rp("id"))
            ws.doctor=WebsiteUser.objects.get(id=rp("doctor"))
            ws.start=rp("start")
            ws.end=rp('end')

            ws.save()

        response_data['status'] = "success"
        return HttpResponse(json.dumps(response_data,cls=DjangoJSONEncoder), content_type='application/json')

        
    c = {
        'calendar' : WorkSchedule.objects.all(),
        'doctors': WebsiteUser.objects.filter(user_type="D")
    }
    return render(request,'common/calender.html',c)
@is_user
def mail(request):
    rp = request.POST.get
    print(rp,"work_schedule")
    response_data ={}
    if request.POST:
        if rp('type') == "add":
            m = Mail.objects.create(reciever=WebsiteUser.objects.get(id=rp('user')),sender=WebsiteUser.objects.get(id=request.session["id"]),message=rp('message'))
        if rp('type') == "delete":
            m = Mail.objects.get(id=rp("id")).delete()
        response_data['status'] = "success"
        return HttpResponse(json.dumps(response_data,cls=DjangoJSONEncoder), content_type='application/json')

    c = {
        "mail":Mail.objects.filter(reciever__id=request.session["id"]),
        "user":WebsiteUser.objects.all(),
    }
    return render(request,'common/mail.html',c)
