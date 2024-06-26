import datetime
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


def do_react(request, audio_id, reaction_type):
    user_id = request.data['user_id']
    operation_type = controller.post_reaction(user_id, audio_id, reaction_type)
    if user_id == "5":
        return Response({"Message": "User Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"Type": operation_type}, status=status.HTTP_201_CREATED)


def comment(request, audio_id):
    user_id = request.data['user_id']
    com = request.data['comment']
    make_comment = controller.post_comment(user_id, audio_id, com)
    return Response({"State": make_comment}, status=status.HTTP_201_CREATED)


def new_interaction(request, audio_id):
    user_id = request.data['user_id']
    interact = controller.post_reproduction(
        user_id, audio_id, datetime.datetime.now(datetime.UTC))
    return Response({"State": interact}, status=status.HTTP_201_CREATED)


def reaction_delete(request, audio_id):
    user_id = request.data['user_id']
    operation_state = controller.delete_reaction(user_id, audio_id)

    '''
    if user_id == "5":
        return Response({"Message": "User Not Valid"}, status=status.HTTP_400_BAD_REQUEST)
    '''

    return Response({"State": operation_state}, status=status.HTTP_200_OK)


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
        return do_react(request, audio_id, Reaction.LIKED)

    if request.method == 'DELETE':
        return reaction_delete(request, audio_id)

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
        return do_react(request, audio_id, Reaction.DISLIKED)

    if request.method == 'DELETE':
        return reaction_delete(request, audio_id)

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

    songs = controller.get_liked_songs(user_id)
    if len(songs) == 0:
        return Response({"Message": "Information Not Found"}, status=status.HTTP_404_NOT_FOUND)

    liked = UserSongsResponse(songs)
    serializer = UserSongsSerializer(liked)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def audio_reproductions(request, audio_id):
    if not audio_id.isnumeric():
        return Response({"Message": "Audio Not Valid"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        return new_interaction(request, audio_id)

    count = controller.get_reproduction_info(audio_id)
    # TODO: Revisar si no hay registros del audio en la tabla de historial
    '''
    if audio_id == "5":
        return Response({"Message": "Audio Not Found"}, status=status.HTTP_404_NOT_FOUND)
    '''
    return build_interactions_counter_response(count)


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def audio_comments(request, audio_id):
    if not audio_id.isnumeric():
        return Response({"Message": "Audio Not Valid"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        return comment(request, audio_id)

    comments = controller.get_comments(audio_id)
    return build_comments_response(comments)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def user_recently_played(request, user_id):
    # TODO: refactor with user_likes (both have the same code)
    if not user_id.isnumeric():
        return Response({"Message": "User Not Valid"}, status=status.HTTP_400_BAD_REQUEST)

    songs = controller.get_recently_played(user_id)
    if len(songs) == 0:
        return Response({"Message": "Information Not Found"}, status=status.HTTP_404_NOT_FOUND)
    played = UserSongsResponse(songs)
    serializer = UserSongsSerializer(played)
    return Response(serializer.data)
