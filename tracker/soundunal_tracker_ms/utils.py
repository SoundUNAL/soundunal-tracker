from pymongo import MongoClient
import pymongo


class Connection():
    def __init__(self, connection_uri="mongodb://host.docker.internal:27017/", db_name='soundunal_interactions_db'):
        self.client = MongoClient(connection_uri)
        self.db_handler = self.client[db_name]


class MongoAccessLogic():
    def __init__(self, connection) -> None:
        self.connection = connection

    def get_audio_likes(self, audio_id):
        return self.connection.db_handler.reactions.count_documents(
            {'audioID': audio_id, 'reaction': 'LIKED'})

    def get_audio_dislikes(self, audio_id):
        return self.connection.db_handler.reactions.count_documents(
            {'audioID': audio_id, 'reaction': 'DISLIKED'})

    def get_audio_reproductions(self, audio_id):
        return self.connection.db_handler.history.count_documents({'audioID': audio_id})

    def get_user_likes(self, user_id):
        result = self.connection.db_handler.reactions.find({'userID': user_id, 'reaction': 'LIKED'},
                                                           {'_id': 0, 'audioID': 1})
        return [x['audioID'] for x in result]

    def user_has_liked(self, user_id, audio_id):
        return True if self.connection.db_handler.reactions.find_one({'userID': user_id, 'audioID': audio_id, 'reaction': 'LIKED'}) is not None else False

    def user_has_disliked(self, user_id, audio_id):
        return True if self.connection.db_handler.reactions.find_one({'userID': user_id, 'audioID': audio_id, 'reaction': 'DISLIKED'}) is not None else False

    def get_audio_comments(self, audio_id):
        result = self.connection.db_handler.reviews.find(
            {'audioID': audio_id}, {'_id': 0, 'userID': 1, 'comment': 1})
        return [x for x in result]

    def get_user_recent_songs(self, user_id):
        result = self.connection.db_handler.history.find({'userID': user_id}, {'_id': 0, 'audioID': 1}).sort(
            'date', pymongo.DESCENDING).limit(15)
        return [x['audioID'] for x in result]

    def delete_reaction(self, user_id, audio_id):
        deleted = self.connection.db_handler.reactions.delete_one(
            {'userID': user_id, 'audioID': audio_id})
        return True if deleted.deleted_count > 0 else False

    def give_like(self, user_id, audio_id):
        if self.connection.db_handler.reactions.find_one({'userID': user_id, 'audioID': audio_id}) is not None:
            self.connection.db_handler.reactions.update_one({'userID': user_id, 'audioID': audio_id}, {
                '$set': {'reaction': "LIKED"}})
            return 'Updated'
        else:
            self.connection.db_handler.reactions.insert_one(
                {'userID': user_id, 'audioID': audio_id, 'reaction': "LIKED"})
            return 'Created'

    def give_dislike(self, user_id, audio_id):
        if self.connection.db_handler.reactions.find_one({'userID': user_id, 'audioID': audio_id}) is not None:
            self.connection.db_handler.reactions.update_one({'userID': user_id, 'audioID': audio_id}, {
                '$set': {'reaction': "DISLIKED"}})
            return 'Updated'
        else:
            self.connection.db_handler.reactions.insert_one(
                {'userID': user_id, 'audioID': audio_id, 'reaction': "DISLIKED"})
            return 'Created'
