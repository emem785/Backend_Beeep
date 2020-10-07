from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from helpers.http_codes import http_codes
from django.shortcuts import render
from useraccounts.models import *
from main.models import *
from cors.models import *
import json

# Create your views here.


def index(request):
    return HttpResponse(json.dumps({"response": "success", "message": "Sorry no content here. Maybe download the app."}))


@csrf_exempt
def update_details(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        phone = data.get("phone")

        try:
            auth_successful = Token.verify_token(request)
            print(auth_successful)

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)

                main_user = main_user[0]
                result = main_user.update_details(data)

                if result["status"]:

                    resp = (json.dumps({"response": {
                        "code": http_codes["Created"],
                        "task_successful": True,
                        "content": {
                            "message": result["message"],
                            "user_type": "main_user.__class__.__name__",
                            "details": main_user.get_details()
                        },
                        "auth_keys": {"access_token": main_user.get_token()
                                    }
                    }
                    })
                    )

                    return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)

                else:

                    resp = (json.dumps({"response": {
                        "code": http_codes["Not Modified"],
                        "task_successful": False,
                        "content": {
                            "message": "Input format might be wrong..!!"
                        },
                        "auth_keys": {"access_token": ""}
                    }
                    })
                    )

                    return CORS(resp).allow_all(status_code=401)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
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

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=405)


@csrf_exempt
def add_buddy(request):

    if request.method == 'POST':

        data = json.loads(request.body)

        try:
            auth_successful = Token.verify_token(request)

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)

                main_user = main_user[0]
                result = main_user.add_buddy(data)

                if result["is_added"]:

                    resp = (json.dumps({"response": {
                        "code": http_codes["Created"],
                        "task_successful": True,
                        "content": {
                            "message": "Added",
                            "user_type": "",
                            "details": result["details"]
                        },
                        "auth_keys": {"access_token": main_user.get_token()
                                    }
                    }
                    })
                    )

                    return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)

                else:

                    resp = (json.dumps({"response": {
                        "code": http_codes["Not Modified"],
                        "task_successful": False,
                        "content": {
                            "message": "Input format might be wrong..!!"
                        },
                        "auth_keys": {"access_token": ""}
                    }
                    })
                    )

                    return CORS(resp).allow_all(status_code=401)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
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

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=405)


@csrf_exempt
def add_location(request):

    if request.method == 'POST':

        data = json.loads(request.body)

        try:
            auth_successful = Token.verify_token(request)

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)

                main_user = main_user[0]
                result = main_user.add_location(data)

                if result:

                    resp = (json.dumps({"response": {
                        "code": http_codes["Created"],
                        "task_successful": True,
                        "content": {
                            "message": "Added",
                            "user_type": "main_user.__class__.__name__",
                            "details": "user_data"
                        },
                        "auth_keys": {"access_token": main_user.get_token()
                                    }
                    }
                    })
                    )

                    return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)

                else:

                    resp = (json.dumps({"response": {
                        "code": http_codes["Not Modified"],
                        "task_successful": False,
                        "content": {
                            "message": "Input format might be wrong..!!"
                        },
                        "auth_keys": {"access_token": ""}
                    }
                    })
                    )

                    return CORS(resp).allow_all(status_code=401)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
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

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=405)


@csrf_exempt
def get_details(request):

    if request.method == 'GET':
        print(request.META)

        try:
            auth_successful = Token.verify_token(request)

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)
                # print(main_user.get_token())

                main_user = main_user[0]
                user_data = main_user.get_details()

                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "details": user_data,
                        "user_type": main_user.__class__.__name__,
                    },
                    "auth_keys": {"access_token": main_user.get_token()
                                }
                }
                })
                )

                return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
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

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=405)


@csrf_exempt
def get_civilian_plans(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        phone = data.get("phone")
        plan = data.get("plan")

        try:
            auth_successful = Token.verify_token(request)
            user = Civilian.objects.filter(
                user__username=phone)
            main_user = Civilian.objects.filter(
                user__username=phone)

            plans = Plan.objects.get(type_of_user="civilian")

            if auth_successful:

                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "message": f"Authenticated new user",
                        "user_type": "main_user.__class__.__name__",
                        "details": "user_data"
                    },
                    "auth_keys": {"access_token": main_user[0].get_token()
                                  }
                }
                })
                )

                return CORS(resp).allow_all(auth=main_user[0].get_token(), status_code=201)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
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

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=405)


