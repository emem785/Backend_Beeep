from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from main.models import *
from main import views
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.shortcuts import get_object_or_404
import json
import ast
from helpers.http_codes import http_codes
from django.shortcuts import render
# from snippet import helpers


def login_view(request):

    if request.method == 'POST':

        if True:

            email = request.POST.get("email", "")
            username = request.POST.get("username", "").lower()
            email = email.lower()
            password = request.POST.get("password", "")

            try:
                # GET CORRESPONDING USERNAME FROM EMAIL POSTED
                user = authenticate(
                    username=username.lower(), password=password)

                if (user.username == username):  # allows user to login using username
                    # No backend authenticated the credentials

                    user = User.objects.get(username=username)
                    login(request, user)

                    return HttpResponse(json.dumps({"response": "success"}))
            except:
                return HttpResponse(json.dumps({"response": "failure"}))
        else:
            return HttpResponse(json.dumps({"response": "failure"}))

    else:
        return render(request, "login.html")


def login_as_view(request, id):

    # form = LoginForm(request.POST)

    if True:

        # GET CORRESPONDING USERNAME FROM EMAIL POSTED
        customer = Customer.objects.get(id=id)

        user = customer.user
        login(request, user)

        return redirect(views.index)
    else:
        return HttpResponse(json.dumps({"response": "failure"}))


def update_password(request):

    user = User.objects.get(pk=request.user.id)

    if request.method == 'POST':
        # # print(request.POST)
        old = request.POST.get("old")
        new = request.POST.get("new")
        customer_id = request.POST.get("customer_id", False)

        if customer_id == False:

            user = authenticate(username=user.username, password=old)

            if user:
                user.set_password(new)
                user.save()
                login(request, user)

                return HttpResponse(json.dumps({"response": "success"}))
            else:
                return HttpResponse(json.dumps({"response": "failure"}))
        else:
            customer = Customer.objects.get(id=customer_id)

            user = authenticate(username=customer.user.username, password=old)

            if user:
                user.set_password(new)
                user.save()

                return HttpResponse(json.dumps({"response": "success"}))
            else:
                return HttpResponse(json.dumps({"response": "failure"}))


@csrf_exempt
def mobile_signin(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        phone = data["phone"]
        password = data["password"]

        try:
            auth_successful = Token.authenticate(phone, password, request)
            user = Civilian.objects.filter(
                user__username=phone) or Lawyer.objects.filter(user__username=phone)
            main_user = Civilian.objects.filter(
                user__username=phone) or Lawyer.objects.filter(user__username=phone)

            if auth_successful.get("success"):

                auth_token = main_user[0].get_token()

                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "message": f"Authenticated new user",
                        "user_type": main_user[0].__class__.__name__,
                        "details": main_user[0].get_details()
                    },
                    "auth_keys": {"access_token": auth_token
                                  }
                }
                })
                )

                return CORS(resp).allow_all(auth=auth_token, status_code=201)

            elif auth_successful.get("is_not_verified"):

                resp = (json.dumps({"response": {
                    "code": http_codes["Forbidden"],
                    "task_successful": False,
                    "content": {
                        "message": f"{auth_successful.get('message')}. Or Username or Password might be wrong..!!"
                    },
                    "auth_keys": {"access_token": ""}
                }
                })
                )

                return CORS(resp).allow_all(status_code=403)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": f"{auth_successful.get('message')}. Or Username or Password might be wrong..!!"
                    },
                    "auth_keys": {"access_token": ""}
                }
                })
                )

                return CORS(resp).allow_all(status_code=401)

        except SyntaxError:
            resp = HttpResponse(json.dumps({"response": {
                "code": http_codes["Unauthorized"],
                "task_successful": False,
                "content": {
                    "user": "",
                    "message": f"Authentication credentials mismatch"
                },
                "auth_keys": {"access_token": ""}
            }
            }))

            return CORS(resp).allow_all(status_code=http_codes["Unauthorized"]["code"])

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=http_codes["Method Not Allowed"]["code"])


@csrf_exempt
def mobile_register_civilian(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        first_name = data["firstname"]
        last_name = data["lastname"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]
        twitter_handle = data["twitter_handle"] if data["twitter_handle"] != "" else "@"

        if Civilian.objects.filter(phone=phone).exists() or User.objects.filter(username=phone).exists():

            resp = (json.dumps({"response": {"task_successful": False, "content": {
                "code": http_codes["Precondition Failed"], "user": first_name, "message": "phone number may already exist"}, "auth_keys": {"access_token": "NULL"}}}))

            return CORS(resp).allow_all(status_code=http_codes["Precondition Failed"]["code"])

        else:

            civilian = Civilian().create(firstname=first_name, lastname=last_name, phone=phone,
                                         password=password, email=email, twitter_handle=twitter_handle)

            resp = (json.dumps({"response": {
                "code": http_codes["Created"],
                "task_successful": True,
                "content": {
                    "user": civilian.firstname,
                    "message": f"created and authenticated new user - ({civilian.firstname})"
                },
                "auth_keys": {"access_token": civilian.get_token()}
            }
            })
            )

            return CORS(resp).allow_all(status_code=http_codes["Created"]["code"])

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"], "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=http_codes["Method Not Allowed"]["code"])


