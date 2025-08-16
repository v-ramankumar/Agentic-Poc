from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
import json
import os

from db.config.connection import get_db
from db.models.dbmodels.requestProgress import RequestProgress, RequestStatus
from db.models.dbmodels.utility.httpResponseEnum import HttpResponseEnum
from db.models.responseModels.JsonResponse import JsonResponse

router = APIRouter()

@router.get("/patients/{patient_id}")
async def get_patient_details(patient_id: int, payer_id: int = Query(...)):
    """Retrieve patient information based on patient_id and payer_id."""
    
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tmp", "json-payload.json")
    print(f"Looking for file at: {json_file_path}")
    db = await get_db()
    try:
        if not os.path.exists(json_file_path):
            raise HTTPException(status_code=404, detail=f"JSON payload file not found at: {json_file_path}")
            
        with open(json_file_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()

            
            content = content.strip()
            if not content:
                raise HTTPException(status_code=500, detail="JSON payload file is empty")
            json_data = json.loads(content)
            db.collection("requestProgress").update_one(
                {"requestId": payer_id},
                {
                    "$set": {
                        "status": RequestStatus.IN_PROGRESS,
                        "lastUpdatedAt": datetime.now(),
                        "remarks": "Patient details retrieved successfully"
                    }
                }
            )
        return JsonResponse(
            http_status=HttpResponseEnum.OK,
            json_data=json_data
        )
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        db.collection("requestProgress").update_one(
            {"requestId": payer_id},
            {
                "$set": {
                    "status": RequestStatus.FAILED,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": f"Invalid JSON format: {str(e)}"
                }
            }
        )
        raise HTTPException(status_code=500, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        print(f"General error: {str(e)}")
        db.collection("requestProgress").update_one(
            {"requestId": payer_id},
            {
                "$set": {
                    "status": RequestStatus.FAILED,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": str(e)
                }
            }
        )
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")