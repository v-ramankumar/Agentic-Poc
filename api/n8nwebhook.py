import os
from datetime import datetime
from fastapi import APIRouter
from httpx import AsyncClient

from db.config.connection import get_db
from db.models.dbmodels.requestProgress import RequestStatus
from db.models.dbmodels.utility.httpResponseEnum import HttpResponseEnum
from db.models.requestmodels.n8nWebhookRequest import n8nWebhookRequest
from db.models.responseModels.n8nWorkflowResponse import N8nWorkflowResponse
from db.models.dbmodels.priorAuthRequest import priorAuthRequest  # <-- import model

router = APIRouter()


@router.post("/n8n-webhook")
async def n8n_webhook(req: n8nWebhookRequest):
    db = await get_db()
    requestId = req.requestId
    json_data = req.json_data
    payer_id = req.payer_id
    task = req.task

    try:
        # Forward request to N8N webhook
        async with AsyncClient() as client:
            response = await client.post(
                os.getenv("N8N_WEBHOOK_URL"),
                json={
                    "requestId": requestId,
                    "json_data": json_data,
                    "payer_id": payer_id,
                    "task": task,
                },
                timeout=30.0,
            )

        # Build priorAuthRequest document
        prior_auth_doc = priorAuthRequest(
            requestId=requestId,
            userId=req.userId,          # make sure n8nWebhookRequest has this field
            patientId=req.patientId,    # make sure it exists
            patientName=req.patientName,
            payerId=req.payerId,
            createdAt=datetime.now(),
            lastUpdatedAt=datetime.now(),
        )

        # Insert into priorAuthRequest collection
        await db.collection("priorAuthRequest").insert_one(prior_auth_doc.dict())

        # Update requestProgress collection
        await db.collection("requestProgress").update_one(
            {"requestId": requestId},
            {
                "$set": {
                    "status": RequestStatus.IN_PROGRESS,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": "N8N initialised successfully",
                }
            },
        )

        return N8nWorkflowResponse(http_status=HttpResponseEnum.OK)

    except Exception as e:
        await db.collection("requestProgress").update_one(
            {"requestId": requestId},
            {
                "$set": {
                    "status": RequestStatus.FAILED,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": f"{str(e)}",
                }
            },
        )
        return N8nWorkflowResponse(
            http_status=HttpResponseEnum.INTERNAL_SERVER_ERROR,
            error_message=str(e),
        )
