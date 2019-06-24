import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import datetime
import traceback
from json_log_formatter import JSONFormatter
from flask import Flask, request, Response

environment = os.getenv('ENVIRONMENT')
app = Flask(__name__)


def divide_numbers(a,b):
    try:
        a/b
    except Exception as e:
        print('not divisable')
        logger.exception('ex')

    return  a/b


@app.before_request
def log_entry():
    context = {
        'datetime': str(datetime.datetime.now()),
        'environment': environment,
        'type': 'before request',
        'method': request.method,
        'path': request.path,
        'ip': request.environ.get("REMOTE_ADDR"),
        'url': request.url
    }
    app_log.info(json.dumps(context))


@app.after_request
def log_the_status_code(response):
    context = {
    'datetime': str(datetime.datetime.now()),
    'environment': environment,
    'type': 'after request',
    'method': request.method,
    'path': request.path,
    'ip': request.environ.get("REMOTE_ADDR"),
    'url': request.url,
    'status': response.status_code
    }
    app_log.info(json.dumps(context))
    return response



@app.route('/health')
def health_check():
    return 'OK'





if __name__=='__main__':

    log_format={'level': '%(levelname)s',
        'loggerName': '%(name)s',
        'message': '%(message)s',
        'time': '%(asctime)s',
        'environment': environment,
        'exc_info': str('%(exc_info)s')
    }
    log_format = json.dumps(log_format)

    logger = logging.getLogger(__name__)
    c_handler = TimedRotatingFileHandler('test.log', when='m', interval=1, backupCount=2, encoding=None, delay=False, utc=False)
    c_handler.setLevel(logging.WARNING)
    c_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(c_handler)



    app_log = app.logger
    app_handler = TimedRotatingFileHandler('test_app.log', when='m', interval=1, backupCount=2, encoding=None, delay=False, utc=False)
    app_log.addHandler(app_handler)
    app_log.setLevel(logging.INFO)

    logger.error('This is an error')

    try:
        divide_numbers(5,0)
    except Exception as e:
        logger.error('some text')


    app.run(port=12345, debug=True)
