from django.shortcuts import render, redirect
from django.http import HttpResponse
from lock.modules import recognize
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from lock.models import *
import random
import string
from binascii import a2b_base64
import urllib
import os
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.models import User
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
import base64

from cryptography.fernet import Fernet
from .models import access_code

# Encryption Key
enc_key = b'UAI_kOla1b07_Y-Ko7ynnVZ_Mq0cLQFqdDSBIeYugtQ='

def home(request):

    #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)
    return render(request, "index_2.html")
        

def auth(request):

    if request.method == "POST":
        print(request.POST.get("access"))
        access = request.POST.get("access")
        if access_code.objects.filter(code=access).exists() and access_code.objects.get(code=access).active == True:
            code = "2b717bdd84dd1e61"
            code = code.encode('utf-8')
            code = base64.b64encode(code).decode()


            response = HttpResponse("<script>alert('Access Granted!');window.location.href='../';</script>")
            response.set_cookie('access', code, max_age=60*60*24*365*2)
            return response
        else:
            return HttpResponse("<script>alert('Access Denied!');window.location.href='';</script>")
    return render(request, "auth.html")

def register(request):
    #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.method == "POST":
        img = request.POST.get("photo")

        #convert to png
        res = urllib.request.urlopen(img)

        name = request.POST.get("name")

        #generate unique code for photo
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        #rename photo
        with open('unlockers/'+ random_code +'.png', 'wb') as f:
            f.write(res.file.read())

        photo = 'unlockers/'+ random_code +'.png'

        #save photo
        Unlockers.objects.create(name=name, photo_id=random_code, image=photo)

        return HttpResponse("<script>alert('Registered Successfully!');window.location.href='';</script>")


    return render(request, "register.html")

@csrf_exempt
def check(request):

    #check api key
    if request.GET.get('api_key'):
        key = request.GET.get('api_key')
        if key == "O6RrcSH6wO32ldid6mOSfMZGmSSTg9hF":
            if jobs.objects.count() != 0:
                job = jobs.objects.first()
                if job.status == True:
                    jobid = job.jobid
                    JobType = job.job

                    return JsonResponse({"status": True, "jobid": jobid, "job": JobType})
            else:
                return JsonResponse({"status": False})
        else:
            return HttpResponse("Forbidden", status=403)


    return HttpResponse("Forbidden", status=403)


@csrf_exempt
def image(request):

    if request.method == "POST":

        #check api key
        if not request.POST.get('api_key'):
            return HttpResponse("Forbidden", status=403)
        elif request.POST.get('api_key') != "O6RrcSH6wO32ldid6mOSfMZGmSSTg9hF":
            return HttpResponse("Forbidden", status=403)

        jobid = request.POST.get("jobid")
        #get files
        original = request.POST.get("image")
        print("This was encrypted image")
        
        #decrypt the image
        print(original)
        f = Fernet(enc_key)
        original = f.decrypt(original.encode()).decode()

        #base64 decode
        image = a2b_base64(original)

        


        #save image
        with open('/Users/prince/Desktop/fromMaster.jpg', 'wb') as f:
            f.write(image)

        if jobs.objects.get(jobid=jobid).job == 1:
            #Registration Job

            #generate unique code for photo
            random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

            #save photo
            name = jobs.objects.get(jobid=jobid).access_code #on registration job access code represents name
            TRegistration(name=name, photo_id=random_code, image=original).save()

            #delete job
            jobs.objects.get(jobid=jobid).delete()

        elif jobs.objects.get(jobid=jobid).job == 0:

            result = recognize()
            if result != False:
                print(result)

                #delete job
                jobs.objects.get(jobid=jobid).delete()

                #update success
                update = TAccessCodes.objects.get(jobid=jobid)
                update.success = 1
                update.name = result
                update.save()

                All_logs(name=result, success=True).save()

            else:
                #No match
                
                #delete job
                jobs.objects.get(jobid=jobid).delete()

                #update success
                update = TAccessCodes.objects.get(jobid=jobid)
                update.success = 0
                update.save()



                All_logs(name="Unknown", success=False, reason="Facial Verification Failed", image=original).save()

                return JsonResponse({"status": False})

        return JsonResponse({"status": True})



    return JsonResponse({"status": True})



@xframe_options_exempt
def loader(request):
    return render(request, "loader.html")


def digitlock(request):
    #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)
        
    if request.method == "POST":
        (num1, num2, num3, num4, num5, num6) = (request.POST.get("num1"), request.POST.get("num2"), request.POST.get("num3"), request.POST.get("num4"), request.POST.get("num5"), request.POST.get("num6"))
        if num1 == "1" and num2 == "2" and num3 == "3" and num4 == "4" and num5 == "5" and num6 == "6":


            #generate 21 length unicue code

            random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=21))

            #save code
            TAccessCodes(access_code=random_code, active=True).save()
            print(random_code)

            return JsonResponse({"status": 1, "location": "http://localhost:8000/initiate_unlocking?access=" + random_code})
        else:
            All_logs(name="Unknown", success=False, reason="Incorrect Digit Lock").save()
            return JsonResponse({"status": 0})

    return render(request, "digit_lock.html")

