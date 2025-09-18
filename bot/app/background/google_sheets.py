import os
from typing import List, Any, Tuple
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.page.background import notify_export_finished


load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class GoogleSheetsClient:
    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self.service = self._get_service()
        self.sheet = self.service.spreadsheets()

    def _get_service(self):
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        return build("sheets", "v4", credentials=creds)

    def create_or_clear_sheet(self, sheet_name: str) -> None:
        """Создание нового листа или очистка существующего"""
        spreadsheet = self.sheet.get(spreadsheetId=self.spreadsheet_id).execute()
        existing_sheets = {s["properties"]["title"]: s["properties"]["sheetId"] for s in spreadsheet["sheets"]}

        if sheet_name not in existing_sheets:
            request_body = {
                "requests": [
                    {"addSheet": {"properties": {"title": sheet_name}}}
                ]
            }
            self.sheet.batchUpdate(spreadsheetId=self.spreadsheet_id, body=request_body).execute()
        else:
            self.sheet.values().clear(spreadsheetId=self.spreadsheet_id, range=sheet_name).execute()

    def get_sheet_url(self, sheet_name: str) -> str:
        """Получить URL вкладки по имени"""
        spreadsheet = self.sheet.get(spreadsheetId=self.spreadsheet_id).execute()
        for s in spreadsheet["sheets"]:
            if s["properties"]["title"] == sheet_name:
                gid = s["properties"]["sheetId"]
                return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit#gid={gid}"
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit"

    def append_rows(self, rows: List[List[Any]], sheet_name: str) -> dict:
        """Запись"""
        response = self.sheet.values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption="RAW",
            body={"values": rows}
        ).execute()

        updated_cells = response.get("updatedCells", 0)
        return updated_cells > 0


def prepare_task_rows(tasks: list) -> List[List[str]]:
    """Подготовка заголовков и строк для Google Sheets"""
    if not tasks:
        return []

    sample_task = tasks[0]
    headers = [k for k in sample_task.__dict__.keys() if not k.startswith("_")]
    rows = [headers]

    for t in tasks:
        row = []
        for h in headers:
            value = getattr(t, h)
            row.append(_serialize_value(value))
        rows.append(row)

    return rows


def _serialize_value(value: Any) -> str:
    """Сериализация значений для Google Sheets"""
    if value is None:
        return ""
    if hasattr(value, "isoformat"):
        return value.isoformat(sep=" ")
    if hasattr(value, "__dict__") and hasattr(value, "name"):
        return value.name
    return str(value)


async def background_export(user_id: int, tasks) -> Tuple[bool, str]:

    rows = prepare_task_rows(tasks)
    client = GoogleSheetsClient(SPREADSHEET_ID)
    client.create_or_clear_sheet(str(user_id))
    is_completed = client.append_rows(rows, str(user_id))
    url = client.get_sheet_url(str(user_id))
    
    await notify_export_finished(user_id, is_completed, url)
