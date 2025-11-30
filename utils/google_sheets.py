import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheetsError(Exception):
    """Raised when Google Sheets interaction fails."""


# Load environment variables before reading paths/IDs
load_dotenv()

# Spreadsheet configuration
SPREADSHEET_ID = os.getenv(
    "GOOGLE_SHEETS_ID",
    "1GJCz5exxiVOM1hCwOSJ-O-lL35k1yOUfA4jo40wPdgY",
)
WORKSHEET_NAME = os.getenv("GOOGLE_SHEETS_WORKSHEET", "Posts")


def _get_gspread_client() -> gspread.Client:
    """
    Creates an authorized gspread client using a service account.

    Expects a credentials.json file in the project root or a path
    specified via GOOGLE_SHEETS_CREDENTIALS environment variable.
    """
    credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")

    if not os.path.exists(credentials_path):
        raise GoogleSheetsError(
            f"Google Sheets credentials file not found: {credentials_path}. "
            f"Set GOOGLE_SHEETS_CREDENTIALS env var or place credentials.json in the project root."
        )

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_path, scopes
        )
        client = gspread.authorize(credentials)
    except Exception as exc:
        raise GoogleSheetsError(
            f"Failed to authorize Google Sheets client: {exc}"
        ) from exc

    return client


def append_post_row(
    topic: str,
    draft: str,
    final_post: str,
    total_tokens: Optional[int],
    cost: Optional[float],
) -> None:
    """
    Appends a new row to the Google Sheet.

    Columns:
        Timestamp | Topic | Draft (Writer) | Final Post (Editor) | Total Tokens | Cost
    """
    try:
        client = _get_gspread_client()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
    except Exception as exc:
        raise GoogleSheetsError(
            f"Failed to open spreadsheet or worksheet: {exc}"
        ) from exc

    timestamp = datetime.utcnow().isoformat()

    row = [
        timestamp,
        topic,
        draft,
        final_post,
        total_tokens if total_tokens is not None else "",
        cost if cost is not None else "",
    ]

    try:
        worksheet.append_row(row, value_input_option="RAW")
    except Exception as exc:
        raise GoogleSheetsError(
            f"Failed to append row to Google Sheets: {exc}"
        ) from exc
