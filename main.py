import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def fetch_nse_data(symbol="NIFTY"):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.5"
    }
    session.get("https://www.nseindia.com", headers=headers)
    response = session.get(f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}", headers=headers)
    return response.json()

def update_google_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("secrets/service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("NSE Option Chain").sheet1

    rows = []
    for item in data['records']['data']:
        if 'CE' in item and item['CE']['expiryDate'] == data['records']['expiryDates'][0]:
            ce = item['CE']
            rows.append([
                ce.get('strikePrice'),
                ce.get('openInterest'),
                ce.get('changeinOpenInterest'),
                ce.get('totalTradedVolume')
            ])

    sheet.clear()
    sheet.append_row(["Strike Price", "Open Interest", "Change in OI", "Volume"])
    for row in rows:
        sheet.append_row(row)

if __name__ == "__main__":
    data = fetch_nse_data()
    update_google_sheet(data)
