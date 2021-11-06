from pymongo import MongoClient
from emoji import emojize
from random import choice

import settings


def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id,
            "emoji": emojize(choice(settings.USER_EMOJI), use_aliases=True)
        }
        db.users.insert_one(user)
    return user


def change_avatar_db(db, effective_user):
    db.users.update_one({
        'user_id': effective_user.id
    }, {
        '$set': {
            'emoji': emojize(choice(settings.USER_EMOJI), use_aliases=True)
        }
    }, upsert=False)
    user = db.users.find_one({"user_id": 460311758})
    return user


client = MongoClient(settings.CONN_STR, serverSelectionTimeoutMS=5000)

db = client[settings.MONGO_DB]