@csrf_exempt
def set_plan_civilian(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        phone = data.get("phone")
        plan = data.get("plan")

        try:
            auth_successful = Token.verify_token(request)
            user = Civilian.objects.filter(
                user__username=phone)
            main_user = Civilian.objects.filter(
                user__username=phone)

            if auth_successful:

                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "message": f"Authenticated new user",
                        "user_type": "main_user.__class__.__name__",
                        "details": "user_data"
                    },
                    "auth_keys": {"access_token": main_user[0].get_token()
                                  }
                }
                })
                )

                return CORS(resp).allow_all(auth=main_user[0].get_token(), status_code=201)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
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

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=405)


@csrf_exempt
def get_all_plans(request):

    if request.method == 'GET':

        try:
            auth_successful = Token.verify_token(request)

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)
                # print(main_user.get_token())

                main_user = main_user[0]
                plans = Plan.get_all_plans()

                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "details": plans,
                        "user_type": main_user.__class__.__name__,
                    },
                    "auth_keys": {"access_token": "IN HEADERS"
                                }
                }
                })
                )

                return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
                    },
                    "auth_keys": {"access_token": "IN HEADERS"}
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
                "auth_keys": {"access_token": "IN HEADERS"}
            }
            }))

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": "IN HEADERS"}}}))

        return CORS(resp).allow_all(status_code=405)


@csrf_exempt
def ping_lawyer(request):

    if request.method == 'POST':

        try:
            auth_successful = Token.verify_token(request)

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)
                # print(main_user.get_token())
                main_user = main_user[0]
                notification = Beeep.send_notification_to_lawyer(
                    main_user, request)

                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "details": notification,
                        "user_type": main_user.__class__.__name__,
                    },
                    "auth_keys": {"access_token": "IN HEADERS"
                                }
                }
                })
                )

                return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
                    },
                    "auth_keys": {"access_token": "IN HEADERS"}
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
                "auth_keys": {"access_token": "IN HEADERS"}
            }
            }))

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": "IN HEADERS"}}}))

        return CORS(resp).allow_all(status_code=405)


@csrf_exempt
def get_closest_lawyers(request):

    if request.method == 'GET':

        try:
            auth_successful = Token.verify_token(request)

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)
                # print(main_user.get_token())

                main_user = main_user[0]
                closest_lawyers = Lawyer.get_closest(main_user)

                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "details": closest_lawyers,
                        "distance_unit": "km",
                        "user_type": main_user.__class__.__name__,
                    },
                    "auth_keys": {"access_token": "IN HEADERS"
                                }
                }
                })
                )

                return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
                    },
                    "auth_keys": {"access_token": "IN HEADERS"}
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
                "auth_keys": {"access_token": "IN HEADERS"}
            }
            }))

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": "IN HEADERS"}}}))

        return CORS(resp).allow_all(status_code=405)


@csrf_exempt
def get_closest_lawyers_to_user(request, phone):

    if request.method == 'GET':

        try:
            auth_successful = Token.verify_token(request)

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)
                # print(main_user.get_token())

                main_user = main_user[0]
                target_user = Civilian.objects.get(phone=phone)
                closest_lawyers = Lawyer.get_closest(target_user)

                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "details": closest_lawyers,
                        "distance_unit": "km",
                        "user_type": target_user.__class__.__name__,
                    },
                    "auth_keys": {"access_token": "IN HEADERS"
                                }
                }
                })
                )

                return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
                    },
                    "auth_keys": {"access_token": "IN HEADERS"}
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
                "auth_keys": {"access_token": "IN HEADERS"}
            }
            }))
            return CORS(resp).allow_all(status_code=401)
        except Civilian.DoesNotExist:
            resp = HttpResponse(json.dumps({"response": {
                "code": http_codes["Not Found"],
                "task_successful": False,
                "content": {
                    "user": "",
                    "message": f"User does not exist"
                },
                "auth_keys": {"access_token": "IN HEADERS"}
            }
            }))

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": "IN HEADERS"}}}))

        return CORS(resp).allow_all(status_code=405)
@csrf_exempt
def get_user_location(request, phone):

    if request.method == 'GET':

        try:
            auth_successful = Token.verify_token(request)
            

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)
                # print(main_user.get_token())

                main_user = main_user[0]
                user_data = main_user.get_details()

                target_civilian_location = Civilian.objects.get(phone = phone).get_location()


                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "details": {
                            "target_user_location":target_civilian_location
                            },
                        "user_type": main_user.__class__.__name__,
                    },
                    "auth_keys": {"access_token": main_user.get_token()
                                }
                }
                })
                )

                return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)


            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
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

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=405)



