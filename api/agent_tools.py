"""
Individual API tools for the Planner Agent
Each endpoint serves as a standalone tool that the agent can call
"""

import uuid
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

import httpx
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from db.config.connection import get_db
from db.models.dbmodels.requestProgress import RequestProgress, RequestStatus
from db.models.dbmodels.priorAuthRequest import priorAuthRequest
from db.models.dbmodels.utility.httpResponseEnum import HttpResponseEnum

router = APIRouter()

# ============================================================================
# TOOL 1: Start New Request
# ============================================================================

class StartRequestTool(BaseModel):
    user_id: str = Field(..., description="ID of the user making the request")
    prompt: str = Field(..., description="Natural language prompt from user")
    
class StartRequestResponse(BaseModel):
    request_id: str = Field(..., description="Generated unique request ID")
    status: str = Field(..., description="Initial status")
    message: str = Field(..., description="Response message")

@router.post("/tools/start-request", response_model=StartRequestResponse)
async def start_new_request(req: StartRequestTool):
    """
    TOOL 1: Start a new preauth request
    Creates initial request tracking record
    """
    request_id = uuid.uuid4().hex
    
    try:
        # Create initial request progress record
        request_progress = RequestProgress(
            requestId=request_id,
            status=RequestStatus.CREATED,
            lastUpdatedAt=datetime.now(),
            remarks=f"New request started with prompt: {req.prompt[:100]}..."
        )
        db = get_db()
        
        res = await db["requestProgress"].insert_one(request_progress.model_dump(by_alias=True))
        print(res)
        return StartRequestResponse(
            request_id=request_id,
            status="CREATED",
            message="Request started successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TOOL 2: Check Payer Onboarding
# ============================================================================

class PayerCheckResponse(BaseModel):
    is_onboarded: bool = Field(..., description="Whether payer is onboarded")
    payer_details: Optional[Dict[str, Any]] = Field(None, description="Payer information if found")
    message: str = Field(..., description="Result message")

@router.get("/tools/check-payer/{payer_id}", response_model=PayerCheckResponse)
async def check_payer_onboarding(payer_id: str, request_id: str = Query(...)):
    """
    TOOL 2: Check if payer is onboarded
    Validates payer existence in the system
    """
    try:
        db = get_db()
        
        # Update request status
        await db["requestProgress"].update_one(
            {"requestId": request_id},
            {
                "$set": {
                    "status": RequestStatus.PROCESSING,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": f"Checking payer onboarding: {payer_id}"
                }
            }
        )
        
        # Check payer in database
        payer = await db["priorAuthPayers"].find_one({"id": payer_id})
        
        if payer:
            # Convert ObjectId to string for JSON serialization
            if "_id" in payer:
                payer["_id"] = str(payer["_id"])
                
            await db["requestProgress"].update_one(
                {"requestId": request_id},
                {
                    "$set": {
                        "status": RequestStatus.PROCESSING,
                        "lastUpdatedAt": datetime.now(),
                        "remarks": "Payer validated successfully"
                    }
                }
            )
            return PayerCheckResponse(
                is_onboarded=True,
                payer_details=payer,
                message="Payer is onboarded and active"
            )
        else:
            await db["requestProgress"].update_one(
                {"requestId": request_id},
                {
                    "$set": {
                        "status": RequestStatus.FAILED,
                        "lastUpdatedAt": datetime.now(),
                        "remarks": f"Payer {payer_id} not found"
                    }
                }
            )
            return PayerCheckResponse(
                is_onboarded=False,
                payer_details=None,
                message=f"Payer {payer_id} is not onboarded"
            )
            
    except Exception as e:
        await db["requestProgress"].update_one(
            {"requestId": request_id},
            {
                "$set": {
                    "status": RequestStatus.FAILED,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": f"Error checking payer: {str(e)}"
                }
            }
        )
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TOOL 3: Get Patient Details
# ============================================================================

class PatientDetailsRequest(BaseModel):
    patient_id: str = Field(..., description="Patient ID to fetch")
    request_id: str = Field(..., description="Associated request ID")

class PatientDetailsResponse(BaseModel):
    patient_data: Dict[str, Any] = Field(..., description="Patient details JSON")
    success: bool = Field(..., description="Whether fetch was successful")
    message: str = Field(..., description="Result message")

@router.post("/tools/get-patient-details", response_model=PatientDetailsResponse)
async def get_patient_details(req: PatientDetailsRequest):
    """
    TOOL 3: Get patient details JSON
    Fetches patient information from external system or database
    """
    db = get_db()
    
    try:
        # Update request status
        await db["requestProgress"].update_one(
            {"requestId": req.request_id},
            {
                "$set": {
                    "status": RequestStatus.PROCESSING,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": f"Fetching patient details for: {req.patient_id}"
                }
            }
        )
        
        # Here you would typically call an external patient API
        # For now, we'll return mock data or fetch from local database
        
        # Example external API call:
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(f"{os.getenv('PATIENT_API_URL')}/patients/{req.patient_id}")
        #     patient_data = response.json()
        
        # Mock patient data for demonstration
        mock_patient_data = {
            "patient_id": req.patient_id,
            "patient_name": "John Doe",
            "date_of_birth": "1990-01-01",
            "insurance_number": "INS123456",
            "diagnosis_code": "Z123",
            "procedure_code": "P456",
            "response": [
                {
                    "payerid": "PAYER001",
                    "patient_details": {
                        "name": "John Doe",
                        "dob": "1990-01-01",
                        "member_id": "MEM123456"
                    }
                }
            ]
        }
        
        await db["requestProgress"].update_one(
            {"requestId": req.request_id},
            {
                "$set": {
                    "status": RequestStatus.PROCESSING,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": "Patient details fetched successfully"
                }
            }
        )
        
        return PatientDetailsResponse(
            patient_data=mock_patient_data,
            success=True,
            message="Patient details retrieved successfully"
        )
        
    except Exception as e:
        await db["requestProgress"].update_one(
            {"requestId": req.request_id},
            {
                "$set": {
                    "status": RequestStatus.FAILED,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": f"Error fetching patient details: {str(e)}"
                }
            }
        )
        return PatientDetailsResponse(
            patient_data={},
            success=False,
            message=f"Failed to fetch patient details: {str(e)}"
        )

# ============================================================================
# TOOL 4: Validate JSON
# ============================================================================

class JsonValidationRequest(BaseModel):
    patient_data: Dict[str, Any] = Field(..., description="Patient JSON data to validate")
    payer_id: str = Field(..., description="Payer ID for validation rules")
    request_id: str = Field(..., description="Associated request ID")

class JsonValidationResponse(BaseModel):
    is_valid: bool = Field(..., description="Whether JSON is valid")
    validation_errors: list = Field(default=[], description="List of validation errors")
    missing_fields: list = Field(default=[], description="List of missing required fields")
    message: str = Field(..., description="Validation result message")

@router.post("/tools/validate-json", response_model=JsonValidationResponse)
async def validate_patient_json(req: JsonValidationRequest):
    """
    TOOL 4: Validate patient JSON against payer rules
    Uses existing validation logic from validate_json.py
    """   
    db = get_db()
    
    try:
        # Update request status
        await db["requestProgress"].update_one(
            {"requestId": req.request_id},
            {
                "$set": {
                    "status": RequestStatus.PROCESSING,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": f"Validating JSON for payer: {req.payer_id}"
                }
            }
        )
        
        # Call existing validation endpoint
        async with httpx.AsyncClient() as client:
            validation_request = {
                "request_id": req.request_id,
                "json_data": req.patient_data
            }
            
            response = await client.post(
                f"{os.getenv('BASE_URL', 'http://localhost:8001')}/api/validate-json",
                json=validation_request,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("is_valid", False):
                    await db["requestProgress"].update_one(
                        {"requestId": req.request_id},
                        {
                            "$set": {
                                "status": RequestStatus.PROCESSING,
                                "lastUpdatedAt": datetime.now(),
                                "remarks": "JSON validation successful"
                            }
                        }
                    )
                    return JsonValidationResponse(
                        is_valid=True,
                        validation_errors=[],
                        missing_fields=[],
                        message="JSON validation passed"
                    )
                else:
                    await db["requestProgress"].update_one(
                        {"requestId": req.request_id},
                        {
                            "$set": {
                                "status": RequestStatus.USER_ACTION_REQUIRED,
                                "lastUpdatedAt": datetime.now(),
                                "remarks": "JSON validation failed - additional info required"
                            }
                        }
                    )
                    return JsonValidationResponse(
                        is_valid=False,
                        validation_errors=result.get("validation_errors", []),
                        missing_fields=result.get("missing_fields", []),
                        message=result.get("message", "Validation failed")
                    )
            else:
                raise Exception("Validation service error")
                
    except Exception as e:
        await db["requestProgress"].update_one(
            {"requestId": req.request_id},
            {
                "$set": {
                    "status": RequestStatus.FAILED,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": f"JSON validation error: {str(e)}"
                }
            }
        )
        return JsonValidationResponse(
            is_valid=False,
            validation_errors=[str(e)],
            missing_fields=[],
            message=f"Validation failed: {str(e)}"
        )

# ============================================================================
# TOOL 5: Trigger N8N Workflow
# ============================================================================

class N8NTriggerRequest(BaseModel):
    request_id: str = Field(..., description="Request ID")
    user_id: str = Field(..., description="User ID")
    patient_id: str = Field(..., description="Patient ID")
    patient_name: str = Field(..., description="Patient name")
    payer_id: str = Field(..., description="Payer ID")
    prompt: str = Field(..., description="Original user prompt")
    validated_json: Dict[str, Any] = Field(..., description="Validated patient JSON")

class N8NTriggerResponse(BaseModel):
    workflow_triggered: bool = Field(..., description="Whether workflow was triggered")
    workflow_id: Optional[str] = Field(None, description="N8N workflow execution ID")
    message: str = Field(..., description="Result message")

@router.post("/tools/trigger-n8n", response_model=N8NTriggerResponse)
async def trigger_n8n_workflow(req: N8NTriggerRequest):
    """
    TOOL 5: Trigger N8N workflow with validated data
    Starts the automation process in N8N
    """   
    db = get_db()
    
    try:
        # Update request status
        await db["requestProgress"].update_one(
            {"requestId": req.request_id},
            {
                "$set": {
                    "status": RequestStatus.IN_PROGRESS,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": "Triggering N8N workflow"
                }
            }
        )
        
        # Create prior auth request record
        prior_auth_request = priorAuthRequest(
            requestId=req.request_id,
            userId=req.user_id,
            patientId=req.patient_id,
            patientName=req.patient_name,
            payerId=req.payer_id,
            createdAt=datetime.now(),
            lastUpdatedAt=datetime.now()
        )
        await db["priorAuthRequest"].insert_one(prior_auth_request.dict())
        
        # Call N8N webhook
        async with httpx.AsyncClient() as client:
            n8n_payload = {
                "requestId": req.request_id,
                "payerId": req.payer_id,
                "userId": req.user_id,
                "patientId": req.patient_id,
                "patientName": req.patient_name,
                "task": req.prompt,
                "json_data": req.validated_json
            }
            
            response = await client.post(
                os.getenv("N8N_WEBHOOK_URL"),
                json=n8n_payload,
                timeout=30.0
            )
            
            if response.status_code in [200, 201]:
                await db["requestProgress"].update_one(
                    {"requestId": req.request_id},
                    {
                        "$set": {
                            "status": RequestStatus.IN_PROGRESS,
                            "lastUpdatedAt": datetime.now(),
                            "remarks": "N8N workflow triggered successfully"
                        }
                    }
                )
                
                return N8NTriggerResponse(
                    workflow_triggered=True,
                    workflow_id=response.headers.get("X-Workflow-ID"),
                    message="N8N workflow triggered successfully"
                )
            else:
                raise Exception(f"N8N webhook failed: {response.status_code}")
                
    except Exception as e:
        await db["requestProgress"].update_one(
            {"requestId": req.request_id},
            {
                "$set": {
                    "status": RequestStatus.FAILED,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": f"N8N trigger failed: {str(e)}"
                }
            }
        )
        return N8NTriggerResponse(
            workflow_triggered=False,
            workflow_id=None,
            message=f"Failed to trigger N8N workflow: {str(e)}"
        )

# ============================================================================
# TOOL 6: Get Request Status
# ============================================================================

@router.get("/tools/request-status/{request_id}")
async def get_request_status(request_id: str):
    """
    TOOL 6: Get current status of any request
    Allows agent to check progress and status
    """
    db = get_db()
    
    try:
        request_progress = await db["requestProgress"].find_one({"requestId": request_id})
        if not request_progress:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Get user actions if any
        user_actions = await db["priorAuthUserAction"].find({"requestId": request_id}).to_list(None)
        
        return {
            "request_id": request_id,
            "status": request_progress["status"],
            "last_updated": request_progress["lastUpdatedAt"],
            "remarks": request_progress.get("remarks", ""),
            "user_actions_pending": len([a for a in user_actions if a.get("actionStatus") == "PENDING"]),
            "workflow_step": request_progress.get("workflowStep"),
            "metadata": request_progress.get("metadata", {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TOOL 7: Handle User Action Response  
# ============================================================================

class UserActionResponse(BaseModel):
    request_id: str = Field(..., description="Request ID")
    action_id: str = Field(..., description="User action ID")
    response_data: Dict[str, Any] = Field(..., description="User provided data")

@router.post("/tools/handle-user-action")
async def handle_user_action_response(req: UserActionResponse):
    """
    TOOL 7: Process user action response
    Updates database and can resume workflow
    """  
    db = get_db()
    
    try:
        # Update user action status
        result = await db["priorAuthUserAction"].update_one(
            {"id": req.action_id, "requestId": req.request_id},
            {
                "$set": {
                    "actionStatus": "COMPLETED",
                    "actionedAt": datetime.now(),
                    "metadata": json.dumps(req.response_data)
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User action not found")
        
        # Update request status to resume processing
        await db["requestProgress"].update_one(
            {"requestId": req.request_id},
            {
                "$set": {
                    "status": RequestStatus.PROCESSING,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": "User action completed - ready to resume"
                }
            }
        )
        
        return {
            "success": True,
            "message": "User action processed successfully",
            "can_resume": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
