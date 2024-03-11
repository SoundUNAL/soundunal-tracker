from django.urls import path
from .recommendations import views as recommendationsapi
from .interactions import views as interactionsapi

urlpatterns = [
    path("v1/recommendations/users/<str:user_id>",
         recommendationsapi.user_recommendation, name="user_recommendation"),
    path("v1/recommendations", recommendationsapi.popular_recommendation,
         name="popular_recommendatio"),
    path("v1/interactions/audios/<str:audio_id>/likes",
         interactionsapi.audio_likes, name="audio_likes"),
    path("v1/interactions/audios/<str:audio_id>/dislikes",
         interactionsapi.audio_dislikes, name="audio_dislikes"),
    path("v1/interactions/likes",
         interactionsapi.user_likes, name="user_likes"),
    path("v1/interactions/audios/<str:audio_id>/reproductions",
         interactionsapi.audio_reproductions, name="audio_reproductions"),
    path("v1/interactions/audios/<str:audio_id>/comments",
         interactionsapi.audio_comments, name="audio_comments"),
    path("v1/interactions/user/<str:user_id>/audios/recent",
         interactionsapi.user_recently_played, name="user_recently_played")
]
