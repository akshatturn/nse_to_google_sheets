# NSE Option Chain to Google Sheets

This project fetches option chain data from NSE and updates a Google Sheet.

## Setup
1. Create a service account and enable Google Sheets API.
2. Download the `service_account.json` and place it in the `secrets` folder.
3. Share the target Google Sheet with the service account email.

## Deploy on Render
- Use the `render.yaml` to deploy as a Background Worker.
