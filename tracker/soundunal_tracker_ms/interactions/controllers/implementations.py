from ...utils import Connection, MongoAccessLogic
from .enums import Reaction
from .interfaces import InteractionsController


class MongoInteractionsController(InteractionsController):
    def __init__(self) -> None:
        super().__init__()
        self.db = MongoAccessLogic(Connection())

    def get_reactions_info(self, audio_id: str, reaction_type: Reaction) -> int:
        if reaction_type == Reaction.LIKED:
            return self.db.get_audio_likes(int(audio_id))
        else:
            return self.db.get_audio_dislikes(int(audio_id))

    def get_user_reaction(self, user_id: str, audio_id: str, reaction_type: Reaction) -> bool:
        if int(audio_id) > 10:
            raise Exception('Mock exception')
        return True

    def get_liked_songs(self, user_id: str) -> list:
        pass

    def get_comments(self, audio_id: str) -> list:
        pass

    def get_reproduction_info(self, audio_id: str) -> int:
        pass

    def get_recently_played(self, user_id: str) -> list:
        pass

    def post_reaction(self, user_id: str, audio_id: str, reaction_type: Reaction) -> bool:
        pass

    def delete_reaction(self, user_id: str, audio_id: str) -> bool:
        pass


class MockInteractionsController(InteractionsController):
    def get_reactions_info(self, audio_id: str, reaction_type: Reaction) -> int:
        if int(audio_id) > 10:
            raise Exception('Mock exception')
        return 6

    def get_user_reaction(self, user_id: str, audio_id: str, reaction_type: Reaction) -> bool:
        if int(audio_id) > 10:
            raise Exception('Mock exception')
        return True

    def get_liked_songs(self, user_id: str) -> list:
        pass

    def get_comments(self, audio_id: str) -> list:
        pass

    def get_reproduction_info(self, audio_id: str) -> int:
        pass

    def get_recently_played(self, user_id: str) -> list:
        pass

    def post_reaction(self, user_id: str, audio_id: str, reaction_type: Reaction) -> bool:
        pass

    def delete_reaction(self, user_id: str, audio_id: str) -> bool:
        pass