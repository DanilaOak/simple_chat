MESSAGE_COLLECTION = 'messages'
CHAT_COLLECTION = 'chat'


class Message:

    def __init__(self, collection, **kwargs):
        self.collection = collection

    async def save(self, chat_name, user_name, created: str, message, **kwargs):
        result = await self.collection.insert(
            {'chat_name': chat_name, 'user_name': user_name, 'created': created, 'message': message})
        return result

    async def get_messages(self):
        result = self.collection.find().sort([('time', 1)])
        return await result.to_list(length=None)

    async def get_by_id(self, message_id):
        result = await self.collection.find_one({'message_id': message_id})
        return result

    async def update(self, message_id, data):
        await self.collection.update_one({'message_id': message_id}, {'$set': data})
        result = await self.collection.find_one({'message_id': message_id})
        return result


class Chat:

    def __init__(self, collection, **kwargs):
        self.collection = collection

    async def save(self, chat_name, user_name, created: str, message, **kwargs):
        result = await self.collection.insert(
            {'chat_name': chat_name, 'created': created, 'messages': []})
        return result


class DataBase:

    def __init__(self, db: dict):
        self.message = Message(db[MESSAGE_COLLECTION])
        self.chat = Chat(db[CHAT_COLLECTION])
