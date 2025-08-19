from functions.table_files import PAYERS
from functions.schema import ResponseModel
from functions.table_files import pre_auth_req_data
import httpx

# ---------- PLACEHOLDER FUNCTION ----------
def pre_authorization_workflow(patient_id: str, payer: str):
    # TODO: Replace this with calling the
    # print(f"jsoonn : {pre_auth_req_data}")    
    return pre_auth_req_data

def get_payer_details(payer_name: str) -> dict | None:
    """Fetch payer details from the mocked PAYERS table."""
    for payer in PAYERS:
        if payer["payer_name"].lower() == payer_name.lower():
            return payer
    return None

# def trigger_n8n(patient_id: str, payer: str) -> dict:
#     """
#     Calls the pre_authorization_workflow() API and enriches its response 
#     with payer details from get_payer_details().
#     """
#     # Step 1: Call workflow API
#     workflow_data = pre_authorization_workflow(patient_id, payer)

#     # Step 2: Fetch payer details
#     payer_details = get_payer_details(payer)

#     # Step 3: Enrich response
#     enriched_response = {
#         "payer_details": payer_details,
#         "workflow_data": workflow_data
#     }
#     return enriched_response


def trigger_n8n(patient_id: str, payer: str) -> dict:
    """
    Calls pre_authorization_workflow(), enriches with payer details,
    then calls the /tools/trigger-n8n API (running on 8001) to trigger N8N.
    """
    # Step 1: Call workflow API
    workflow_data = pre_authorization_workflow(patient_id, payer)

    # Step 2: Fetch payer details
    payer_details = get_payer_details(payer)

    # Step 3: Prepare payload for /tools/trigger-n8n
    n8n_payload = {
        "request_id": "hfjhjh",
        "user_id": "system-user",  # <-- replace with actual user if available
        "patient_id": patient_id,
        "patient_name": "hvhvhvh",
        "payer_id": str(payer_details["payer_id"]),
        "prompt": "Pre-authorization request",  # or pass actual prompt
        "validated_json": workflow_data
    }

    # Step 4: Call the APIs service at port 8001
    try:
        with httpx.Client() as client:
            response = client.post(
                "http://127.0.0.1:8001/api/tools/trigger-n8n",
                json=n8n_payload,
                timeout=30.0
            )
            response.raise_for_status()
            n8n_response = response.json()
    except Exception as e:
        n8n_response = {"error": f"Failed to trigger N8N API: {str(e)}"}

    # Step 5: Combine and return enriched response
    enriched_response = {
        "n8n_response": n8n_response,
        "payer_details": payer_details,
        "workflow_data": workflow_data
    }
    return enriched_response


def handle_pre_authorization(Intent: str, patient_id: str, payer: str) -> ResponseModel:
    """Handles the pre-authorization intent logic and returns a ResponseModel with custom messages."""

    # Case 1: Both details missing
    if not patient_id and not payer:
        return ResponseModel(
            status="incomplete",
            message="Please provide patient_id and a valid payer name to proceed with pre-authorization.",
            Intent=Intent,
            patient_id=patient_id,
            payer=payer
        )

    # Case 2: Only patient_id missing
    if not patient_id:
        return ResponseModel(
            status="incomplete",
            message="Please provide patient_id to proceed with pre-authorization.",
            Intent=Intent,
            patient_id=patient_id,
            payer=payer
        )

    # Case 3: Only payer missing
    if not payer:
        return ResponseModel(
            status="incomplete",
            message="Please provide a valid payer name to proceed with pre-authorization.",
            Intent=Intent,
            patient_id=patient_id,
            payer=payer
        )

    # Case 4: All details present
    workflow_data = trigger_n8n(patient_id, payer)
    return ResponseModel(
        status="success",
        message="Thank you for the details, pre-authorization successfully proceeded.",
        Intent=Intent,
        patient_id=patient_id,
        payer=payer,
        data=workflow_data
    )
