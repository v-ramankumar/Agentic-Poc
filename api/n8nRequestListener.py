from datetime import datetime
from fastapi import APIRouter, HTTPException

from db.config.connection import get_db
from  db.models.requestmodels.n8nRequestListener import N8nRequestListener
from db.models.dbmodels.requestProgress import RequestStatus
from db.models.dbmodels.utility.httpResponseEnum import HttpResponseEnum
from db.models.responseModels.n8nWorkflowResponse import N8nWorkflowResponse

router = APIRouter()

@router.post("/n8n/listen")
async def n8n_request_listener(req: N8nRequestListener):
    """
    Endpoint to listen for n8n workflow updates and update request progress.
    """
    try:
        db = get_db()
        
        requestId = req.requestId
        payerId = req.payerId
        error = req.error or ""
        message = req.message or ""
        
        # Determine status based on error presence
        if error:
            status = RequestStatus.FAILED
            remarks = f"N8N workflow failed: {error}"
        else:
            status = RequestStatus.SUCCEEDED
            remarks = f"N8N workflow completed successfully: {message}"
        
        # Update request progress in database
        result = await db.collection("requestProgress").update_one(
            {"requestId": requestId},
            {
                "$set": {
                    "status": status,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": remarks
                }
            }
        )
        
        # Check if the request was found and updated
        if result.matched_count == 0:
            raise HTTPException(
                status_code=404, 
                detail=f"Request with ID {requestId} not found"
            )
        
        # Log the update for debugging
        print(f"Updated request {requestId} with status {status}")
        
        return N8nWorkflowResponse(
            http_status=HttpResponseEnum.OK
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other exceptions
        print(f"Error in n8n_request_listener: {str(e)}")
        
        # Try to update the request as failed if possible
        try:
            if 'requestId' in locals():
                await db.collection("requestProgress").update_one(
                    {"requestId": requestId},
                    {
                        "$set": {
                            "status": RequestStatus.FAILED,
                            "lastUpdatedAt": datetime.now(),
                            "remarks": f"Internal error processing n8n response: {str(e)}"
                        }
                    }
                )
        except:
            pass  # Don't fail if we can't update the database
        
        return N8nWorkflowResponse(
            http_status=HttpResponseEnum.INTERNAL_SERVER_ERROR,
            error_message=str(e)
        )


