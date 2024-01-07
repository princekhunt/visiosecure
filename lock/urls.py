from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.home, name="home"),
    path("auth", views.auth, name="auth"),
    path("register", views.register, name="register"),

    path("slave/api/check", views.check, name="check"),
    path("slave/api/image", views.image, name="image"), #for receiving image


    path("loader", views.loader, name="loader"),
    path("digit_lock", views.digitlock, name="digitlock"),
    path("initiate_unlocking", views.initiate, name="initiate"),
    path("status", views.status, name="status"),
    path("Rstatus", views.Rstatus, name="Rstatus"),


    path("administration", views.administration, name="administration"),
    path("administration/dashboard", views.dashboard, name="dashboard"),
    path("administration/delete", views.delete, name="delete"),
    path("administration/capture/retake", views.retake, name="retake"),

    path("administration/capture/name", views.name, name="name"),
    path("administration/logout", views.logout, name="logout"),


    path("administration/upload", views.upload, name="upload"),
    path("administration/capture", views.capture, name="capture"),
    path("administration/capture/approve", views.approve, name="approve"),


    path("logs", views.logs, name="logs"),





    path("facts", views.facts, name="facts"),
]