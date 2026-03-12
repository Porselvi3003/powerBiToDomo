import zipfile
import json
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_raw_pbi_data(file_path):

    raw_output = {
        "fileContent": None,
        "layoutInput": None
    }

    try:
        with zipfile.ZipFile(file_path, 'r') as z:

            if "DataModelSchema" in z.namelist():
                with z.open("DataModelSchema") as f:
                    raw_bytes = f.read()
                    try:
                        raw_output["fileContent"] = json.loads(raw_bytes.decode("utf-16"))
                    except:
                        raw_output["fileContent"] = json.loads(raw_bytes.decode("utf-8"))

            if "Report/Layout" in z.namelist():
                with z.open("Report/Layout") as f:
                    raw_bytes = f.read()
                    try:
                        raw_output["layoutInput"] = json.loads(raw_bytes.decode("utf-16"))
                    except:
                        raw_output["layoutInput"] = json.loads(raw_bytes.decode("utf-8"))

        return raw_output

    except zipfile.BadZipFile:
        return {"error": "Invalid PBIT file"}


@app.post("/extract")
async def extract_pbit(file: UploadFile = File(...)):

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = extract_raw_pbi_data(tmp_path)

    return result