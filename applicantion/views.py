from app import songs_api, mongo
from flask import Response,render_template,request,jsonify
from bson import json_util, ObjectId
import json
from applicantion import business as biz


@songs_api.route("/songs/create", methods=["POST"])
def view_create_record():
    """
        This API creates a record based on audio file type.
        Sample payload for Song type
        {
            "audioFileType": "Song",
            "audioFileMetadata": {
                "id": 1001,
                "name_of_the_song": "Name of the song",
                "duration_in_seconds": 342
            }
        }

        Sample payload for podacst
        {
            "audioFileType": "podcast",
            "audioFileMetadata": {
                "id": 1002,
                "name_of_the_podcast": "Name of the song",
                "host": "Jimmy",
                "participants": ["Vicky", "Rony"],
                "duration_in_seconds": 342
            }
        }

        Sample payload for audiobook
        {
            "audioFileType": "audiobook",
            "audioFileMetadata": {
                "id": 1003,
                "title_of_the_audiobook": "Name of the song",
                "author": "Jimmy",
                "narrator": "Ranjit",
                "duration_in_seconds": 342
            }
        }
    """
    status = 200
    try:
        print("Hello")
        json_data = request.get_json(force=True)
        print(json_data)
        audioFileType = json_data.get("audioFileType", "")
        audioFileMetadata = json_data.get("audioFileMetadata", {})

        if not audioFileType:
            raise ValueError("Audio file type is required")
        if not audioFileMetadata:
            raise ValueError("Audio file metadata is required")

        response = biz.create_record(audioFileType, audioFileMetadata)
    except Exception as e:
        response = {"status": False, "message": str(e)}
        status = 400
    return Response(json.dumps(response, default=json_util.default), mimetype="application/json"), status


@songs_api.route("/songs/delete/<audioFileType>/<audioFileID>", methods=['DELETE'])
def view_delete_record(audioFileType, audioFileID):
    """
        Admin API to delete a record
    """
    status = 200
    try:
        res = biz.delete_record(audioFileType, audioFileID)
        if res:
            response = { "status" : True, "message" : "Record deleted successfully" }
        else:
            response = { "status" : True, "message" : "Unable to delete" }
    except Exception as e:
        response = {"status": False, "message": str(e)}
        status = 400
    return Response(json.dumps(response, default=json_util.default ), mimetype="application/json")


@songs_api.route("/songs/update/<audioFileType>/<audioFileID>", methods=["POST"])
def view_upd_record(audioFileType, audioFileID):
    """
        This API updates a record based on audio file type.
        Sample payload for Song type
        {
            "audioFileType": "Song",
            "audioFileMetadata": {
                "id": 1001,
                "name_of_the_song": "Name of the song",
                "duration_in_seconds": 342
            }
        }

       
    """
    status = 200
    try:
        json_data = request.get_json(force=True)
        audioFileMetadata = json_data.get("audioFileMetadata", {})
        if not audioFileMetadata:
            raise ValueError("Audio file metadata is required")

        response = biz.upd_record(audioFileType, audioFileMetadata, audioFileID)
    except Exception as e:
        response = {"status": False, "message": str(e)}
        status = 400
    return Response(json.dumps(response, default=json_util.default), mimetype="application/json"), status


@songs_api.route("/songs/get/<audioFileType>", methods=['GET'],defaults={'audioFileID':"all"})
@songs_api.route("/songs/get/<audioFileType>/<audioFileID>", methods=['GET'])
def view_get_record(audioFileType, audioFileID):
    """
        Admin API to get one/all records.
    """
    status = 200
    try:
        if not audioFileID == "all":
            res = mongo.audio.find({"audioFileType": audioFileType, "id": int(audioFileID)})
        else:
            res = mongo.audio.find({"audioFileType": audioFileType})
        if res:
            response = { "status" : True, "data" : res }
        else:
            response = { "status" : True, "message" : "Unable to get data" }
    except Exception as e:
        response = {"status": False, "message": str(e)}
        status = 400
    return Response(json.dumps(response, default=json_util.default ), mimetype="application/json")
