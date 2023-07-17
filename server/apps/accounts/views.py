from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.views.generic import TemplateView, FormView
from django.contrib.auth import login
# Create your views here.
from .forms import UserLoginForm, UserSignupForm


class LoginView(DjangoLoginView):
    template_name = 'pages/accounts/registration/login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('assets:assets-list')
        return super().get(request, *args, **kwargs)


class SignupView(FormView):
    template_name = 'pages/accounts/registration/signup.html'
    form_class = UserSignupForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user, 'django.contrib.auth.backends.ModelBackend')
        return response

    def get_success_url(self):
        redirect_to = self.request.GET.get('next', '/')
        return redirect_to
