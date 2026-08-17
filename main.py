from fastapi import FastAPI, UploadFile, File
import pandas as pd
from io import BytesIO

import requests

API_URL = "http://192.168.1.80/openmrs/admin/concepts/conceptDrug.form"

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

        url = "http://192.168.1.8/openmrs/admin/concepts/conceptDrug.form"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        cookies = {
            "JSESSIONID": "E4ACCD8BAB6412575FC73E28468174D6",
            "OWASP-CSRFTOKEN": "6ZL5-365R-KHT5-OGQQ-N5S3-W98J-2Z90-3OUF"
        }

        data = {
            "OWASP-CSRFTOKEN": "6ZL5-365R-KHT5-OGQQ-N5S3-W98J-2Z90-3OUF",
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
                timeout=30
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

        url = "http://192.168.1.8/openmrs/ws/rest/v1/concept"

        username = "admin"
        password = "Admin123"


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
                auth=(username, password),
                json=data,
                timeout=30
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

        url = "http://192.168.1.8/openmrs/ws/rest/v1/drug"

        username = "admin"
        password = "Admin123"


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
                auth=(username, password),
                json=data,
                timeout=30
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
