import os
import time
import logging
import threading
import multiprocessing
from functools import wraps
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from memory_profiler import profile

LOG_FILES_DIR = 'C:\\Users\\Dell\\Desktop\\Net_Result\\django-material-dashboard\\logs\\'

def get_client_info(request):
    ip_keys = {
        "HTTP_X_FORWARDED_FOR": "X-Forwarded-For",
        "HTTP_CLIENT_IP": "Client-IP",
        "REMOTE_ADDR": "Remote Address",
    }

    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

    for key, description in ip_keys.items():
        if key in request.META:
            ip_address = request.META[key]
            if "," in ip_address:
                ip_address = ip_address.split(",")[0].strip()
            return ip_address, description, user_agent

    return "Unknown", "Unknown", user_agent

def log_and_require(methods=("GET", "POST"), login=True, function_name=None):
    def decorator(view_func):
        @wraps(view_func)
        # @profile
        def _wrapped_view(request, *args, **kwargs):
            start_time = time.time()
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

            if not os.path.isfile(log_file):
                open(log_file, 'w').close()

            response = wrapped(request, *args, **kwargs)

            end_time = time.time()
            elapsed_time = end_time - start_time

            process_id = os.getpid()
            thread_id = threading.get_ident() if threading.current_thread() else "Main"

            log_message = (
                f"{view_func.__name__} function called - Response Time: {elapsed_time:.2f} seconds - Process ID: {process_id} - Thread ID: {thread_id} - Response Size: {len(response.content)} bytes"
            )

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

            try:
                response['X-Render-Time'] = str(elapsed_time)
            except Exception as e:
                pass
            return response
        return _wrapped_view
    return decorator
