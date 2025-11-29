import os
from datetime import datetime
from typing import Optional

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Spreadsheet and worksheet configuration
SPREADSHEET_ID = "1GJCz5exxiVOM1hCwOSJ-O-lL35k1yOUfA4jo40wPdgY"
WORKSHEET_NAME = "Posts"


def _get_gspread_client():
    """
    Creates an authorized gspread client using a service account.
    Expects a credentials.json file in the project root by default.
    """
    credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"Google Sheets credentials file not found: {credentials_path}. "
            f"Set GOOGLE_SHEETS_CREDENTIALS env var or place credentials.json in the project root."
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
):
    """
    Appends a new row to the Google Sheet with the given data.
    Columns:
        Timestamp | Topic | Draft (Writer) | Final Post (Editor) | Total Tokens
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
    ]

    worksheet.append_row(row, value_input_option="RAW")