@csrf_exempt
def mobile_register_lawyer(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        first_name = data["firstname"]
        last_name = data["lastname"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]
        twitter_handle = data["twitter_handle"] if data["twitter_handle"] != "" else "@"

        if Lawyer.objects.filter(phone=phone).exists() or User.objects.filter(username=phone).exists():

            resp = (json.dumps({"response": {"task_successful": False, "content": {
                "code": http_codes["Precondition Failed"], "user": first_name, "message": "phone number may already exist"}, "auth_keys": {"access_token": "NULL"}}}))

            return CORS(resp).allow_all(status_code=http_codes["Precondition Failed"]["code"])

        else:

            lawyer = Lawyer().create(firstname=first_name, lastname=last_name, phone=phone,
                                     password=password, email=email, twitter_handle=twitter_handle)

            resp = (json.dumps({"response": {
                "code": http_codes["Created"],
                "task_successful": True,
                "content": {
                    "user": lawyer.firstname,
                    "message": f"created and authenticated new user - ({lawyer.firstname})"
                },
                "auth_keys": {"access_token": lawyer.get_token()}
            }
            })
            )

            return CORS(resp).allow_all(status_code=http_codes["Created"]["code"])

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"], "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=http_codes["Method Not Allowed"]["code"])


@csrf_exempt
def mobile_verify_code(request):

    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            phone = data["phone"]
            code = data["code"]

        except KeyError:
            resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Bad Request"],                            "content": {
                "user": "", "message": "User account not activated (Bad parameters sent"}, "auth_keys": {"access_token": []}}}))
            return CORS(resp).allow_all(status_code=http_codes["Bad Request"]["code"])

        try:

            users = User.objects.filter(username=phone)

            try:
                if users:
                    user = users[0]
                else:
                    raise Exception("Phone number does not exist error ")

            except Exception:

                resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Not Implemented"],                            "content": {
                    "user": "", "message": "Account details provided do not exist."}, "auth_keys": {"access_token": []}}}))
                return CORS(resp).allow_all(status_code=http_codes["Not Implemented"]["code"])

            is_verified = Activation_Code_Manager(user).verify_code(code)

            if is_verified:

                accounts = Lawyer.objects.filter(
                    user=user) or Civilian.objects.filter(user=user)

                target_account = accounts[0]
                target_account.is_verified = True
                Token(user=target_account.user).add_token(request)
                target_account.save()
                auth_token = target_account.get_token()
                resp = (json.dumps({"response": {"task_successful": is_verified, "code": http_codes["Accepted"],                            "content": {
                    "user": "", "message": "User account activated",
                    "details": target_account.get_details()}, "auth_keys": {"access_token": auth_token}}}))
                return CORS(resp).allow_all(auth=auth_token, status_code=http_codes["Accepted"]["code"])
            else:
                resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Not Implemented"],                            "content": {
                    "user": "", "message": "Account details provided do not exist."}, "auth_keys": {"access_token": []}}}))
                return CORS(resp).allow_all(status_code=http_codes["Not Implemented"]["code"])

        except NameError:
            resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Not Implemented"],                            "content": {
                "user": "", "message": "User account not activated( something went wrong"}, "auth_keys": {"access_token": []}}}))
            return CORS(resp).allow_all(status_code=http_codes["Not Implemented"]["code"])

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                            "content": {
            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=http_codes["Method Not Allowed"]["code"])


@csrf_exempt
def get_verification_code(request, phone):

    try:

        user = User.objects.get(username=phone)
        verification_code = Activation_Code_Manager(user).get_code()

        resp = (json.dumps({"response": {"task_successful": True, "code": http_codes["OK"],                            "content": {
            "verification_code": verification_code, "message": ""}, "auth_keys": {"access_token": []}}}))
        return CORS(resp).allow_all()

    except:

        resp = (json.dumps({"response": {"task_successful": True, "code": http_codes["Not Found"],                            "content": {
            "verification_code": "no code", "message": "Requested user resource not found"}, "auth_keys": {"access_token": []}}}))
        return CORS(resp).allow_all(http_codes["Not Found"]["code"])
