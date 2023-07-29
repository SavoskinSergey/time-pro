from django.urls import path
from django.contrib.auth import views as django_views
from . import views

urlpatterns = [
    path("", views.AccountListView.as_view(), name='home'),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),

    path("password_change/",
         views.password_change_view, name="change_password"),
    path("password_reset/",
         views.CustomPasswordResetView.as_view(),
         name="password_reset"),
    path(
        "password_reset/done/",
        django_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        django_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # url(r"^password/reset/$", views.password_reset, name="reset-password"),
    # url(
    #     r"^password/reset/done/$",
    #     django_views.PasswordResetDoneView.as_view(
    #         template_name="account/password_reset_done.html"
    #     ),
    #     name="reset-password-done",
    # ),
    # url(
    #     r"^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",  # noqa
    #     views.password_reset_confirm,
    #     name="reset-password-confirm",
    # ),
    # url(
    #     r"password/reset/complete/$",
    #     django_views.PasswordResetCompleteView.as_view(  # noqa
    #         template_name="account/password_reset_from_key_done.html"
    #     ),
    #     name="reset-password-complete",
    # ),
    # url(r"^address/(?P<pk>\d+)/edit/$", views.address_edit,
    # name="address-edit"),
    # url(r"^address/(?P<pk>\d+)/delete/$", views.address_delete,
    # name="address-delete"),
    # url(r"^delete/$", views.account_delete, name="delete"),
    # url(
    #     r"^(?P<token>[0-9A-Za-z_\-]+)/delete-confirm/",
    #     views.account_delete_confirm,
    #     name="delete-confirm",
    # ),
]
