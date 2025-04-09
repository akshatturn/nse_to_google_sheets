from fastapi import FastAPI
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = FastAPI()

@app.get("/update")
def update_sheet():
    try:
        # Step 1: Fetch data from NSE API
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0"}
        session.get("https://www.nseindia.com", headers=headers)
        res = session.get("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY", headers=headers)
        data = res.json()

        # Step 2: Google Sheets auth
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # For now using file — switch to env later
        creds = ServiceAccountCredentials.from_json_keyfile_name("secrets/service_account.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("NSE Option Chain").sheet1

        # Step 3: Write data to sheet
        rows = []
        for item in data["records"]["data"]:
            if "CE" in item:
                ce = item["CE"]
                rows.append([
                    ce.get("strikePrice"),
                    ce.get("openInterest"),
                    ce.get("changeinOpenInterest"),
                    ce.get("totalTradedVolume")
                ])
        sheet.clear()
        sheet.append_row(["Strike Price", "Open Interest", "Change in OI", "Volume"])
        for row in rows:
            sheet.append_row(row)

        return {"status": "success", "rows_written": len(rows)}

    except Exception as e:
        return {"status": "error", "message": str(e)}
