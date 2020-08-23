from flask import Flask, render_template, request, jsonify
from get_data import *

app = Flask(__name__)

@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')
    
@app.route('/qna')
def qna():
	return render_template('qna.html')

@app.route('/graph-data', methods=["POST"])
def graph_data():
    query_string = request.form.get('query')
    if not query_string:
        return "",400 #bad request

    parameters = extract_parameters(project_id, 12345678, query_string)
    if not parameters['categories']:
        return "",400
    
    # Get the dates_array
    dates_array = get_dates_array(parameters['start_date'], parameters['end_date'])
    datalist = [] #List of objects. each object has a 'title' and another array containing the numbers for the required stats
    # Add data for states
    for cur_state in parameters['states']:
        for cur_category in parameters['categories']:
            state_data = get_data_for_state(cur_state ,cur_category, dates_array)
            label = cur_state + " - " + cur_category
            datalist.append({
                'label': label,
                'data': state_data
            })

    # TODO: Implement for other countries and maybe districts?

    return_obj = {
        'dates_array': dates_array,
        'datalist': datalist
    }
    return jsonify(return_obj)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
