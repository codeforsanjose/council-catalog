from flask import Flask, render_template, redirect, request, make_response
from flask_cors import CORS
import json

app = Flask(__name__ , static_folder='templates/static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    #return render_template('static/index.html', name='index')
    return redirect('http://localhost:8080')

@app.route('/api/keyword', methods=['POST', 'OPTIONS'])
def minutes_search_route():
    print('getting here')
    print(request.form)
    return make_response(json.dumps([]))

if __name__ == '__main__':
    app.run(debug=True)


#https://github.com/dternyak/React-Redux-Flask
