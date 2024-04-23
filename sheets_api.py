# sheets_api.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_data_from_sheet(city):
    # Defina o escopo de acesso ao Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # Carregue as credenciais do arquivo
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # Abra a planilha e a aba específica por ID e nome
    sheet = client.open_by_key('your_spreadsheet_id').worksheet('Nome_da_Aba')

    # Pega todos os registros da planilha
    data = sheet.get_all_records()

    # Filtra os dados pela cidade, considerando a correspondência de case
    filtered_data = [row for row in data if row['Cidade'].lower() == city.lower()]

    return filtered_data