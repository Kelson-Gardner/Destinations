from django.http import HttpRequest, HttpResponseRedirect
from .models import User, Session
from django.shortcuts import redirect

def sessions_middleware(next):
      def middleware(req: HttpRequest):
            if req.COOKIES.get("session"):
                  session_token = req.COOKIES.get("session")
                  sessions = Session.objects.all()
                  found_sesh = False
                  for session in sessions:
                        if session.token == session_token:
                              found_sesh = True
                              session_found = session
                  if found_sesh == True:
                        req.user = session_found.user
            else:
                if req.path != "/" and req.path != "/sessions/new/" and req.path != "/users/new/" and req.path != "/sessions/" and req.path != "/users/":
                    return redirect("/")
                else:
                    res = next(req)
                    return res
            res = next(req)
            return res
      return middleware