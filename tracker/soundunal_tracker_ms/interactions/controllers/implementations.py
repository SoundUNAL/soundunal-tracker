import datetime
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
        if reaction_type == Reaction.LIKED:
            return self.db.user_has_liked(int(user_id), int(audio_id))
        else:
            return self.db.user_has_disliked(int(user_id), int(audio_id))

    def get_liked_songs(self, user_id: str) -> list:
        return self.db.get_user_likes(int(user_id))

    def get_comments(self, audio_id: str) -> list:
        return self.db.get_audio_comments(int(audio_id))

    def get_reproduction_info(self, audio_id: str) -> int:
        return self.db.get_audio_reproductions(int(audio_id))

    def get_recently_played(self, user_id: str) -> list:
        return self.db.get_user_recent_songs(int(user_id))

    def post_reaction(self, user_id: str, audio_id: str, reaction_type: Reaction) -> str:
        if reaction_type == Reaction.LIKED:
            return self.db.give_like(int(user_id), int(audio_id))
        else:
            return self.db.give_dislike(int(user_id), int(audio_id))

    def delete_reaction(self, user_id: str, audio_id: str) -> bool:
        return self.db.delete_reaction(int(user_id), int(audio_id))

    def post_comment(self, user_id: str, audio_id: str, comment: str) -> str:
        return self.db.post_comment(int(user_id), int(audio_id), comment)

    def post_reproduction(self, user_id: str, audio_id: str, date: datetime) -> str:
        return self.db.new_reproduction(int(user_id), int(audio_id), date)


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
