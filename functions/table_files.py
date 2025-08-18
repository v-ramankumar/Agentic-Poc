
# Payers table
PAYERS = [
    {
        "payer_id": 1,
        "payer_name": "cohere",
        "payer_url": "https://portal.cohere.com", 
        "payer_credentials" : {"userid":"abc", "password": "123"}
    },
    {
        "payer_id": 2,
        "payer_name": "humana",
        "payer_url": "https://www.humana.com",
        "payer_credentials" : {"userid":"efg", "password": "456"}
    }
]


pre_auth_req_data ={
  "response": [
    {
      "requestid": "4473",
      "appointmentid": "158231849-1",
      "appointmentdate": "10/27/2025 6:00:00 PM",
      "caseid": "12345873",
      "visittype": "Subsequent",
      "authorizationtype": "Initial",
      "clientspecialty": "Radiology",
      "providerfirstname": "JANE",
      "providerlastname": "DOE",
      "providernpi": "1111111111",
      "providershortcode": "",
      "providerphone": "",
      "provideraddress1": "TEST ADDRESS",
      "provideraddress2": "",
      "providercity": "TEST CITY",
      "providerstate": "NY",
      "providerzip": "10510",
      "providercountry": "USA",
      "subscriberfirstname": "JOHN",
      "subscriberlastname": "DOE",
      "subscriberaddress1": "TEST",
      "subscriberaddress2": "",
      "subscribercity": "TEST",
      "subscriberstate": "NY",
      "subscriberzip": "10562",
      "subscribercountry": "US",
      "subscriberdateofbirth": "10/XX/19XX 12:00:00 AM",
      "subscribergender": "Male",
      "subscriberrelationship": "Self",
      "subscriberrelationshipcode": "18",
      "ediservicecode": "",
      "patientfirstname": "JOHN",
      "patientlastname": "DOE",
      "patientdateofbirth": "XX/XX/19XX 12:00:00 AM",
      "personnumber": "XXX-1111111",
      "patientaddress1": "TEST",
      "patientaddress2": "",
      "patientcity": "TEST",
      "patientstate": "NY",
      "patientzip": "10562",
      "patientcountry": "US",
      "gender": "Male",
      "payername": "FIDELIS MEDICAID",
      "payerid": "350007",
      "policynumber": "<POLICY NUMBER>",
      "locationcode": "NY",
      "locationname": "<FACILITY NAME>",
      "locationaddress1": "<FACILITY ADDRESS>",
      "locationaddress2": "",
      "locationcity": "CITY",
      "locationstate": "NY",
      "locationzip": "10549",
      "locationcountry": "USA",
      "facilitynpi": "11111111111",
      "providergrouptaxid": "1111211111",
      "placeofservice": "11",
      "mandatorydocuments": "",
      "additionaldocuments": "",
      "contactname": "<contact name>",
      "contactphone": "888-868-4102",
      "contactfax": "(469) 466-6178",
      "dxcodes": "E66.9,E78.2,Z00.01,I25.10,Z87.891",
      "cptcodes": "71271",
      "procedurecodes": [
        {
          "code": "71271",
          "unit": "1",
          "modifiercode": "",
          "diagnosiscode": ""
        }
      ],
      "totalprocedurecodes": 1,
      "category": "PA_CMM_Epic_Radiology_FIdelis_AS",
      "followupdate": "8/5/2025 2:14:23 AM",
      "clientname": "CLIENT NAME",
      "enterpriseid": "CLIENT ID",
      "enterprisename": "ENTERPRISE NAME",
      "vendorname": "EVICORE",
      "subsupportedmedium": "BROWSER",
      "encounterid": "",
      "other": {
        "other1": {
          "other_que": "Auth Submission Comments",
          "other_ans": "Good"
        },
        "other2": {
          "other_que": "Spoke_To",
          "other_ans": ""
        },
        "other3": {
          "other_que": "Contact Email",
          "other_ans": "test@IKSHEALTH.com"
        },
        "other4": {
          "other_que": "Facility TIN",
          "other_ans": "1211111111"
        },
        "other5": {
          "other_que": "IKS Specialty",
          "other_ans": "Radiology"
        },
        "other6": {
          "other_que": "Client Visit Reason",
          "other_ans": "IMG200A - LDCT LUNG SCREENING"
        },
        "other7": {
          "other_que": "IKS Visit Reason",
          "other_ans": "IMG200A - LDCT LUNG SCREENING"
        },
        "other8": {
          "other_que": "Platform",
          "other_ans": "EVICORE Portal"
        },
        "other9": {
          "other_que": "POS Description",
          "other_ans": "Location, other than a hospital, skilled nursing facility (SNF), military treatment facility, community health center, State or local public health clinic, or intermediate care facility (ICF), where the health professional routinely provides health examinations, diagnosis, and treatment of illness or injury on an ambulatory basis."
        },
        "other10": {
          "other_que": "Order Type",
          "other_ans": "Traditional"
        },
        "other11": {
          "other_que": "Ordering Provider ID",
          "other_ans": "xxxxxx"
        },
        "other12": {
          "other_que": "Ordering Provider FName",
          "other_ans": "JOHN"
        },
        "other13": {
          "other_que": "Ordering Provider LName",
          "other_ans": "DOE"
        },
        "other14": {
          "other_que": "Ordering Provider NPI",
          "other_ans": "11111111"
        },
        "other15": {
          "other_que": "Ordering Provider TIN",
          "other_ans": ""
        },
              "other17": {
          "other_que": "Last Worked By",
          "other_ans": "EVE-Autonomous"
        },
        "other18": {
          "other_que": "UserName",
          "other_ans": "System"
        },
        "other19": {
          "other_que": "Previous Auth Notes",
          "other_ans": ""
        }
      },
      "casereferencenumber": "test-1",
      "snapshotofauth": "",
      "authstatus": "",
      "payerresponsedocument": "",
      "authid": "",
      "authstartdate": "",
      "authenddate": "",
      "totalnumberofvisit": "1",
      "denialreason": "",
      "denialresponsenumber": "",
      "denialdate": "",
      "effectivedate": "10/27/2025 6:00:00 PM",
      "questionnaire": {},
      "documents": {},
      "taskassignment": {
        "document1": {
          "name": "",
          "assignedto": "No"
        }
      },
      "authnotes": ""
    }
  ]
}