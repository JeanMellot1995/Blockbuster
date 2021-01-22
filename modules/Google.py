import datetime
import os
import pickle

import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build

CLIENT_SECRET_FILE = "credentials.json"
API_SERVICE_NAME = "sheets"
API_VERSION = "v4"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep="-")
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f"token_{API_SERVICE_NAME}_{API_VERSION}.pickle"
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, "wb") as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, "service created successfully")
        return service
    except Exception as e:
        print(e)
    return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + "Z"
    return dt


def fetch_excel(sheetId, sheetname, ranges):
    service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

    request = (
        service.spreadsheets()
        .values()
        .batchGet(spreadsheetId=sheetId, ranges=sheetname + "!" + ranges)
    )
    response = request.execute()

    values = response["valueRanges"][0]["values"]
    prev_data = pd.DataFrame(data=values, columns=values[0])
    prev_data.fillna("", inplace=True)
    prev_data = prev_data[1:].reset_index(drop=True)
    return prev_data


def export_data_to_sheets(df, spreadsheetId, sheetname, with_column):
    service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

    if with_column == True:
        columns = {}
        for c in df.columns:
            columns[c] = c.title()

        df.rename(columns=columns, inplace=True)
        df_list = df.T.reset_index().T.values.tolist()
        sheet_range = sheetname + "!A1:BA"
    else:
        print(df.columns)
        print(chr(ord("@") + len(df.columns.values)))
        df_list = df.T.reset_index().T.values.tolist()[1:]
        sheet_range = sheetname + "!A2:" + "BA"

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        valueInputOption="USER_ENTERED",
        range=sheet_range,
        body=dict(majorDimension="ROWS", values=df_list),
    ).execute()
    print("{} Sheet Updated!".format(sheetname))


def append_Data_To_Sheets(df, spreadsheetId, sheetname, sheetrange):
    service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId,
        valueInputOption="USER_ENTERED",
        range=sheetname + "!" + sheetrange,
        body=dict(
            majorDimension="ROWS", values=df.T.reset_index().T.values.tolist()[1:]
        ),
    ).execute()
    print("{} Sheet Updated!".format(sheetname))


def fill_columns_in_sheets(df, spreadsheetId, sheetname, sheet_range):
    service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
    df_list = df.T.reset_index().T.values.tolist()[1:]
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        valueInputOption="USER_ENTERED",
        range=sheetname + "!" + sheet_range,
        body=dict(majorDimension="ROWS", values=df_list),
    ).execute()
    print("{} Sheet Updated!".format(sheetname))
