# from captcha.fields import ReCaptchaField
from django import forms
# from django.conf import settings
from django.contrib.auth import forms as django_forms
# from django.urls import reverse_lazy
# , update_session_auth_hash
# from phonenumbers.phonenumberutil import country_code_for_region

# from ..account import events as account_events
from ..account.models import User
# from ..extensions.manager import get_extensions_manager
# from . import emails
from django.core.exceptions import ValidationError

# class FormWithReCaptcha(forms.BaseForm):
#     def __new__(cls, *args, **kwargs):
#         if settings.RECAPTCHA_PUBLIC_KEY and settings.RECAPTCHA_PRIVATE_KEY:
#             # insert a Google reCaptcha field inside the form
#             # note: label is empty, the reCaptcha is self-explanatory making
#             #       the form simpler for the user.
#             cls.base_fields["_captcha"] = ReCaptchaField(label="")
#         return super(FormWithReCaptcha, cls).__new__(cls)


# def get_address_form(data, country_code, initial=None,
#  instance=None, **kwargs):
#     country_form = AddressMetaForm(data, initial=initial)
#     preview = False
#     if country_form.is_valid():
#         country_code = country_form.cleaned_data["country"]
#         preview = country_form.cleaned_data["preview"]

#     if initial is None and country_code:
#         initial = {}
#     if country_code:
#         initial["phone"] = "+{}".format(country_code_for
# _region(country_code))
#     address_form_class = get_address_form_class(country_code)

#     if not preview and instance is not None:
#         address_form_class = get_address_form_class(instance.country.code)
#         address_form = address_form_class(data, instance=instance, **kwargs)
#     else:
#         initial_address = (
#             initial if not preview else data.dict() if data
# is not
# None else data
#         )
#         address_form = address_form_class(
#             not preview and data or None, initial=initial_address, **kwargs
#         )

#     if hasattr(address_form.fields["country_area"], "choices"):
#         choices = address_form.fields["country_area"].choices
#         choices = [(choice[1], choice[1]) for choice in choices]
#         address_form.fields["country_area"].choices = choices
#     return address_form, preview


# class ChangePasswordForm(django_forms.PasswordChangeForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["new_password1"].user = self.user
#         self.fields["old_password"].widget.attrs["placeholder"] = ""
#         self.fields["new_password1"].widget.attrs["placeholder"] = ""
#         del self.fields["new_password2"]


# def logout_on_password_change(request, user):
#     if update_session_auth_hash is not None and not
# settings.LOGOUT_ON_PASSWORD_CHANGE:
#         update_session_auth_hash(request, user)

class LoginForm(django_forms.AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", max_length=75)

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        if request:
            username = request.GET.get("username")
            if username:
                self.fields["username"].initial = username

# class PasswordUpdateManuallyForm(django_forms.PasswordChangeForm):


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, label="Password"
    )
    email = forms.EmailField(
        label="Email",
        error_messages={
            "unique":
            "Ошибка регистрации. Такая почта уже зарегистрирована в системе."
        },
    )
    username = forms.CharField(
        label="Username",
        error_messages={
            "unique": "Ошибка регистрации. Такой пользователь уже \
                        зарегистрирован в системе."
        },
    )

    class Meta:
        model = User
        fields = ("email", "username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update(
                {"autofocus": ""}
            )

    def save(self, request=None, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
            # account_events.customer_account_created_event(user=user)
            # get_extensions_manager().customer_created(customer=user)
        return user


class PasswordChangeForm(django_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.validators = []

        # Переопределение подсказок для каждого поля
        self.fields['old_password'].help_text = "Введите ваш текущий пароль."
        self.fields['new_password1'].help_text = "Введите ваш новый пароль."
        self.fields['new_password2'].help_text = (
            "Введите новый пароль еще раз для подтверждения."
        )

        self.fields['old_password'].label = "Старый пароль"
        self.fields['new_password1'].label = "Новый пароль"
        self.fields['new_password2'].label = "Подтверждение нового пароля"

    # Удаление встроенных валидаторов
        self.error_messages['password_mismatch'] = (
            "Пароли не совпадают. Пожалуйста, проверьте правильность ввода."
        )

        self.error_messages['password_incorrect'] = (
            "Некорректно введет старый пароль. Пожалуйста, \
                проверьте правильность ввода."
        )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        # password_validation.validate_password(password2, self.user)
        return password2


class CustomPasswordResetConfirmForm(django_forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Здесь вы можете переопределить метки полей.
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтверждение нового пароля'

# class PasswordResetForm(django_forms.PasswordResetForm):
#     """Allow resetting passwords.

#     This subclass overrides sending emails to use templated email.
#     """

#     def get_users(self, email):
#         active_users = User.objects.filter(email__iexact=email,
# is_active=True)
#         return active_users

#     def send_mail(
#         self,
#         subject_template_name,
#         email_template_name,
#         context,
#         from_email,
#         to_email,
#         html_email_template_name=None,
#     ):
#         # Passing the user object to the Celery task throws an
#         # error "'User' is not JSON serializable". Since it's not used in our
#         # template, we remove it from the context.
#         user = context.pop("user")
#         emails.send_user_password_reset_email(to_email, context, user.pk)


# class NameForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ["first_name", "last_name"]
#         labels = {
#             "first_name": pgettext_lazy(
#                 "Customer form: Given name field", "Given name"
#             ),
#             "last_name": pgettext_lazy(
#                 "Customer form: Family name field", "Family name"
#             ),
#         }
