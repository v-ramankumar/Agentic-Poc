from fastapi import APIRouter

from db.models.requestmodels import n8nRequestListener

router = APIRouter()
@router.post("/n8n/listen")
async def n8n_request_listener(req:n8nRequestListener):
    requestId = req.requestId
    payerId = req.payerId
    error = req.error or ""
    message = req.message or ""


