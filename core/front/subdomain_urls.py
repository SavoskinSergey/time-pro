
# from django.contrib import admin
# from django.urls import path, include, re_path
# from django.conf.urls import url
# from django.contrib.staticfiles.views import serve as serve_static
# from core.account.urls import urlpatterns as account_urls
# from core.employee.urls import urlpatterns as employee_urls
# from core.project.urls import urlpatterns as project_urls

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    path('/', views.landing_index),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
