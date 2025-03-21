# -*- coding: utf-8 -*-
from flask import *
import hashlib
import os
import re
import logging
from datetime import datetime

app = Flask(__name__)

logging.basicConfig(filename='port9024.log', level=logging.INFO)
logger = logging.getLogger()

@app.route('/exists/', methods=['POST'])
def apibapi():
    try:
        if request.method == 'POST':
            flagImya, flagOtchestvo, flagFamiliya = False, False, False
            requestPrevious = request.json
            firstname = requestPrevious.get('firstname')
            secondname = requestPrevious.get('secondname')
            surname = requestPrevious.get('surname')
            current_datetime = datetime.now()
            logger.info("Time: %s, data: %s", current_datetime, requestPrevious)
            if firstname != None: 
                firstnametemp = re.sub(r'[^a-zа-яәғқңөұүһі\-]', '', re.sub(r'[\d\s]+', '', firstname.lower()))
                ans1 = hashlib.md5(firstnametemp.upper().encode('utf-8')).hexdigest()
                fileP1 = '/random/apps/random/var/lib/asterisk/sounds/FIO/' + ans1 + '.wav'
                if os.path.exists(fileP1):
                    flagImya = True
            if secondname != None:
                secondnametemp = re.sub(r'[^a-zа-яәғқңөұүһі\-]', '', re.sub(r'[\d\s]+', '', secondname.lower()))
                ans2 = hashlib.md5(secondnametemp.upper().encode('utf-8')).hexdigest()
                fileP2 = '/random/apps/random/var/lib/asterisk/sounds/FIO/' + ans2 + '.wav'
                if os.path.exists(fileP2):
                    flagOtchestvo = True
            if surname != None:
                surnametemp = re.sub(r'[^a-zа-яәғқңөұүһі\-]', '', re.sub(r'[\d\s]+', '', surname.lower()))
                ans3 = hashlib.md5(surnametemp.upper().encode('utf-8')).hexdigest()
                fileP3 = '/random/apps/random/var/lib/asterisk/sounds/FIO/' + ans3 + '.wav'
                if os.path.exists(fileP3):
                    flagFamiliya = True

            if (flagFamiliya and flagImya) or (flagFamiliya and flagOtchestvo and flagImya):
                data = {"exists": True}
                logger.info(data)
                json_string = json.dumps(data,ensure_ascii = False)
                response = Response(json_string,content_type="application/json; charset=utf-8", status = 200)
                return response
            else:
                data = {"exists": False}
                logger.info(data)
                json_string = json.dumps(data,ensure_ascii = False)
                response = Response(json_string,content_type="application/json; charset=utf-8", status = 400)
                return response
    except Exception as e:
        error_message = f'Error: {str(e)}'
        current_datetime2 = datetime.now()
        logger.info("Time: %s", current_datetime2)
        logging.error(error_message)
        logger.info("\n")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 9024, debug=False)
