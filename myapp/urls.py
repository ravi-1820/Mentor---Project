"""
URL configuration for myproject project.
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('index/',          views.index,          name='index'),
    path('contact/',        views.contact,        name='contact'),
    path('profile/',        views.profile,        name='profile'),
    path('login/',          views.login,          name='login'),
    path('logout/',         views.logout,         name='logout'),
    path('cpass/',          views.cpass,          name='cpass'),
    path('about/',          views.about,          name='about'),
    path('mabout/',         views.mabout,         name='mabout'),
    path('course-details/', views.course_details, name='course_details'),
    path('courses/',        views.courses,        name='courses'),
    path('events/',         views.events,         name='events'),
    path('pricing/',        views.pricing,        name='pricing'),
    path('starter-page',    views.starter_page,   name='starter_page'),
    path('trainers/',       views.trainers,       name='trainers'),
    path('fpass/',          views.fpass,          name='fpass'),
    path('otp/',            views.otp,            name='otp'),
    path('newpass/',        views.newpass,        name='newpass'),
    path('mindex/',         views.mindex,         name='mindex'),
    path('add/',            views.add,            name='add'),
    path('view/',           views.view,           name='view'),
    path('cdetails/<int:pk>/',  views.cdetails,   name='cdetails'),
    path('edit/<int:pk>',       views.edit,       name='edit'),
    path('delete/<int:pk>',     views.delete,     name='delete'),
    path('cpdetails/<int:pk>/', views.cpdetails,  name='cpdetails'),
    path('addwish/<int:pk>/',   views.addwish,    name='addwish'),
    path('delwish/<int:pk>/',   views.delwish,    name='delwish'),
    path('wishlist/',       views.wishlist,       name='wishlist'),
    path('addcart/<int:pk>',    views.addcart,    name='addcart'),
    path('deletecart/<int:pk>', views.deletecart, name='deletecart'),
    path('cart/',           views.cart,           name='cart'),
    path('success/',        views.success,        name='success'),

    # ── Admin Panel (Manager only) ────────────────────────────
    path('admin_panel/',    views.admin_panel,    name='admin_panel'),
    path('admin_users/',    views.admin_users,    name='admin_users'),
    path('admin_courses/',  views.admin_courses,  name='admin_courses'),
    path('admin_orders/',   views.admin_orders,   name='admin_orders'),
]
