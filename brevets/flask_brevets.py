"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow
import acp_times
import requests

import logging
import os
###
# Globals
###
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG) 

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"

def get_brevet():

    lists = requests.get(f"{API_URL}/brevets").json()

    new_list = lists[-1]

    return new_list["length"], new_list["start_time"], new_list["checkpoints"]

def insert_brevet(length, start_time, checkpoints):

    _id = requests.post(f"{API_URL}/brevets", json={"length": length, "start_time": start_time, "checkpoints": checkpoints}).json()  
 
    return _id

###
# Pages
###


@app.route("/")

@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

@app.route("/_insert", methods=["POST"])
def insert():
        
        input_json = request.json
        
        length = input_json["length"] 
        start_time = input_json["start_time"] 
        checkpoints = input_json["checkpoints"]

        todo_id = insert_brevet(length, start_time, checkpoints)

        return flask.jsonify(result={},
                        message="Inserted!", 
                        status=1,
                        mongo_id=todo_id)
    

        return flask.jsonify(result={},
                        message="Something went wrong!!", 
                        status=0, 
                        mongo_id='None')

@app.route("/_fetch")
def fetch():

    try:
        length, start_time, checkpoints = get_brevet()
        return flask.jsonify(
                result={"length": length, "start_time": start_time, "checkpoints": checkpoints}, 
                status=1,
                message="Successfully fetched!")
    except:
        return flask.jsonify(
                result={}, 
                status=0,
                message="Fetching was unsuccessful!")

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")

    km = request.args.get('km', 999, type=float)
    br_dis = request.args.get('br_dis', 999, type=float)
    start_time = request.args.get('start_time', type=str)
    start_time = arrow.get(start_time, 'YYYY-MM-DDTHH:mm')

    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    open_time = acp_times.open_time(km, br_dis, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, br_dis, start_time).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = os.environ["DEBUG"]
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
   # print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=os.environ["PORT"], host="0.0.0.0")
