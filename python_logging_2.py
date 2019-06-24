import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import datetime
import traceback
import json_log_formatter
import ujson
from flask import Flask, request, Response

environment = os.getenv('ENVIRONMENT')
app = Flask(__name__)


class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    json_lib = ujson

    def mutate_json_record(self, json_record):
        return json_record

    def json_record(self, message, extra, record):
        extra['message'] = message
        extra['environment'] = environment
        extra['level'] = record.levelname
        extra['loggerName'] = record.name

        if 'time' not in extra:
            extra['time'] = str(datetime.datetime.now())

        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        return extra

@app.route('/div')
def divide_numbers(a=5,b=0):
    try:
        a/b
    except Exception as e:
        print('not divisable')
        logger.error('ex', exc_info=True)

    return  a/b


@app.route('/health')
def health_check():
    return 'OK'


def create_json_logging_with_traceback():
    json_handler = TimedRotatingFileHandler('my-log.json', when='m', interval=1, backupCount=2, encoding=None, delay=False, utc=False)
    json_handler.setFormatter(CustomisedJSONFormatter())

    logger = logging.getLogger('my_json')
    logger.addHandler(json_handler)
    logger.setLevel(logging.INFO)
    return logger


if __name__=='__main__':
    logger = create_json_logging_with_traceback()


    app.run(port=12345, debug=True)
