from fastapi import APIRouter, HTTPException, Query, Request
from jsonschema import validate, ValidationError
import json
import os


router = APIRouter()







@router.get("/patients/{patient_id}")
async def get_patient_details(patient_id: int, payer_id: int = Query(...)):
    """Retrieve patient information based on patient_id and payer_id."""
    
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tmp", "json-payload.json")
    print(f"Looking for file at: {json_file_path}")
    
    try:
        if not os.path.exists(json_file_path):
            raise HTTPException(status_code=404, detail=f"JSON payload file not found at: {json_file_path}")
            
        with open(json_file_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()
            print(f"Raw file content: '{content}'")
            print(f"File content length: {len(content)}")
            print(f"First 50 chars: '{content[:50]}'")
            
            content = content.strip()
            if not content:
                raise HTTPException(status_code=500, detail="JSON payload file is empty")
            json_data = json.loads(content)
        return json_data
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        print(f"General error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")