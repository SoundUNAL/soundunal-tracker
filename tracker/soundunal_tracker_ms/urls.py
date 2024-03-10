from django.urls import path
from .recommendations import views as recommendationsapi
from .likes import views as likesapi

urlpatterns = [
    path("v1/recommendations/users/<str:user_id>",
         recommendationsapi.user_recommendation, name="user_recommendation"),
    path("v1/recommendations", recommendationsapi.popular_recommendation,
         name="popular_recommendatio"),
    path("v1/interactions/audios/<str:audio_id>/likes",
         likesapi.audio_likes, name="audio_likes"),
    path("v1/interactions/audios/<str:audio_id>/dislikes",
         likesapi.audio_dislikes, name="audio_dislikes")
]
