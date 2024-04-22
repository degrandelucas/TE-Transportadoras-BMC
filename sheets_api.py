# sheets_api.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_data_from_sheet(city):
    scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key('1FQOiNWM1ChoaLKK5a-26PvZDUo_iI993').worksheet('BASE')

    data = sheet.get('D:K')  # Obtém todas as linhas nas colunas D a K
    filtered_data = [row for row in data if row[0].lower() == city.lower()]
    return filtered_data