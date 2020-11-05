from django.urls import path
from . import views
from .views import *


urlpatterns=[
    # авторизация пользователя
    path('register/', register, name='register'),
    # регистрация пользователя
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # url-для тестовой обработки пагинации используя функции
    path('test/', test_pagination, name='test'),
    path('contact',contact,name='contact'),
    # path('', views.index,name='home'),аналог -нижнего path,
    path('',HomeNews.as_view(), name='home'),

    # path('category/<int:category_id>/', views.get_category,name='category'),
    path('category/<int:category_id>/', NewsByCategory.as_view(),
         name='category'),

    # path('news/<int:news_id>/', views.view_news, name='view_news'),
    path('news/<int:pk>/', NewsDeatail.as_view(),
         name='view_news'),
    # path('news/add-news/', views.add_news, name='add_news')
    path('news/add-news/', NewsCreate.as_view(), name='add_news'),
    path('api/', NewsApiView.as_view(),name='api_home'),
    path('api/<int:pk>/', NewsApiDetailView.as_view(), name='api_detail')

]