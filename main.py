# Imports
from flask import Flask, Response
from flask_cors import CORS
from flask import request
from flask import jsonify
from flask import Flask, render_template, request, session
import time

# Defining the Flask APP and Setting up the
# Cross-Origin Resource Policy for the web-based front_end
app = Flask(__name__, static_folder="static")
CORS(app)

class Calculator:
    def __init__(self):
        self.last_valid_request_timestamp = 0
        self._MAX_CONSECUTIVE_ATTEMPTS = 5
        self._TIMEOUT_INTERVAL_SECONDS = 30
        self.notes = []
        self.block_requests = False
        self.log = ""
    
    def local_log_message(self):
        # Create log file
        logging_fname = f"logs/calculator_log_{time.time()}.txt"
        f = open(logging_fname, "x")
        f.close()

        # Save log file
        f = open(logging_fname, "a")
        f.write(self.log)
        f.close()

        self.log = ""

    def is_timeout_completed(self):
        return int(time.time() - self.last_valid_request_timestamp) > self._TIMEOUT_INTERVAL_SECONDS

    def calculate_output(self):
        ans = ans_expr = ""

        # If the maximum number of consecutive requests was reached but the timeout interval has passed, reset the requests count
        if len(self.notes) > self._MAX_CONSECUTIVE_ATTEMPTS and self.is_timeout_completed():
            self.notes.clear()
            self.block_requests = False
        
        # If the maximum number of consecutive requests haven't been made, fulfill the request
        if len(self.notes) < self._MAX_CONSECUTIVE_ATTEMPTS:
            expr = request.form['expression']

            # Best-effort to evaluate the input expression
            try:
                ans = str(eval(expr))
                ans_expr = f"{expr} = {ans}"
            except:
                ans_expr = ans = "Invalid syntax!"
            
            print(f"{expr} = {ans}")
            self.log += ans_expr + "\n"
            
            # Add message to log list for client
            self.notes.append(ans_expr)

            # Start a timer by recording the timestamp of the last valid consecutive request
            if len(self.notes) == self._MAX_CONSECUTIVE_ATTEMPTS - 1:
                self.last_valid_request_timestamp = time.time()
        elif not self.block_requests:
            self.block_requests = True
            self.notes.append("You have reached your maximum limit, please wait for 30 seconds")
        
        return ans

calculator = Calculator()

@app.route('/', methods=['GET', 'POST'])
def home():
    # If the webpage is being requested for the first time
    if request.method == 'GET':
        return render_template('index.html')

    ans = calculator.calculate_output()
    return render_template('index.html', entry=ans, logs = calculator.notes, L=len(calculator.notes),ip = request.remote_addr, message="you have reached maximum limit, please try again after 10 seconds")

@app.route('/test', methods=['GET', 'POST'])
def test():
    return "Hello, world"

@app.route('/exportLog', methods=['POST'])
def export_log():
    if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
        app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
