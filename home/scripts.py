import os
import time
import logging
from functools import wraps
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

LOG_FILES_DIR = 'C:\\Users\\Dell\\Desktop\\Net_Result\\django-material-dashboard\\logs\\'

def get_client_info(request):
    # Define the potential keys and their descriptions
    ip_keys = {
        "HTTP_X_FORWARDED_FOR": "X-Forwarded-For",
        "HTTP_CLIENT_IP": "Client-IP",
        "REMOTE_ADDR": "Remote Address",
    }

    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    
    for key, description in ip_keys.items():
        if key in request.META:
            ip_address = request.META[key]
            # Extract the first IP address from a comma-separated list if necessary
            if "," in ip_address:
                ip_address = ip_address.split(",")[0].strip()
            return ip_address, description, user_agent

    # Return default values if no IP address is found
    return "Unknown", "Unknown", user_agent

def log_and_require(methods=("GET", "POST"), login=True, function_name=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            start_time = time.time()  # Measure the start time
            ip_address, key_description, user_agent = get_client_info(request)
            timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file = LOG_FILES_DIR + f"{view_func.__name__}.log"
            if not os.path.exists(LOG_FILES_DIR):
                os.makedirs(LOG_FILES_DIR)
            
            if methods is not None:
                wrapped = require_http_methods(methods)(view_func)
            else:
                wrapped = view_func
            
            if login:
                wrapped = login_required(login_url="/accounts/login/")(wrapped)

            # Check if the log file exists, and if not, create it
            if not os.path.isfile(log_file):
                open(log_file, 'w').close()

            response = wrapped(request, *args, **kwargs)

            end_time = time.time()  # Measure the end time
            elapsed_time = end_time - start_time  # Calculate the elapsed time
            
            # Log the request and embed the response time in the log message
            log_message = (f"{view_func.__name__} function called - Response Time: {elapsed_time:.2f} seconds")

            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - Visitor IP: %(ip)s (Key: %(key)s) - User Agent: %(user_agent)s - %(message)s Referrer - %(url)s - User - %(current_user)s",
            )
            logging.info(
                log_message,
                extra={
                    "ip": ip_address,
                    "key": key_description,
                    "timestamp": timestamp,
                    "url": request.META.get("HTTP_REFERER"),
                    "user_agent": user_agent,
                    "current_user": request.user,
                },
            )
            # Add the elapsed time to the response headers
            try:
                response['X-Render-Time'] = str(elapsed_time)
            except Exception as e:
                pass  # Do nothing if setting the header fails
            return response
        return _wrapped_view
    return decorator
