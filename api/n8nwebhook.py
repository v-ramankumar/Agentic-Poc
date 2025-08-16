import os
from datetime import datetime

from fastapi import APIRouter, HTTPException
from httpx import AsyncClient
from db.config.connection import get_db
from db.models.dbmodels.requestProgress import RequestStatus
from db.models.dbmodels.utility.httpResponseEnum import HttpResponseEnum
from db.models.requestmodels.n8nWebhookRequest import n8nWebhookRequest
from db.models.responseModels.n8nWorkflowResponse import N8nWorkflowResponse

router = APIRouter()



@router.post("/n8n-webhook")
async def n8n_webhook(req: n8nWebhookRequest):
    db = await get_db()
    requestId = req.requestId
    json_data = req.json_data
    payer_id = req.payer_id
    task = req.task
    try:
        # Extract request params


        # Forward request to N8N webhook
        async with AsyncClient() as client:
            response = await client.post(
                os.getenv("N8N_WEBHOOK_URL"),
                json={
                    "requestId": requestId,
                    "json_data": json_data,
                    "payer_id": payer_id,
                    "task": task
                },
                timeout=30.0
            )
        await db.collection("requestProgress").update_one(
            {"requestId": requestId},
            {
                "$set": {
                    "status": RequestStatus.IN_PROGRESS,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": "N8N intialised successfully"
                }
            }
        )
        return N8nWorkflowResponse(
        http_status=HttpResponseEnum.OK
        )
    except Exception as e:
        await db.collection("requestProgress").update_one(

        {"requestId": requestId},
            {
                "$set": {
                    "status": RequestStatus.FAILED,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": f"{str(e)}"
                }
            }
        )
        return N8nWorkflowResponse(
            http_status=HttpResponseEnum.INTERNAL_SERVER_ERROR,
            error_message=str(e)
        )





