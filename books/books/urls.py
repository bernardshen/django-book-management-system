"""books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import bookms.views as views

urlpatterns = [
    path('', views.ShowIndex, name='index'),
    path('home/<int:user_id>', views.User_Home, name='home'),
    path('SearchBooks/', views.SearchBooks, name='search_books'),
    path('SearchBooks/<int:book_isbn>', views.Book_Info, name='book_info'),
    path('SignIn/', views.SignIn, name='sign_in'),
    path('SignOut/', views.SignOut, name='sign_out'),
    path('SignUp', views.SignUp, name='sign_up'),
    path('admin/', admin.site.urls, name='admin'),
    path('Borrow/<int:book_isbn>', views.Borrow, name='borrow'),
    path('Renewal/<int:book_isbn>', views.Renewal, name='renewal'),
    path('ReturnBook/<int:book_isbn>', views.ReturnBook, name='return_book'),
]
