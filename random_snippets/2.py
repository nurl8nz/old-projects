from flask import *
from datetime import datetime
import csv
from requests.auth import HTTPBasicAuth
import requests
import xml.etree.ElementTree as ET
from urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import html.parser
import logging

app = Flask(__name__)

def creatio(iin, number, groupID, lang):
    url = "http://0.0.0.0/bip-sync/"
    url2 = 'http://0.0.0.0:8081/send'
    headers = {'content-type': 'text/xml'}
    body = f"""<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <SOAP-ENV:Header/>
    <SOAP-ENV:Body>
    <sync:SendMessage xmlns:sync="http://0.0.0.0/SyncChannel/v10/Types">
    <request>
    <requestInfo>
    <messageId>123456789</messageId>
    <serviceId>SomeService</serviceId>
    <messageDate>2023-02-13T11:17:26.000+06:00</messageDate>
    <routeId/>
    <sender>
    <senderId>username</senderId>
    <password>12345678</password>
    </sender>
    </requestInfo>
    <requestData>
    <data>
    <GetRdbRequest>
    <requestId>2</requestId>
    <iin>%s</iin>
    <groupId>%s</groupId>
    </GetRdbRequest>
    </data>
    </requestData>
    </request>
    </sync:SendMessage>
    </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>
    """ % (iin, groupID)
    
    # first sending
    print(body)
    try:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        response = requests.post(url,data=body,headers=headers, verify=False)
    except Exception:
        return 'BAD1'

    # making kazyavkas more pretty
    parser = html.parser.HTMLParser()
    bla = parser.unescape(response.text)
    
    #c = bla.index('</requestId>')
    #bla = bla[:c-1] + groupID + bla[c:]

    # finding index where we can add our lang
    x = bla.index('</RdbResponse>')
    bla = bla[:x-1] +'<groupId>'+groupID+'</groupId>'+'<lang>' + lang + '</lang>' + bla[x:]

    # second sending
    print(bla)
    try:
        resp = requests.post(url2, data=bla.encode('utf-8'), headers=headers, verify=False)
    except Exception:
        return 'BAD2'
    
    # getting link
    linkX = resp.json().get('link')
    text = None
    if(lang == "1"):
        text = f"Уважаемый клиент, ваш документ готов. {linkX}"
    else:
        text = f"Құрметті клиент, сіздің құжатыңыз дайын.  {linkX}"
    # reading token for sending sms
    with open('../python_code/token_file.txt') as f:
        accessToken = f.readlines()
    dataForSMS = {
          "phone": number,
          "smsText": text
    }

    # third sending
    try:
        headers2 = {"Authorization": "Bearer " + accessToken[0]}
        smsPROD = 'https://0.0.0.0:2046/api/smsgateway/send'
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        res = requests.post(smsPROD, json = dataForSMS, headers = headers2, verify=False)
    except Exception:
        return 'BAD3'
    return 'OK'

@app.route('/m3/<string:iin>/<string:number>/<string:groupID>/<string:lang>', methods=['GET'])
def cringe(iin, number, groupID, lang):
    csvTime = datetime.now()
    logging.basicConfig(filename="test.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M%S',
                        level=logging.DEBUG)
    responseX = creatio(iin, number, groupID, lang)
    csvTime2 = datetime.now()
    durationX = (csvTime2 - csvTime).total_seconds()
    x = 'status: ' + responseX + ', ' + iin + ', ' + number + ', ' + groupID + ', ' + lang + ', ' + str(durationX) + ', ' + str(csvTime) + ', ' + str(csvTime2)
    logging.info(x)
    if 'BAD' in responseX:
        return 'BAD'
    elif responseX == 'OK':
        return 'OK' 

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 2706, debug=True)
