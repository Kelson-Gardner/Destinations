from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from .models import User, Session, Destination
from django.contrib.auth.hashers import make_password, check_password
import string
import random
 
# Create your views here.

def index(request: HttpRequest):
        destinations = Destination.objects.all()
        public_destinations = destinations.filter(share_publicly=True)
        ordered_destinations = reversed(public_destinations)

        session = request.COOKIES.get("session")
        return render(request, 'core/index.html', {'public_destinations': ordered_destinations, 'session': session})

def destinations(request: HttpRequest):
    if request.method == "POST":
        params = request.POST
        if params.get("place") == "":
            return render(request, "core/new_destination.html", {'place_error': "ERROR: INVALID PLACE"})
        if params.get("review") == "":
            return render(request, "core/new_destination.html", {'review_error': "ERROR: INVALID REVIEW"})

        try:
            if int(params.get("rating")) < 1 or int(params.get("rating")) > 5:
                return render(request, "core/new_destination.html", {'rating_error': "ERROR: INVALID RATING"})
        except Exception as e:
            return render(request, "core/new_destination.html", {'rating_error': "ERROR: INVALID RATING"})
    
        destination = Destination(
            name=params.get("place"),
            review=params.get("review"),
            rating=params.get("rating"),
            share_publicly=params.get("public"),
            user=request.user
        )

        destination.save()

    destinations = Destination.objects.all()
    my_destinations = destinations.filter(user=request.user)
    ordered_destinations = reversed(my_destinations)
    
    return render(request, 'core/destinations.html', {'destinations': ordered_destinations})

def sign_up(request: HttpRequest):
    return render(request, "core/sign_up.html")


def create_user(request: HttpRequest):
    params = request.POST
    
    if params.get("name") == '':
        return render(request, "core/sign_up.html", {"username_error": "ERROR: INVALID USERNAME"})

    if params.get("password_hash") == '':
        return render(request, "core/sign_up.html", {"password_error": "ERROR: INVALID PASSWORD"})
    
    hashed_password = make_password(params.get("password_hash"))

    if User.objects.filter(email=params.get("email")).exists():
        return render(request, "core/sign_up.html", {"email_exists_error": "ERROR: EMAIL ALREADY IN USE"})

    if "@" not in params.get("email"):
        return render(request, "core/sign_up.html", {"email_error": "ERROR: INVALID EMAIL"})
    
    user = User(
        name=params.get("name"),
        email=params.get("email"),
        password_hash=hashed_password
    )

    user.save()
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(30))
    session = Session(
        token=token,
        user=User.objects.get(id=user.id)
    )
    session.save()

    response = HttpResponseRedirect("/destinations")
    response.set_cookie("session", session.token)
    return response



def sign_in(request: HttpRequest):
    return render(request, "core/sign_in.html")



def validate_user(request: HttpRequest):
    params = request.POST

    try:
        user = User.objects.get(email=params.get("email"))
    except Exception as e:
        print("The Email Was Invalid")
        return render(request, "core/sign_in.html", {"email_error": "ERROR: INVALID EMAIL"})
    if not check_password(params.get("password_hash"), user.password_hash):
        print("The password is invalid")
        return render(request, "core/sign_in.html", {"password_error": "ERROR: INVALID PASSWORD"})

    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(30))
    session = Session(
        token=token,
        user=user
    )

    session.save()
    response = HttpResponseRedirect("/destinations")
    response.set_cookie("session", session.token)

    return response


def logout(request: HttpRequest):
    session_token = request.COOKIES["session"]
    session = Session.objects.get(token=session_token)
    session.delete()
    response = HttpResponseRedirect("/")
    response.delete_cookie('session')
    return response

     

def new_destination(request: HttpRequest):
    return render(request, "core/new_destination.html")

def edit_destination(request: HttpRequest, id: int):
    if request.method == "POST":
        params = request.POST
        destination = Destination.objects.get(id=id)


        destination.name = params.get("place")
        destination.review = params.get("review")

        if params.get("place") == "":
            return render(request, "core/edit_destination.html", {'place_error': "ERROR: INVALID PLACE", 'destination': destination})
        if params.get("review") == "":
            return render(request, "core/edit_destination.html", {'review_error': "ERROR: INVALID REVIEW", 'destination': destination})
        try:
            if int(params.get("rating")) < 1 or int(params.get("rating")) > 5:
                return render(request, "core/edit_destination.html", {'rating_error': "ERROR: INVALID RATING", 'destination': destination})
        except Exception as e:
            return render(request, "core/edit_destination.html", {'rating_error': "ERROR: INVALID RATING", 'destination': destination})
        destination.rating = params.get("rating")
        destination.share_publicly = params.get("public")
        destination.save()

        return redirect("/destinations")

    destination = Destination.objects.get(id=id)
    return render(request, "core/edit_destination.html", {'destination': destination})

def delete_destination(request: HttpRequest, id: int):
    destination = Destination.objects.get(id=id)
    destination.delete()
    return redirect("/destinations")

