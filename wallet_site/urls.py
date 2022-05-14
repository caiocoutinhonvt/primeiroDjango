"""wallet_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from myapp.views import  list, create, update, delete,charts,list_category, create_category, update_category, delete_category, limit_month, profile, createprofile, editprofile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # DJANGO ADMIN
    path('admin/', admin.site.urls),

    # TRANSACTIONS 

    path('', list, name='url_list'),
    path('update/<int:id>/', update, name='url_update'),    
    path('delete/<int:id>/', delete, name='url_delete'), 
    path('adicionar/', create , name = 'url_create'),
    path('visaogeral/', charts),
    
    

    #LOGIN USER 
    path('accounts/', include('allauth.urls'), name=''),

    #CATEGORY
    path('categoria/', list_category  , name = 'url_list_category'),
    path('adicionar_categoria/', create_category, name = 'url_create_category'),
    path('update_categoria/<int:id>/', update_category, name='url_update_category'), 
    path('delete_categoria/<int:id>/', delete_category, name='url_delete_category'), 
    path('limit_month/<int:id>/', limit_month, name = 'url_limit_month'),

    # PROFILE 
    path('edit_profile/', editprofile, name="url_profile_view"),
    path('profile/', profile, name="url_profile"),
    path('create_profile/', createprofile, name="url_create_profile")

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)