from datetime import datetime
from fastapi import APIRouter, Query, Path

from db.config.connection import get_db
from db.models.dbmodels.requestProgress import RequestStatus
from db.models.dbmodels.utility.httpResponseEnum import HttpResponseEnum

router = APIRouter()

@router.get("/payers/{payer_id}")
async def get_payer(
    payer_id: str = Path(..., description="Payer ID to fetch"),
    request_id: str = Query(..., description="Request ID for validation")
):
    """
    Endpoint to retrieve payer information by payer_id and request_id.
    """
    db = await get_db()
    try:
        payer = await db.collection("priorAuthPayers").find_one({"id": payer_id})
        if payer:
            await db.collection("requestProgress").update_one(
                {"requestId": request_id},
                {
                    "$set": {
                        "status": RequestStatus.VALIDATED,
                        "lastUpdatedAt": datetime.now(),
                        "remarks": "Payer validated successfully"
                    }
                }
            )
            return {"status": HttpResponseEnum.OK, "message": "Payer validated successfully"}
        else:
            return {"status": HttpResponseEnum.NOT_FOUND, "message": "Payer not found"}
    except Exception as e:
        await db.collection("requestProgress").update_one(
            {"requestId": request_id},
            {
                "$set": {
                    "status": RequestStatus.FAILED,
                    "lastUpdatedAt": datetime.now(),
                    "remarks": str(e)
                }
            }
        )
        return {"status": HttpResponseEnum.INTERNAL_SERVER_ERROR, "message": str(e)}
