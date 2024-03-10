from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
#from recommendations.response import Recommendation 
from rest_framework.response import Response
from rest_framework import status


#from recommendations.serializers import RecommendationSerializer
from .recommendations.serializers import RecommendationSerializer
from .recommendations.response import Recommendation

from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def user_recommendation(request, user_id):
    if(not user_id.isnumeric()):
        return Response({"Message": "User Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
    songs = [1,3,4,2]
    if(len(songs) == 0):
        return Response({"Message": "Information Not Found"}, status=status.HTTP_404_NOT_FOUND)
    rec = Recommendation(songs)
    serializer = RecommendationSerializer(rec)
    return Response(serializer.data)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def popular_recommendation(request):
    songs = [5,10,4,2]
    print("SONGS: ", songs )
    rec = Recommendation(songs)
    print("rec is: ", rec)
    serializer = RecommendationSerializer(rec)
    return Response(serializer.data)