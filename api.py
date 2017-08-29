from flask import Flask, render_template, redirect

app = Flask(__name__ , static_folder='templates/static', template_folder='templates')

@app.route('/')
def index():
    #return render_template('static/index.html', name='index')
    return redirect('http://localhost:8080')

if __name__ == '__main__':
    app.run(debug=True)
