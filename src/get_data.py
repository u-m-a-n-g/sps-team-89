from datetime import datetime, date, timedelta
import json
import dialogflow_v2 as dialogflow

project_id = "summer20-sps-89"


def extract_parameters(project_id, session_id, text, language_code='en-US'):
    '''
    Extracts the parameters from the text and returns them in structured format.
    Returns the dictionary {
        'categories': categories, #list of categories (active-cases, total-cases)
        'states': states, #list of states (from India)
        'countries': countries, #list of countries
        'start_date': start_date, #date object representing start date.
        'end_date': end_date #date object representing end date.
    }
    '''
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    fields = response.query_result.parameters.fields

    categories = [x for x in fields['category'].list_value]
    states = [x for x in fields['state-india'].list_value]
    countries = [x for x in fields['geo-country'].list_value]
    dates_struct = fields['date-period'].struct_value
    if dates_struct:
        start_date_str = dates_struct.fields['startDate'].string_value
        start_date = datetime.date(datetime.fromisoformat(start_date_str))
        end_date_str = dates_struct.fields['endDate'].string_value
        end_date = datetime.date(datetime.fromisoformat(end_date_str))
        
        # Manually change year to 2020 as dialogflow parses 2021 for dates already passed.
        start_date = start_date.replace(year=2020)
        end_date = end_date.replace(year=2020)
    else:
        # default dates
        start_date = date.fromisoformat('2020-03-01')
        end_date = date.fromisoformat('2020-08-20')
    
    returnObj = {
        'categories': categories,
        'states': states,
        'countries': countries,
        'start_date': start_date,
        'end_date': end_date
    }
    return returnObj

def load_data(filename):
    with open(filename,'r') as f:
        data = json.load(f)
        return data
complete_state_data = load_data('data/data-india.json')
state_to_statecode = {
    "Andaman and Nicobar Islands": "AN",
    "Andhra Pradesh": "AP",
    "Arunachal Pradesh": "AR",
    "Assam": "AS",
    "Bihar": "BR",
    "Chandigarh": "CH",
    "Chhattisgarh": "CT",
    "Dadra and Nagar Haveli and Daman and Diu": "DN",
    "Delhi": "DL",
    "Goa": "GA",
    "Gujarat": "GJ",
    "Haryana": "HR",
    "Himachal Pradesh": "HP",
    "Jammu and Kashmir": "JK",
    "Jharkhand": "JH",
    "Karnataka": "KA",
    "Kerala": "KL",
    "Ladakh": "LA",
    "Madhya Pradesh": "MP",
    "Maharashtra": "MH",
    "Manipur": "MN",
    "Meghalaya": "ML",
    "Mizoram": "MZ",
    "Nagaland": "NL",
    "Odisha": "OR",
    "Puducherry": "PY",
    "Punjab": "PB",
    "Rajasthan": "RJ",
    "Sikkim": "SK",
    "Tamil Nadu": "TN",
    "Telangana": "TG",
    "Tripura": "TR",
    "Uttarakhand": "UT",
    "Uttar Pradesh": "UP",
    "West Bengal": "WB"
}

def get_dates_array(start_date, end_date):
    day_count = (end_date - start_date).days + 1
    dates_in_between = [ single_date.strftime("%Y-%m-%d") for single_date in (start_date + timedelta(n) for n in range(day_count))]
    return dates_in_between

def get_data_for_state(state, category, dates_array):
    '''
    dates_array is array of dates for which the statistics is required.
    returns an array with the statistics. (None if no data for that date).
    '''
    state_data = [None for _ in dates_array]
    # Handle invalid state
    if not (state in state_to_statecode):
        return state_data
    
    for i,cur_date in enumerate(dates_array):
        try:
            cur_date_stats = complete_state_data[cur_date][state_to_statecode[state]]['total']
            if category == 'active':
                state_data[i] = cur_date_stats['confirmed'] - cur_date_stats['deceased'] - cur_date_stats['recovered']
            elif category == 'deaths':
                state_data[i] = cur_date_stats['deceased']
            elif category == 'tests':
                state_data[i] = cur_date_stats['tested']
            else: # confirmed or recovered
                state_data[i] = cur_date_stats[category]
        except KeyError: #No data found for that date.
            pass #defaulted to None
    return state_data

if __name__ == '__main__':
    # query = "Plot the total, deaths and active cases in India, USA and Brazil between 3rd july and 5th august"
    query = "Plot the confirmed cases for MP between 2nd April and 6th May"
    parameters = extract_parameters(project_id, 12345678, query)
    dates_array = get_dates_array(parameters['start_date'], parameters['end_date'])
    state_data = get_data_for_state(parameters['states'][0] , parameters['categories'][0], dates_array)
