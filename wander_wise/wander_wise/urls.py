"""
URL configuration for wander_wise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from Wander import views
#from django.views.generic import TemplateView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'), 
    path('service/', views.service, name='service'), 
    path('appointment/', views.appointment, name='appointment'),
    path('be_a_guide/', views.be_a_guide, name='be_a_guide'),
    path('feature/', views.feature, name='feature'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path( 'contact/', views.contact, name='contact'),
    path( 'visitor/', views.visitor, name='visitor'),
    path( 'guideinterface/', views.guideinterface, name='guideinterface'),
    path( 'exam/', views.exam, name='exam'),
    #path('logout/', views.logout, name='logout'),



    #path('contact.html', TemplateView.as_view(template_name='contact.html'), name='contact'),
]
