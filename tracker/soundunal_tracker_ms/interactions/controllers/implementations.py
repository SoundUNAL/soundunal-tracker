from .enums import Reaction
from .interfaces import InteractionsController


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
