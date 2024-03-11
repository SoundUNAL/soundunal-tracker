class InteractionCounterResponse():
    def __init__(self, count=0):
        self.count = count


class UserReactionResponse():
    def __init__(self, reaction=False):
        self.reaction = reaction


class UserSongsResponse():
    def __init__(self, songs):
        self.songs = songs


class CommentsResponse():
    def __init__(self, comments):
        self.comments = comments
