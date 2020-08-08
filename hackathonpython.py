from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/cases', methods=['POST'])
def cases():
    county = request.form['county']
    state = request.form['state']

    return '{},{}'.format(county,state)
    return render_template('cases.html',county = request.form['county'],state = request.form['state'])


@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
