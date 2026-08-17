from fastapi import FastAPI, UploadFile, File
import pandas as pd
from io import BytesIO
import yaml
import os

import requests

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

baseurl = config['baseurl']
CSRF_TOKEN = config['auth']['csrf_token']
SESSION_ID = config['auth']['session_id']
AUTH_USERNAME = config['auth']['username']
AUTH_PASSWORD = config['auth']['password']
REQUEST_TIMEOUT = config['request']['timeout']


app = FastAPI()

@app.post("/upload-drugs")
async def upload_drugs(file: UploadFile = File(...)):
    # Read uploaded Excel file
    contents = await file.read()

    # Convert Excel to DataFrame
    df = pd.read_excel(BytesIO(contents))

    # Convert DataFrame to JSON
    exceldata = df.to_dict(orient="records")

    for index, row in df.iterrows():

        row_number = index + 2  # +2 because Excel has header row
        # print(row)

        url = f"{baseurl}{config['api']['concepts_drug']}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        cookies = {
            "JSESSIONID": SESSION_ID,
            "OWASP-CSRFTOKEN": CSRF_TOKEN
        }

        data = {
            "OWASP-CSRFTOKEN": CSRF_TOKEN,
            "name": row["536.1"],
            "concept": "4256",
            "concept_other": "",
            "_combination": "",
            "dosageForm": "",
            "dosageForm_other": "",
            "strength": "",
            "minimumDailyDose": "",
            "maximumDailyDose": "",
            "phrase": ""
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                cookies=cookies,
                data=data,
                timeout=REQUEST_TIMEOUT
            )

            if response.ok:
                print(f"SUCCESS - Excel row {response.text}")
            else:
                print(
                    f"FAILED - Excel row {row_number} "
                    f"- HTTP {response.status_code} "
                    f"- {response.text}"
                )

        except requests.exceptions.RequestException as e:
            print(f"ERROR - Excel row {row_number} - {e}")

    return {
        "filename": file.filename,
        "data": exceldata
    }


select_items = {
    "Test": 1,
    "Procedure": 2,
    "Drug": 3,
    "Diagnosis": 4,
    "Finding": 5,
    "Anatomy": 6,
    "Question": 7,
    "LabSet": 8,
    "MedSet": 9,
    "ConvSet": 10,
    "Misc": 11,
    "Symptom": 12,
    "Symptom/Finding": 13,
    "Specimen": 14,
    "Misc Order": 15,
    "Frequency": 16,
    "Pharmacologic Drug Class": 17,
    "Units of Measure": 18,
    "Workflow": 19,
    "State": 20,
    "Program": 21,
    "Indicator": 22,
    "Organism": 23,
    "Radiology/Imaging Procedure": 24,
    "Drug form": 25,
    "InteractSet": 26,
    "Medical supply": 27
}


@app.post("/upload-concent")
async def upload_concent(file: UploadFile = File(...)):
    # Read uploaded Excel file
    contents = await file.read()

    # Convert Excel to DataFrame
    df = pd.read_csv(BytesIO(contents))

    for index, row in df.iterrows():

        row_number = index + 2  # +2 because Excel has header row
        print(f"Row {index + 1}:")
        print(row.to_dict())

        url = f"{baseurl}{config['api']['concept']}"


        data = {
  "names": [
    {
      "name": "Drug-New-Concept",
      "locale": "en",
      "conceptNameType": "FULLY_SPECIFIED"
    }
  ],
  "datatype": "8d4a4c94-c2cc-11de-8d13-0010c6dffd0f",
  "conceptClass": "8d490dfc-c2cc-11de-8d13-0010c6dffd0f"
}


        print(data)
        try:
            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json"
                },
                auth=(AUTH_USERNAME, AUTH_PASSWORD),
                json=data,
                timeout=REQUEST_TIMEOUT
            )

            if response.ok:
                print(f"SUCCESS - Excel row {response.text}")
            else:
                print(
                    f"FAILED - Excel row {row_number} "
                    f"- HTTP {response.status_code} "
                    f"- {response.text}"
                )

        except requests.exceptions.RequestException as e:
            print(f"ERROR - Excel row {row_number} - {e}")

        if row_number >= 2:
            break

    return {
        "filename": file.filename,
        "data": []
    }


@app.post("/upload-new-drug")
async def upload_new_drug(file: UploadFile = File(...)):
    # Read uploaded Excel file
    contents = await file.read()

    # Convert Excel to DataFrame
    df = pd.read_excel(BytesIO(contents))

    for index, row in df.iterrows():

        row_number = index + 2  # +2 because Excel has header row
        print(f"Row {index + 1}:")
        print(row.to_dict())

        url = f"{baseurl}{config['api']['drug']}"


        data = {
                "name": "Paracetamol new 500mg tablet",
                "concept": "fd77ec55-5c3b-45da-989f-7999c897a7d6",
                "dosageForm": "",#"8d4a4ab4-c2cc-11de-8d13-0010c6dffd0f",
                "strength": "500mg",
                "combination": False
            }



        print(data)
        try:
            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json"
                },
                auth=(AUTH_USERNAME, AUTH_PASSWORD),
                json=data,
                timeout=REQUEST_TIMEOUT
            )

            if response.ok:
                print(f"SUCCESS - Excel row {response.text}")
            else:
                print(
                    f"FAILED - Excel row {row_number} "
                    f"- HTTP {response.status_code} "
                    f"- {response.text}"
                )

        except requests.exceptions.RequestException as e:
            print(f"ERROR - Excel row {row_number} - {e}")

        if row_number >= 2:
            break

    return {
        "filename": file.filename,
        "data": []
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
