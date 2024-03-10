from django.urls import path
from . import views

urlpatterns = [
    path("v1/recommendations/users/<str:user_id>", views.user_recommendation, name="user_recommendation"),
    path("v1/recommendations", views.popular_recommendation, name="popular_recommendatio")
]