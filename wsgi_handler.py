"""
AWS Lambda handler for Flask application using serverless-wsgi
"""
try:
    import unzip_requirements
except ImportError:
    pass

import serverless_wsgi
from main import app

def handler(event, context):
    """Lambda handler function"""
    return serverless_wsgi.handle_request(app, event, context)
