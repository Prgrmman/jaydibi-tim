# quick mess-around area for learning flask
# Using https://www.tutorialspoint.com/flask/flask_application.htm as reference


from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/pizza')
def give_me_pizza():
    return 'Have some pizza!'

def meta_test(count):
    """
    Just a stupid decorator that takes a parameter
    I'm trying to see what I can do with it
    """
    def decorate(func):
        def inner(*args, **kwargs):
            for i in range(count):
                print('run the function {}'.format(i))
                func(*args, **kwargs)
        return inner
    return decorate
                


# actually run the script
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
