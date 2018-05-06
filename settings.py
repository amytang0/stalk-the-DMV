SLACK_CHANNEL = '#dmv' # this should be the slack channel which you want to send messages to
URL = 'https://www.dmv.ca.gov/wasapp/foa/clear.do?goTo=officeVisit' # the url for the DMV web form
LOCATIONS = {
    #'San Mateo': '130'
    'San Mateo': '130', # the office ID obtained by inspecting the xpath, this is what selenium uses to identify the correct option
    'Redwood City': '108',
    'Daly City': '28',
    'Santa Clara': '133',
    'San Francisco:': '123',
    'San Jose': '124',
    'Fremont': '41',
    'Oakland Claremont': '86',
    'Oakland Coliseum': '87',
}
PROFILE = {
    'first_name': 'AMY',
    'last_name': 'TANG',
    'mm': '01',
    'dd': '01',
    'yyyy': '1993',
    'dl_number': 'F12345',
    'tel_prefix': '510',
    'tel_suffix1': '123',
    'tel_suffix2': '1234'
    # format: (area-code) prefix - lineNumber
}

