from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def simpan_ke_csv(data):
    try:
        data.to_csv("data_fashions.csv", index=False)
        print('✅ Data berhasil disimpan ke file CSV.')
    except Exception as e:
        print(f"❌ Gagal menyimpan data ke CSV: {e}")

def simpan_ke_google_sheet(data):
    try:
        credential = Credentials.from_service_account_file(
            "utils/google-sheets-api.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        values = [data.columns.tolist()] + data.values.tolist()
        body = {'values': values}

        sheet.values().update(
            spreadsheetId="1eHLAZpOlinzONQszmmoHlGjASSKSy-HcuaSIlW14gaQ",
            range="Sheet1",
            valueInputOption='RAW',
            body=body
        ).execute()

        print('✅ Data berhasil disimpan ke Google Sheets.')
    except Exception as e:
        print(f"❌ Gagal menyimpan data ke Google Sheets: {e}")

def simpan_ke_postgresql(df):
    db_url = "postgresql+psycopg2://naomistg:naomi@localhost:5432/product"
    engine = create_engine(db_url)

    with engine.connect() as conn:
        df.to_sql(name="fashionstudio", con=conn, if_exists="append", index=False)
        print("✅ Data berhasil disimpan ke PostgreSQL.")
