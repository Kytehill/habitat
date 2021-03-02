from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Andrew'}
    environments = [
        {
            'environment': {'name': 'environment1'},
            'servers': ['server1', 'server2', 'server3']
        },
        {
            'environment': {'name': 'envrionment2'},
            'servers': ['server4', 'server5', 'server6']
        }
    ]
    return render_template('index.html', title='Home', user=user, environments=environments)
