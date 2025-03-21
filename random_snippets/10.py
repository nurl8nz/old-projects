# -*- coding: utf-8 -*-
from flask import *
import hashlib
import os
import re
import logging
from datetime import datetime
import json 

app = Flask(__name__)

logging.basicConfig(filename='port2046.log', level=logging.INFO)
logger = logging.getLogger()

@app.route('/file/', methods=['POST'])
def apibapi():
    try:
        if request.method == 'POST':
            dialog_id = request.form.get('dialog_id')
            file_name = request.form.get('file_name')
            file = request.files.get('file')

            if not dialog_id or not file_name or not file:
                response = {"error": "Missing 'dialog_id', 'file_name' or 'file'"}
                json_string = json.dumps(response, ensure_ascii=False)
                current_datetime = datetime.now()
                logger.info("Time: %s", current_datetime)
                logger.info("smth is not sended")
                return Response(json_string, content_type="application/json; charset=utf-8", status=400)

            directory_path = os.path.join(os.getcwd(), dialog_id)
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            file_path = os.path.join(directory_path, file_name)
            if os.path.exists(file_path):
                base_name, extension = os.path.splitext(file_name)
                counter = 1
                while os.path.exists(file_path):
                    new_file_name = f"{base_name}_{counter}{extension}"
                    file_path = os.path.join(directory_path, new_file_name)
                    counter += 1
            file.save(file_path)

            current_datetime = datetime.now()
            logger.info("Time: %s", current_datetime)
            logger.info("%s, %s, %s", dialog_id, file_name, file)

            data = {"message": "File saved successfully"}
            json_string = json.dumps(data, ensure_ascii=False)
            response = Response(json_string, content_type="application/json; charset=utf-8", status=200)
            return response
    except Exception as e:
        error_message = f'Error: {str(e)}'
        current_datetime2 = datetime.now()
        logger.info("Time: %s", current_datetime2)
        logging.error(error_message)
        logger.info("\n")

        response = {"error": str(e)}
        json_string = json.dumps(response, ensure_ascii=False)
        return Response(json_string, content_type="application/json; charset=utf-8", status=500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2046, debug=False)
