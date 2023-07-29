from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetConfirmView)
from django.utils.decorators import method_decorator
from django.contrib import auth, messages
from django.contrib.auth import views as django_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from .forms import (
    # ChangePasswordForm,
    LoginForm,
    # NameForm,
    # PasswordResetForm,
    SignupForm,
    PasswordChangeForm,
    # get_address_form,
    # logout_on_password_change,
)
from .models import User

from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomPasswordResetConfirmForm


def send_email(subject, message, recipient_list):
    sender_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender_email, recipient_list)


@method_decorator(login_required, name="dispatch")
class AccountListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'account/account_list.html'
    context_object_name = 'accounts'

    def test_func(self):
        # Проверяем, является ли текущий пользователь админом проекта
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['user'] = self.request.user.username
        # context['site_name'] = 'My Blog Site'
        return context


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('task:tasks')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'account/password_change.html', {'form': form})


def login(request):
    kwargs = {
        "template_name": "account/login.html",
        "authentication_form": LoginForm,
        "next_page": reverse_lazy('task:tasks'),
        }
    return django_views.LoginView.as_view(**kwargs)(request, **kwargs)


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("account:home")


def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")
        user = auth.authenticate(
            request=request,
            username=username, password=password
            )
        if user:
            auth.login(request, user)
        messages.success(request, "User has been created")
        subject = 'Успешная регистрация в сервисе TimePro'
        message = f'Ваш аккаунт {username} успешно зарегистрирован'
        recipient_list = [email]
        send_email(subject, message, recipient_list)

        redirect_url = request.POST.get("next", "task:tasks")
        return redirect(redirect_url)
    ctx = {"form": form}
    return TemplateResponse(request, "account/signup.html", ctx)


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('account:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    success_url = reverse_lazy('account:password_reset_complete')
