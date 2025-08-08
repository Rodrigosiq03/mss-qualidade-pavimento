import functions_framework
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.after_request
def log_response(response):
    status_color = "\033[32m" if response.status_code < 400 else "\033[31m"
    reset = "\033[0m"
    print(f"Request: {request.method} {request.url} - Status: {status_color}{response.status}{reset} \nHeaders: \n{response.headers} \nRequest Body: {request.get_data(as_text=False)}")
    return response

@functions_framework.http
def function_handler(request):
  with app.request_context(request.environ):
    return app.full_dispatch_request()

from src.routes.get_qualidade_pavimento import app as get_qualidade_pavimento_bp

app.register_blueprint(get_qualidade_pavimento_bp)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)