## Imports
import json
# quick mess-around area for learning flask
# Using https://www.tutorialspoint.com/flask/flask_application.htm as reference

## Global defines
CONFIG_FILE='server_config.json'

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/ping')
def ping():
    return 'Pong'

@app.route('/pizza')
def give_me_pizza():
    return 'Have some pizza!'

def run_app(use_reloader=True):
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    app.run(debug=config['debug'], port=config['port'], host='0.0.0.0',
            use_reloader=use_reloader)


if __name__ == '__main__':
    run_app()