def initiate(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.GET.get('access'):
        access_code = request.GET.get('access')
        if TAccessCodes.objects.filter(access_code=access_code).exists():
            if TAccessCodes.objects.get(access_code=access_code).success == 0 or TAccessCodes.objects.get(access_code=access_code).success == 1:
                return render(request, "initiate.html")
            if TAccessCodes.objects.get(access_code=access_code).active == True:

                #add job for unlock

                #generate 11 digit numeric code
                random_code = ''.join(random.choices(string.digits, k=11))

                jobs(job=0, status=True, jobid=random_code, access_code=access_code).save()

                #Add jobid to TAccessCodes
                update = TAccessCodes.objects.get(access_code=access_code)
                update.jobid = random_code
                update.save()

                TAccessCodes.objects.get(access_code=access_code).active = False


                return render(request, "initiate.html")
            else:
                return redirect(digitlock)
        else:
            return redirect(digitlock)
    else:
        return redirect(digitlock)
    


def facts(request):

    #fetch one fact randomly
    fact = RandomFacts.objects.order_by('?').first()

    return JsonResponse({"fact": fact.fact})


def status(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.GET.get('access'):
        access = request.GET.get('access')

        #get job id from TAccesscode foriegn key

        if TAccessCodes.objects.filter(access_code=access).exists():
            record = TAccessCodes.objects.get(access_code=access)
            success = record.success

            if success == 1:
                return JsonResponse({"status": 1, "name": record.name})
            elif success == 0:
                return JsonResponse({"status": 0})
            else:
                return JsonResponse({"status": -1})



def administration(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.user.is_authenticated:
        return redirect(dashboard)

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:

                #login now
                login(request, user)
                
                return JsonResponse({"status": 1, "location": "http://localhost:8000/administration/dashboard"})
            else:
                print("Username match but password is incorrect!")
                return JsonResponse({"status": 0, "message": "Incorrect Password!"})
        else:
            print("user not found")
            return JsonResponse({"status": 0, "message": "User not found!"})


    return render(request, 'administration.html')


def dashboard(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    all = Unlockers.objects.all().order_by('-id')


    return render(request, 'dashboard.html', {"data": all})

def delete(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)
    if request.user.is_authenticated:

        if request.GET.get('id'):
            id = request.GET.get('id')
            Unlockers.objects.get(photo_id=id).delete()
            #delete from storage
            os.remove('unlockers/'+ id +'.png')

            return JsonResponse({"status": 1})
        else:
            return JsonResponse({"status": 0})
    else:
        return HttpResponse("Forbidden", status=403)


def upload(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.method == 'POST':

        name = request.POST.get("name")
        img = request.POST.get('img')
        

        #convert to png
        res = urllib.request.urlopen(img)
        
        #generate unique code for photo
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        #rename photo
        with open('unlockers/'+ random_code +'.png', 'wb') as f:
            f.write(res.file.read())

        photo = 'unlockers/'+ random_code +'.png'

        #save photo
        Unlockers.objects.create(name=name, photo_id=random_code, image=photo)

        return HttpResponse("<script>alert('"+ name +" Registered Successfully!');window.location.href='/administration/dashboard';</script>")


    return render(request, 'upload.html')

def capture(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.user.is_authenticated:

        #generate 11 digit numeric code
        random_code = ''.join(random.choices(string.digits, k=11))

        jobs(job=1, status=True, jobid=random_code).save()


    return render(request, 'capture.html')


def Rstatus(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.user.is_authenticated:
        
        if TRegistration.objects.count() != 0:
            job = TRegistration.objects.first()
            return JsonResponse({"status": 1, "name": job.name, "image": job.image})


        return JsonResponse({"status": -1})
    return JsonResponse({"status": -1})

def approve(request):
        #check access
    import base64
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.user.is_authenticated:

        #Transfer Tregistration to Unlockers

        if TRegistration.objects.count() != 0:
            name = TRegistration.objects.first().name
            photo_id = TRegistration.objects.first().photo_id
            image = TRegistration.objects.first().image

            #convert base64 img to png
            import base64
            image = base64.b64decode(image)

            with open('unlockers/'+ photo_id +'.png', 'wb') as f:
                f.write(image)

            photo = 'unlockers/'+ photo_id +'.png'

            #save photo
            Unlockers.objects.create(name=name, photo_id=photo_id, image=photo)

            #delete from TRegistration
            TRegistration.objects.first().delete()

            return JsonResponse({"status": 1})



    return JsonResponse({"status": 0})


def name(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.user.is_authenticated:

        if request.GET.get('name'):
            name = request.GET.get('name')

            #add in T Registration

            if TRegistration.objects.count() != 0:
                first = TRegistration.objects.first()
                first.name = name

                first.save()

                return JsonResponse({"status": 1, "image": first.image})
            else:
                return JsonResponse({"status": 0})
        else:
            return JsonResponse({"status": 0})


    return JsonResponse({"status": 0})


def logs(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)
    #get reverse order of logs
    all_logs = All_logs.objects.all().order_by('-id')
    for i in all_logs:
        print(i, i.id)

    return render(request, 'logs.html', {"data": all_logs})

def logout(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.user.is_authenticated:
        django_logout(request)
        return redirect(home)

    return redirect(home)

def retake(request):
        #check access
    if not request.COOKIES.get('access'):
        return redirect(auth)
    else:
        access = request.COOKIES.get('access').encode('utf-8')
        access = base64.b64decode(access).decode()
        if access != "2b717bdd84dd1e61":
            return redirect(auth)

    if request.user.is_authenticated:

        if TRegistration.objects.count() != 0:
            TRegistration.objects.first().delete()

            return JsonResponse({"status": 1})

        return JsonResponse({"status": 0})

    return JsonResponse({"status": 0} )