def get_all_beeps(request):

    if request.method == 'GET':

        try:
            auth_successful = Token.verify_token(request)
            

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)
                # print(main_user.get_token())

                main_user = main_user[0]
                user_data = main_user.get_details()

                target_civilian_beeeps = main_user.get_all_beeeps()


                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "details": {
                            "target_user_beeeps":target_civilian_beeeps
                            },
                        "user_type": main_user.__class__.__name__,
                    },
                    "auth_keys": {"access_token": main_user.get_token()
                                }
                }
                })
                )

                return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)


            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
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

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=405)

    print(Civilian.objects.all()[0].get_all_beeeps())


@csrf_exempt
def start_or_stop_beeep(request):

    if request.method == 'POST':

        auth_successful = Token.verify_token(request)
        
        try:

            if auth_successful:

                user = auth_successful["user"]

                main_user = Civilian.objects.filter(
                    user=user) or Lawyer.objects.filter(user=user)

                main_user = main_user[0]

                beeep_start_response = Beeep.handle_beeep(main_user, request)

                

                
                resp = (json.dumps({"response": {
                    "code": http_codes["Created"],
                    "task_successful": True,
                    "content": {
                        "message": f"Authenticated new user",
                        "user_type": "main_user.__class__.__name__",
                        "details": beeep_start_response
                    },
                    "auth_keys": {"access_token": main_user.get_token()
                                  }
                }
                })
                )

                return CORS(resp).allow_all(auth=main_user.get_token(), status_code=201)

            else:

                resp = (json.dumps({"response": {
                    "code": http_codes["Unauthorized"],
                    "task_successful": False,
                    "content": {
                        "message": "Username or Password might be wrong..!!"
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

            return CORS(resp).allow_all(status_code=401)

    else:
        resp = (json.dumps({"response": {"task_successful": False, "code": http_codes["Method Not Allowed"],                    "content": {
                            "user": "", "message": "bad request method"}, "auth_keys": {"access_token": ""}}}))

        return CORS(resp).allow_all(status_code=405)











@csrf_exempt
def post_court_rep_form(request):

    if request.method == 'POST':

        data = request.POST
        file = request.FILES

        try:
            access_token = data["access_token"]
            email = data.get("email")
            useraccount = UserAccount.objects.get(email=email)
            user = useraccount.user
        except:
            resp = HttpResponse(json.dumps(
                {"response": "error", "message": f"invalid user -."}))
            resp = CORS.allow_all(resp)
            return resp

        if useraccount.verify_token(access_token):

            date = data.get("date", "null")
            name = data.get("name", "null")
            case_name = data.get("case_name", "null")
            suit_no = data.get("suit_no", "null")
            court_name = data.get("court_name", "null")
            court_no = data.get("court_no", "null")
            allegation = data.get("allegation", "null")
            name_of_accused = data.get("name_of_accused", "null")
            released_on_bail = data.get("released_on_bail", False)
            bail_conditions = data.get("bail_conditions", "null")
            adjourned_date = data.get("adjourned_date", "null")
            additional_comment = data.get("additional_comment", "null")
            relative_showed_up = data.get("relative_showed_up", False)
            cause_list = file.get("cause_list")

            new_form = Court_Representation_Form(user=user, useraccount=useraccount, date=date, name=name, case_name=case_name, suit_no=suit_no, court_name=court_name, court_no=court_no, allegation=allegation, name_of_accused=name_of_accused,
                                                 released_on_bail=released_on_bail, bail_conditions=bail_conditions, adjourned_date=adjourned_date, additional_comment=additional_comment, relative_showed_up=relative_showed_up, cause_list=cause_list)

            new_form.save()

            resp = HttpResponse(json.dumps(
                {"response": "success", "message": f"Added CR-Form  ({case_name} with allegation of {allegation} to {useraccount.last_name} {useraccount.first_name}'s lists)."}))
            resp = CORS.allow_all(resp)
            return resp

        else:
            resp = HttpResponse(json.dumps(
                {"response": "failure", "message": f"CR-Form not added (invalid access token)"}))
            resp = CORS.allow_all(resp)
            return resp
    else:
        resp = HttpResponse(json.dumps(
            {"response": "failure", "message": f"CR-Form not added (invalid request type)"}))
        resp = CORS.allow_all(resp)
        return resp


@csrf_exempt
def post_credentials_form(request):

    if request.method == 'POST':

        data = request.POST
        file = request.FILES

        try:
            access_token = data["access_token"]
            email = data.get("email")
            useraccount = UserAccount.objects.get(email=email)
            user = useraccount.user
        except:
            resp = HttpResponse(json.dumps(
                {"response": "error", "message": f"invalid user -{email}."}))
            resp = CORS.allow_all(resp)
            return resp

        if useraccount.verify_token(access_token):

            year_of_call = data.get("year_of_call", "null")
            call_to_bar_cert = file.get("call_to_bar_cert")
            undergraduate_cert = file.get("undergraduate_cert")
            cv = file.get("cv")
            nba_seal_stamp = file.get("nba_seal_stamp")
            can_attend_proceedings_regularly = data.get(
                "can_attend_proceedings_regularly", "False")
            weekly_availability_frequency = data.get(
                "weekly_availability_frequency", 9999)
            has_criminal_litigation_experience = data.get(
                "has_criminal_litigation_experience", "False")
            has_police_confrontation_experience = data.get(
                "has_police_confrontation_experience", "False")

            useraccount.year_of_call = year_of_call
            useraccount.call_to_bar_cert = call_to_bar_cert
            useraccount.undergraduate_cert = undergraduate_cert
            useraccount.cv = cv
            useraccount.nba_seal_stamp = nba_seal_stamp
            useraccount.can_attend_proceedings_regularly = can_attend_proceedings_regularly
            useraccount.weekly_availability_frequency = weekly_availability_frequency
            useraccount.has_criminal_litigation_experience = has_criminal_litigation_experience
            useraccount.has_police_confrontation_experience = has_police_confrontation_experience

            useraccount.save()

            resp = HttpResponse(json.dumps(
                {"response": "success", "message": f"Added Credentials for {useraccount.last_name} {useraccount.first_name})."}))
            resp = CORS.allow_all(resp)
            return resp

        else:
            resp = HttpResponse(json.dumps(
                {"response": "failure", "message": f"Credentials not added (invalid access token)"}))
            resp = CORS.allow_all(resp)
            return resp


@csrf_exempt
def get_all_users(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        # print(data)

        access_token = data["auth_keys"]["access_token"]
        email = data.get("email")
        useraccount = UserAccount.objects.get(email=email)
        user = useraccount.user

        if useraccount.verify_token(access_token):
            all_users_query = UserAccount.objects.all()

            all_users = [{"first_name": useraccount.first_name, "last_name": useraccount.last_name, "email": user.email,
                          "phone": useraccount.phone, "address": useraccount.address} for user in all_users_query]

            resp = HttpResponse(json.dumps(
                {"response": "success", "message": {"users": all_users}}))
            resp = CORS.allow_all(resp)
            return resp

        else:
            resp = HttpResponse(json.dumps(
                {"response": "failure", "message": f"Unable to fetch (invalid access token)"}))
            resp = CORS.allow_all(resp)
            return resp


@csrf_exempt
def get_all_forms(request):

    try:

        if request.method == 'POST':

            data = json.loads(request.body)
            # print(data)

            access_token = data["auth_keys"]["access_token"]
            email = data.get("email")
            useraccount = UserAccount.objects.get(email=email)

            if useraccount.verify_token(access_token):
                all_forms = useraccount.get_all_forms()

                resp = HttpResponse(json.dumps({"response": "success", "message": {
                                    "user": f"{useraccount.last_name}, {useraccount.first_name}", "forms": all_forms}}))
                resp = CORS.allow_all(resp)
                return resp

            else:
                resp = HttpResponse(json.dumps(
                    {"response": "failure", "message": f"Unable to fetch (invalid access token)"}))
                resp = CORS.allow_all(resp)
                return resp
        else:
            resp = HttpResponse(json.dumps(
                {"response": "failure", "message": f"Bad request(endpoint expects post), or Unable to fetch (invalid access token)"}))
            resp = CORS.allow_all(resp)
            return resp

    except:
        resp = HttpResponse(json.dumps(
            {"response": "failure", "message": f"Bad request(endpoint expects post), or Unable to fetch (invalid access token)"}))
        resp = CORS.allow_all(resp)
        return resp


# def simple_upload(request):

#         # # print(type(request.FILES.get("file")))
#         file = request.FILES.get("file")
#         doc = Document(document = file)
#         doc.save()
#         if request.method == 'POST':
#                 # # print(request.POST)
#                 return HttpResponse(json.dumps({"response": "success", "message": doc.document.url}))

#         return render(request, 'upload.html')
