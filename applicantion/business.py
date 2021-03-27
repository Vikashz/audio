from bson import json_util, ObjectId
import json
from datetime import datetime
from app import mongo


def create_record(audioFileType, audioFileMetadata):
    res = verify_fields(audioFileType, audioFileMetadata)
    if not res.get("status"):
        return res
    distinct_id = mongo.songs.distinct("id")
    if int(audioFileMetadata["id"]) in distinct_id:
        return {'status': False, 'message': "Record with ID {} alredy exists".format(audioFileMetadata["id"])}
    audioFileMetadata["uploaded_time"] = datetime.now()
    updated = mongo.audio.insert_one(audioFileMetadata)
    if updated:
        return {'status': True, 'message': "Record created successfully"}


def delete_record(audioFileType, audioFileID):
    deleted = mongo.audio.delete_one({"audioFileType": audioFileType, "id": audioFileID})
    if deleted:
        return True
    return False


def upd_record(audioFileType, audioFileMetadata, audioFileID):
    res = verify_fields(audioFileType, audioFileMetadata)
    if not res.get("status"):
        return res

    exists = mongo.audio.find_one({"audioFileType": audioFileType, "id": audioFileID})
    if not exists:
        return {'status': False, 'message': "Record does not exists"}
    audioFileMetadata["uploaded_time"] = exists["uploaded_time"]
    updated = mongo.audio.update({
        "audioFileType": audioFileType, "id": audioFileID
    }, {
        "$set": {
            "activated": False
        }
    })
    if updated:
        return {'status': True, 'message': "Record created successfully"}


def verify_fields(audioFileType, audioFileMetadata):
    if audioFileType.lower() == "song":
        if not audioFileMetadata.get("id"):
            return {'status': False, 'message': "id was not given, id is mandatory"}
        if not audioFileMetadata.get("name_of_the_song"):
            return {'status': False, 'message': "Name of the song was not given, it is mandatory"}
        elif len(audioFileMetadata.get("name_of_the_song")) > 100:
            return {'status': False, 'message':"Name of the song can not be larger than 1000 characters"}
        if not audioFileMetadata.get("duration_in_seconds"):
            return {'status': False, 'message':"Duration of the song was not given, it is mandatory"}
       
    elif audioFileType.lower() == "podcast":
        if not audioFileMetadata.get("id"):
            return {'status': False, 'message': "id was not given, id is mandatory"}
        if not audioFileMetadata.get("name_of_the_podcast"):
            return {'status': False, 'message': "Name of the podcast was not given, it is mandatory"}
        elif len(audioFileMetadata.get("name_of_the_podcast")) > 100:
            return {'status': False, 'message':"Name of the podcast can not be larger than 1000 characters"}
        if not audioFileMetadata.get("duration_in_seconds"):
            return {'status': False, 'message':"Duration of the song was not given, it is mandatory"}
        if not audioFileMetadata.get("host"):
            return {'status': False, 'message':"Host was not given, it is mandatory"}
        elif len(audioFileMetadata.get("host")) > 100:
            return {'status': False, 'message':"Host can not be larger than 1000 characters"}
        if audioFileMetadata.get("participants"):
            for n, p in enumerate(audioFileMetadata.get("participants")):
                if len(p) > 100:
                    return {'status': False, 'message':"participants can not be larger than 1000 characters"}
                if n > 10:
                    return {'status': False, 'message':"participants can not be larger than 1000 characters"}

    elif audioFileType.lower() == "audiobook":
        if not audioFileMetadata.get("id"):
            return {'status': False, 'message': "id was not given, id is mandatory"}
        if not audioFileMetadata.get("title_of_the_audiobook"):
            return {'status': False, 'message': "Title of the audiobook was not given, it is mandatory"}
        elif len(audioFileMetadata.get("title_of_the_audiobook")) > 100:
            return {'status': False, 'message':"Title of the audiobook can not be larger than 1000 characters"}
        if not audioFileMetadata.get("duration_in_seconds"):
            return {'status': False, 'message':"Duration of the song was not given, it is mandatory"}
        if not audioFileMetadata.get("author"):
            return {'status': False, 'message':"Author of the title was not given, it is mandatory"}
        elif len(audioFileMetadata.get("author")) > 100:
            return {'status': False, 'message':"Author of the title can not be larger than 1000 characters"}
        if not audioFileMetadata.get("narrator"):
            return {'status': False, 'message':"Narrator was not given, it is mandatory"}
    
    else:
        return {'status': False, 'message':"Unknown audio file type"}