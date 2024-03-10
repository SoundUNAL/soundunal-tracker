from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .response import InteractionCounterResponse
from .serializers import InteractionCounterSerializer


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def audio_likes(request, audio_id):
    """
    API endpoint for retrieving the number of likes for a specific audio.

    Parameters:
        request (HttpRequest): The HTTP request object.
        audio_id (str): The ID of the audio for which likes are requested.

    Returns:
        Response: A JSON response containing the number of likes for the audio.

    Example:
        GET /v1/interactions/audios/1/likes
    """
    if not audio_id.isnumeric():
        return Response({"Message": "Audio Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
    count = 532
    # TODO: Revisar si no hay registros del audio en la tabla de likes
    if audio_id == "5":
        return Response({"Message": "Audio Not Found"}, status=status.HTTP_404_NOT_FOUND)
    like = InteractionCounterResponse(count)
    serializer = InteractionCounterSerializer(like)
    return Response(serializer.data)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def audio_dislikes(request, audio_id):
    """
    API endpoint for retrieving the number of dislikes for a specific audio.

    Parameters:
        request (HttpRequest): The HTTP request object.
        audio_id (str): The ID of the audio for which dislikes are requested.

    Returns:
        Response: A JSON response containing the number of dislikes for the audio.

    Example:
        GET /v1/interactions/audios/1/dislikes
    """
    if not audio_id.isnumeric():
        return Response({"Message": "Audio Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
    count = 200
    # TODO: Revisar si no hay registros del audio en la tabla de likes
    if audio_id == "5":
        return Response({"Message": "Audio Not Found"}, status=status.HTTP_404_NOT_FOUND)
    dislike = InteractionCounterResponse(count)
    serializer = InteractionCounterSerializer(dislike)
    return Response(serializer.data)
