from .enums import Reaction


class InteractionsController():
    def get_reactions_info(self, audio_id: str, reaction_type: Reaction) -> int:
        pass

    def get_user_reaction(self, user_id: str, audio_id: str, reaction_type: Reaction) -> bool:
        pass

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
