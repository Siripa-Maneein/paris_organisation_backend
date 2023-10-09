from model import ParisDB

#mongodb driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

database = client.ParisDB

collection = database.sport_info

######################Example CRUD request######################
async def fetch_one_sport_info(sport_id):
    document = await collection.find_one({"sport_id": sport_id})
    return document

async def fetch_all_sport_infos():
    sport_infos = []
    cursor = collection.find({})
    async for document in cursor:
        sport_infos.append(ParisDB(**document))
    return sport_infos
    
async def create_sport_info(sport_info):
    document = sport_info
    # find existing sport_id
    try:
        temp = await collection.find_one({"sport_id": sport_info["sport_id"]})
        if temp["sport_id"] ==  sport_info["sport_id"]:
            return False
    except:
        result = await collection.insert_one(document)
        return document

async def update_sport_info(sport_id, sport_name, participating_country, date_time, result):
    
    await collection.update_one({"sport_id": sport_id}, {"$set": {
        "sport_id": sport_id,
        "sport_name": sport_name,
        "participating_country":participating_country,
        "date_time": date_time,
        "result": result
    }})
    document = await collection.find_one({"sport_id": sport_id})
    return document

async def remove_sport_info(sport_id):
    await collection.delete_one({"sport_id": sport_id})
    return True

##################################################################