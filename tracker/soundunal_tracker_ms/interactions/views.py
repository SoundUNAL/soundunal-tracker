from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .response import CommentsResponse, InteractionCounterResponse, UserReactionResponse, UserSongsResponse
from .serializers import CommentsSerializer, InteractionCounterSerializer, UserReactionSerializer, UserSongsSerializer
from .controllers.enums import Reaction
from .controllers.implementations import MockInteractionsController, MongoInteractionsController


controller = MongoInteractionsController()


def build_interactions_counter_response(count):
    response_count = InteractionCounterResponse(count)
    response_serializer = InteractionCounterSerializer(response_count)
    return Response(response_serializer.data)


def build_comments_response(comments):
    response_comments = CommentsResponse(comments)
    response_serializer = CommentsSerializer(response_comments)
    return Response(response_serializer.data)


def get_user_reaction(reaction):
    response_reaction = UserReactionResponse(reaction)
    response_serializer = UserReactionSerializer(response_reaction)
    return response_serializer


def do_react(request):
    user_id = request.data['user_id']
    if user_id == "5":
        return Response({"Message": "User Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_201_CREATED)


def reaction_delete(request):
    user_id = request.data['user_id']
    if user_id == "5":
        return Response({"Message": "User Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


def is_reacted_by_user(request, audio_id, reaction_type):
    user_id = request.query_params.get('user')
    try:
        response_serializer = get_user_reaction(
            controller.get_user_reaction(user_id, audio_id, reaction_type))
        return Response(response_serializer.data)
    except Exception:
        return Response({"Message": "Mocked is reacted exception response"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
@renderer_classes([JSONRenderer])
def audio_likes(request, audio_id):
    if not audio_id.isnumeric():
        return Response({"Message": "Audio Not Valid"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        return do_react(request)

    if request.method == 'DELETE':
        return reaction_delete(request)

    # GET: filtro de que el usuario dio like a ese audio
    if (request.query_params.get('user') is not None):
        return is_reacted_by_user(request, audio_id, Reaction.LIKED)

    # GET: numero de likes del audio
    try:
        count = controller.get_reactions_info(audio_id, Reaction.LIKED)
    except Exception as e:
        print(str(e))
        return Response({"Message": "Info unavailable"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if count == 0:
        response_count = InteractionCounterResponse(count)
        response_serializer = InteractionCounterSerializer(response_count)
        return Response(response_serializer.data, status=status.HTTP_404_NOT_FOUND)

    return build_interactions_counter_response(count)


@api_view(['GET', 'POST', 'DELETE'])
@renderer_classes([JSONRenderer])
def audio_dislikes(request, audio_id):
    if not audio_id.isnumeric():
        return Response({"Message": "Audio Not Valid"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        return do_react(request)

    if request.method == 'DELETE':
        return reaction_delete(request)

    if (request.query_params.get('user') is not None):
        return is_reacted_by_user(request, audio_id, Reaction.DISLIKED)

    # GET: numero de dislikes del audio
    try:
        count = controller.get_reactions_info(audio_id, Reaction.DISLIKED)
    except Exception as e:
        print(str(e))
        return Response({"Message": "Info unavailable"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if count == 0:
        response_count = InteractionCounterResponse(count)
        response_serializer = InteractionCounterSerializer(response_count)
        return Response(response_serializer.data, status=status.HTTP_404_NOT_FOUND)

    return build_interactions_counter_response(count)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def user_likes(request):
    user_id = request.query_params.get('user')
    if not user_id.isnumeric():
        return Response({"Message": "User Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
    songs = [1, 3, 4, 2]
    if len(songs) == 0:
        return Response({"Message": "Information Not Found"}, status=status.HTTP_404_NOT_FOUND)
    liked = UserSongsResponse(songs)
    serializer = UserSongsSerializer(liked)
    return Response(serializer.data)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def audio_reproductions(request, audio_id):
    if not audio_id.isnumeric():
        return Response({"Message": "Audio Not Valid"}, status=status.HTTP_400_BAD_REQUEST)

    count = 2000012
    # TODO: Revisar si no hay registros del audio en la tabla de historial
    if audio_id == "5":
        return Response({"Message": "Audio Not Found"}, status=status.HTTP_404_NOT_FOUND)
    return build_interactions_counter_response(count)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def audio_comments(request, audio_id):
    if not audio_id.isnumeric():
        return Response({"Message": "Audio Not Valid"}, status=status.HTTP_400_BAD_REQUEST)

    comments = ['malo', 'bueno', 'me encanto', 'sigan así']
    # TODO: Revisar si no hay registros del audio en la tabla de reviews
    if audio_id == "5":
        return Response({"Message": "Audio Not Found"}, status=status.HTTP_404_NOT_FOUND)
    return build_comments_response(comments)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def user_recently_played(request, user_id):
    # TODO: refactor with user_likes (both have the same code)
    if not user_id.isnumeric():
        return Response({"Message": "User Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
    songs = [100, 300, 445, 21]
    if len(songs) == 0:
        return Response({"Message": "Information Not Found"}, status=status.HTTP_404_NOT_FOUND)
    played = UserSongsResponse(songs)
    serializer = UserSongsSerializer(played)
    return Response(serializer.data)
