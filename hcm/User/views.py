from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
from django.conf import settings
from .forms import ( PasswordResetEmailForm, LoginForm)
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

User = get_user_model()

class LoginView(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["ENABLE_GOOGLE_LOGIN"] = settings.ENABLE_GOOGLE_LOGIN
        context["GP_CLIENT_SECRET"] = settings.GP_CLIENT_SECRET
        context["GP_CLIENT_ID"] = settings.GP_CLIENT_ID
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST, request=request)
        if form.is_valid():

            user = User.objects.filter(email=request.POST.get('email')).first()

            if user is not None:
                if user.is_active:
                    user = authenticate(username=request.POST.get(
                        'email'), password=request.POST.get('password'))

                    if user is not None:
                        login(request, user)
                        return HttpResponseRedirect('/')
                    return render(request, "login.html", {
                        "ENABLE_GOOGLE_LOGIN": settings.ENABLE_GOOGLE_LOGIN,
                        "GP_CLIENT_SECRET": settings.GP_CLIENT_SECRET,
                        "GP_CLIENT_ID": settings.GP_CLIENT_ID,
                        "error": True,
                        "message":
                        "Your Email and Password didn't match. \
                        Please try again."
                    })
                return render(request, "login.html", {
                    "ENABLE_GOOGLE_LOGIN": settings.ENABLE_GOOGLE_LOGIN,
                    "GP_CLIENT_SECRET": settings.GP_CLIENT_SECRET,
                    "GP_CLIENT_ID": settings.GP_CLIENT_ID,
                    "error": True,
                    "message":
                    "Your Account is inactive. Please Contact Administrator"
                })
            return render(request, "login.html", {
                "ENABLE_GOOGLE_LOGIN": settings.ENABLE_GOOGLE_LOGIN,
                "GP_CLIENT_SECRET": settings.GP_CLIENT_SECRET,
                "GP_CLIENT_ID": settings.GP_CLIENT_ID,
                "error": True,
                "message":
                "Your Account is not Found. Please Contact Administrator"
            })

        return render(request, "login.html", {
            "ENABLE_GOOGLE_LOGIN": settings.ENABLE_GOOGLE_LOGIN,
            "GP_CLIENT_SECRET": settings.GP_CLIENT_SECRET,
            "GP_CLIENT_ID": settings.GP_CLIENT_ID,
            "form": form
        })


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return redirect("User:user_login")


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')

class PasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    form_class = PasswordResetEmailForm
    email_template_name = 'registration/password_reset_email.html'