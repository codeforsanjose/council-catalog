import pandas
import json

from flask import Flask, render_template, redirect, request, make_response
from flask_cors import CORS

minutes_from_file = pandas.read_json('./htmlgrabber_output.json')
app = Flask(__name__ , static_folder='templates/static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    #return render_template('static/index.html', name='index')
    return redirect('http://localhost:8080')

@app.route('/api/keyword', methods=['POST', 'OPTIONS'])
def minutes_search_route():
    print(request.form)
    data = [posted_data for posted_data in request.form.keys()]
    keyword = json.loads(data[0])['keyword']
    import pdb; pdb.set_trace()
    #m['2017-08-29 00:00:00']['content'] will get the content for the date, thanks Matt
    meetings_found = []
    response_data = {
        'keyword': keyword,
        'found_meetings': meetings_found
    }
    return make_response(json.dumps(response_data))

def navigate_through_minutes_panda(keyword):
    meeting_minutes_with_keyword = []
    for timestamp in minutes_from_file.keys():
        search_through_content(keyword, timestamp)

def search_through_content(keyword, timestamp_key):
    content_to_search = minutes_from_file[timestamp_key]['content']


if __name__ == '__main__':
    app.run(debug=True)


#https://github.com/dternyak/React-Redux-Flask
