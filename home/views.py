from django.shortcuts import render
from django.http import HttpResponse
from home.scripts import log_and_require
# Create your views here.

@log_and_require(methods=("GET", ""), login=True,)
def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')
