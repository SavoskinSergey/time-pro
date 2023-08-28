from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'questions', api_views.QuestionViewSet)

urlpatterns = [
    re_path(r"^$", views.QuestionListView.as_view(), name='question'),
    path("export_excel", views.export_question, name='export_question'),
    path('api/login', api_views.Login.as_view(), name='login'),
    path('api/', include((router.urls, 'api'))),
    path('question/<int:pk>/',
         views.QuestionDetailView.as_view(),
         name='question_detail'
         ),
    path('question/update/<int:pk>/',
         views.QuestionUpdateView.as_view(),
         name='question_update'
         ),
]
