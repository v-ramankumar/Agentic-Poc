from functions.table_files import PAYERS
from functions.schema import ResponseModel
from functions.table_files import pre_auth_req_data

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

def enrich_pre_authorization_response(patient_id: str, payer: str) -> dict:
    """
    Calls the pre_authorization_workflow() API and enriches its response 
    with payer details from get_payer_details().
    """
    # Step 1: Call workflow API
    workflow_data = pre_authorization_workflow(patient_id, payer)

    # Step 2: Fetch payer details
    payer_details = get_payer_details(payer)

    # Step 3: Enrich response
    enriched_response = {
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
    workflow_data = enrich_pre_authorization_response(patient_id, payer)
    return ResponseModel(
        status="success",
        message="Thank you for the details, pre-authorization successfully proceeded.",
        Intent=Intent,
        patient_id=patient_id,
        payer=payer,
        data=workflow_data
    )
