from datetime import datetime, date
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

if __name__ == '__main__':
    # query = "Plot the total, deaths and active cases in India, USA and Brazil between 3rd july and 5th august"
    query = "Plot the total, deaths and active cases in India, USA and Brazil"
    extract_parameters(project_id, 12345678, query)