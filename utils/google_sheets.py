import os
from datetime import datetime
from typing import Optional

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Spreadsheet configuration:
# Insert your real spreadsheet ID:
# https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit
SPREADSHEET_ID = "1GJCz5exxiVOM1hCwOSJ-O-lL35k1yOUfA4jo40wPdgY"
WORKSHEET_NAME = "Posts"


def _get_gspread_client():
    """
    Creates an authorized gspread client using a service account.
    Expects a credentials.json file in the project root or a path
    specified via GOOGLE_SHEETS_CREDENTIALS environment variable.
    """
    credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Google Sheets credentials file not found: {credentials_path}. "
            f"Place credentials.json in the root or set GOOGLE_SHEETS_CREDENTIALS env var."
        )

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_path, scopes
    )
    client = gspread.authorize(credentials)
    return client


def append_post_row(
    topic: str,
    draft: str,
    final_post: str,
    total_tokens: Optional[int],
    cost: Optional[float],
):
    """
    Appends a new row to the Google Sheet.

    Expected columns:
        Timestamp | Topic | Draft (Writer) | Final Post (Editor) | Total Tokens | Cost
    """
    client = _get_gspread_client()
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

    timestamp = datetime.utcnow().isoformat()

    row = [
        timestamp,
        topic,
        draft,
        final_post,
        total_tokens if total_tokens is not None else "",
        cost if cost is not None else "",
    ]

    worksheet.append_row(row, value_input_option="RAW")
