import os

try:
    TARGET_ENV = os.environ['TEXTRECRUIT_TARGET_ENV']
    CONFIG_URL = os.environ['TEXTRECRUIT_CONFIG_URL']
    CONFIG_AUTH_PASSWORD = os.environ['TEXTRECRUIT_CONFIG_AUTH_PASSWORD']
    CLOUD_PLATFORM = os.environ.get('TEXTRECRUIT_CLOUD_PLATFORM')
    MONGO_CERT_PASS = os.environ['TEXTRECRUIT_MONGO_CERT_PASS']
    #KEY = os.environ['TEXTRECRUIT_DECRYPT_KEY']
    IAM_ISSUER = os.environ['IAM_ISSUER']
except:
    TARGET_ENV = 'sandbox'
    IAM_ISSUER = 'https://login-dev.icimsmco.net/'
    TOKEN_KEY = 'mysecretkey'
    CLOUD_PLATFORM = 'local'

