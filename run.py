from flask import Flask
from intent_entity_detection.views import intent_entity
import logging
import sys



from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(asctime)s:%(levelname)s:%(module)s:%(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': sys.stdout,
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.register_blueprint(intent_entity, url_prefix='/intent-entity-api')