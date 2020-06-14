## Imports
import json
# quick mess-around area for learning flask
# Using https://www.tutorialspoint.com/flask/flask_application.htm as reference

## Global defines
CONFIG_FILE='server_config.json'

from flask import Flask, redirect, url_for, request, render_template, session
app = Flask(__name__)

# needed to sign session date stored on the client.
app.config['SECRET_KEY'] = 'not a real secret'

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/ping')
def ping():
    return "Pong"

@app.route('/pizza')
def give_me_pizza():
    if not 'count' in session:
        session['count'] = 0
    session['count'] += 1
    return "Have some pizza! Count is {}".format(session['count'])

@app.route('/hello/<name>')
def say_hi(name):
    if name.lower() == 'pizza':
        # do a redirect to give_me_pizza
        return redirect(url_for('give_me_pizza'))
    return "Hello {}".format(name)

@app.route('/increment/<int:num>')
def increment(num):
    return '{}'.format(num + 1)

@app.route('/order', methods = ['POST', 'GET'])
def order():
    """ Dummy function to order pizza using static file serving
        and templates.
    """
    if request.method == 'POST':
        return render_template("order_placed.html", orders = request.form['orders'])
    if request.method == 'GET':
        return render_template("order_placed.html", orders = request.args.get('orders'))
    pass


def run_app(use_reloader=True):
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    app.run(debug=config['debug'], port=config['port'], host='0.0.0.0',
            use_reloader=use_reloader)


if __name__ == '__main__':
    run_app()
