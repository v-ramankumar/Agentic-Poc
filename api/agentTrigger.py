from fastapi import APIRouter, HTTPException
from db.models.requestModels.taskRequest import TaskRequest
from db.config.connection import get_db
import uuid

router = APIRouter()

@router.get("/planner-agent")
async def planner_agent(req:TaskRequest):
    """
    Endpoint to trigger the planner agent with a specific task.
    """
    db = await get_db()
    try:
        prompt  = req.task
        request_id = uuid.uuid4().hex
        ##
        db.re
        
    