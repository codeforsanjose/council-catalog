import pandas
import json
import calendar

from flask import Flask, render_template, redirect, request, make_response
from flask_cors import CORS

minutes_from_file = pandas.read_json('./htmlgrabber_output.json')
app = Flask(__name__ , static_folder='templates/static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    #return render_template('static/index.html', name='index')
    return redirect('http://localhost:8080')

def get_posted_data_from_request():
    data = [posted_data for posted_data in request.form.keys()]
    return json.loads(data[0])

@app.route('/api/keyword', methods=['POST', 'OPTIONS'])
def minutes_search_route():
    posted_data = get_posted_data_from_request()
    keyword = posted_data['keyword']
    meetings_found = navigate_through_minutes_panda(keyword)
    response_data = {
        'keyword': keyword,
        'found_meetings': meetings_found
    }
    return make_response(json.dumps(response_data))

def navigate_through_minutes_panda(keyword):
    meeting_minutes_with_keyword = []
    for timestamp in minutes_from_file.keys():
        meeting_found = search_through_content(keyword, timestamp)
        if meeting_found is not None:
            meeting_minutes_with_keyword.append(meeting_found)
    return meeting_minutes_with_keyword

def search_through_content(keyword, timestamp_key):
    content_to_search = minutes_from_file[timestamp_key]['content'].lower()
    pretty_date = timestamp_key.strftime('%B %d, %Y')
    keyword = keyword.lower()
    if keyword in content_to_search:
        return {
            'timestamp': pretty_date,
            'meeting_content': content_to_search
        }
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)


#https://github.com/dternyak/React-Redux-Flask
