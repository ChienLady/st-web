import requests

url = 'https://sheets.googleapis.com/v4/spreadsheets/{id}/values/{range}'

r = requests.get(url.format(id = '1rS51rM-NWMHfaC5JRqf5QZPr4epCXqlmWkD3hnpCJCQ', range = 'A29:B29'),
                 params = {'dateTimeRenderOption':'FORMATTED_STRING',
                           'majorDimension':'ROWS',
                           'valueRenderOption':'FORMATTED_VALUE'})

print(r)
