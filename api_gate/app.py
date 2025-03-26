from flask import Flask, request, jsonify
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import requests

app = Flask(__name__)

# Configuration for microservices
SERVICES = {
    'fertilizer': 'http://localhost:8000',
    'irrigation': 'http://localhost:5006',
    'leaf': 'http://localhost:5005',
    'species': 'http://localhost:5001'
}

@app.route('/<service>/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy_request(service, subpath):
    """
    Proxy requests to the appropriate microservice
    """
    if service not in SERVICES:
        return jsonify({'error': 'Service not found'}), 404
    
    # Construct the full URL for the target service
    target_url = f"{SERVICES[service]}/{subpath}"
    
    try:
        # Forward the request
        response = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        
        # Return the response from the target service
        return (
            response.content, 
            response.status_code, 
            response.headers.items()
        )
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def health_check():
    """
    Simple health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'services': list(SERVICES.keys())
    })

if __name__ == '__main__':
    # Run the API Gateway on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)