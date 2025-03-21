# -*- coding: utf-8 -*-
from flask import *
import subprocess
import configparser
from datetime import datetime
import logging

app = Flask(__name__)

logging.basicConfig(filename='port1337.log', level=logging.INFO)
logger = logging.getLogger()

@app.route('/random/checklimit', methods=['GET'])
def apilimit():
    try:
        command = "/random/some/directory/bin/sbin/asterisk -rx 'core show channels verbose' | grep 'active call' | awk '{print $1}'"
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        config = configparser.ConfigParser()
        config.read("limit.properties")
        limit = config["limit"]["limitMax"]
        activeCallsIVR = int(output)
        current_datetime = datetime.now()
        logger.info("Time: %s, activecallsnow: %s, limit: %s", current_datetime, activeCallsIVR, str(limit))
        if activeCallsIVR >= int(limit):
            data = {"status": False}
            logging.info(data)
            json_string = json.dumps(data,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8", status = 200)
            return response
        else:
            data = {"status": True}
            logging.info(data)
            json_string = json.dumps(data,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8", status = 200)
            return response
    except Exception as e:
        error_message = f'Error: {str(e)}'
        current_datetime2 = datetime.now()
        logger.info("Time: %s", current_datetime2)
        logging.error(error_message)
        logger.info("\n")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 1337, debug=False)
