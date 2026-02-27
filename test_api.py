import requests

url = "http://localhost:8004/api/ingestion/doc/batch-details"

payload = [{
    "OffenderNumber": "1234567",
    "Location": "Test State Pen",
    "Offense": "TESTING",
    "TDD_SDD": None,
    "CommitmentDate": "2024-01-01T00:00:00",
    "RecallDate": None,
    "InterviewDate": None,
    "MandatoryMinimum": None,
    "DecisionType": None,
    "Decision": None,
    "DecisionDate": None,
    "EffectiveDate": None,
    "Charges": []
}]

try:
    r = requests.post(url, json=payload)
    print("Status Code:", r.status_code)
    print("ResponseText:", r.text)
except Exception as e:
    print("Error:", e)
