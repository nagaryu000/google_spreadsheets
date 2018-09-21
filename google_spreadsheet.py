from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

"""
if you use the sheet as readonly, modify SCOPES below.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
"""
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

SAMPLE_SPREADSHEET_ID = '19VLdM-93NlakG76RLNXQSXhmGowOU0NQcmmHgxAxCW8'
SAMPLE_RANGE_NAME = 'シート1!A1:E7'

def gs_read():
    """Show basic usage of the Sheet API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    SPREADSHEET_ID = '19VLdM-93NlakG76RLNXQSXhmGowOU0NQcmmHgxAxCW8'
    RANGE_NAME = 'シート1!A1:E7'
    
    # get values from the 'シート1!A1:E7'.
    single_result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = single_result.get('values', [])

    if not values:
        print('No data found.')
    else:
        # print('あ行, か行, さ行, た行, な行:')
        for row in values:
            print('%s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[3] ,row[4]))
    # multiplus ranges
    RANGE_NAMES = [
        'シート1!A1:E',
        'シート2!A1:Z',
    ]
    multiple_result = service.spreadsheets().values().batchGet(
        spreadsheetId=SPREADSHEET_ID, ranges=RANGE_NAMES).execute()
    print('{0} ranges retrieved.'.format(multiple_result.get('valueRanges')))

def gs_write():
    """
    one s
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    SPREADSHEET_ID = '19VLdM-93NlakG76RLNXQSXhmGowOU0NQcmmHgxAxCW8'
    RANGE_NAME = 'シート1!A1:E7'
    value_input_option = 'RAW'

    values = [
        [
            # cell values
            'practice to write something to the cell from Python script.'
        ],
            # additional rows
    ]
        
    body = {
        'values': values
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption=value_input_option, body=body
    ).execute()
    print('{0} cells updated.'.format(result.get('updateCells')))

if __name__ == '__main__':
    gs_read()
    gs_write()
