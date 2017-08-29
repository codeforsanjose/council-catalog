from flask import Flask, render_template

app = Flask(__name__ , static_folder='./templates/statuc', template_folder='./templates')

@app.route('/')
def index():
    return render_template('static/index.html', name='index')


if __name__ == '__main__':
    app.run(debug=True)
