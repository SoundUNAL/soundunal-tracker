from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecommendationSerializer
from .response import Recommendation


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def user_recommendation(request, user_id):
    """
    API endpoint for retrieving user recommendations.

    Parameters:
        request (HttpRequest): The HTTP request object.
        user_id (str): The user ID for which recommendations are requested.

    Returns:
        Response: A JSON response containing user recommendations.

    Example:
        GET /v1/recommendations/users/123
    """
    if not user_id.isnumeric():
        return Response({"Message": "User Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
    songs = [1, 3, 4, 2]
    if len(songs) == 0:
        return Response({"Message": "Information Not Found"}, status=status.HTTP_404_NOT_FOUND)
    rec = Recommendation(songs)
    serializer = RecommendationSerializer(rec)
    return Response(serializer.data)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def popular_recommendation(request):
    """
    API endpoint for retrieving popular recommendations.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing popular recommendations.

    Example:
        GET /v1/recommendations
    """
    songs = [5, 10, 4, 2]
    print("SONGS: ", songs)
    rec = Recommendation(songs)
    print("rec is: ", rec)
    serializer = RecommendationSerializer(rec)
    return Response(serializer.data)
