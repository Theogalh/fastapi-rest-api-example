import datetime

from bson.objectid import ObjectId


class GenericManager(object):

    __abstract__ = True

    model = None

    collection = None

    @classmethod
    async def get_all(cls):
        db_objects = []
        async for db_object in cls.collection.find():
            db_objects.append(cls.model(**db_object))
        return db_objects

    @classmethod
    async def create(cls, data):
        new_user = cls.model(**data)
        db_object = await cls.collection.insert_one(new_user.dict())
        setattr(new_user, "id", db_object.inserted_id)
        return new_user

    @classmethod
    async def get(cls, object_id):
        db_object = await cls.collection.find_one({"_id": ObjectId(object_id)})
        return cls.model(**db_object)

    @classmethod
    async def update(cls, object_id, data) -> bool:
        if len(data) < 1:
            return False
        db_object = await cls.collection.find_one({"_id": ObjectId(object_id)})
        if db_object:
            data['modification_datetime'] = datetime.datetime.now()
            updated_db_object = await cls.collection.update_one(
                {"_id": ObjectId(object_id)}, {"$set": data}
            )
            if updated_db_object:
                return True
            return False

    @classmethod
    async def delete(cls, object_id) -> bool:
        db_object = await cls.collection.find_one({"_id": ObjectId(object_id)})
        if db_object:
            await cls.collection.delete_one({"_id": ObjectId(object_id)})
            return True
        return False
