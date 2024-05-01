from django.shortcuts import render
from django.http import HttpResponse
from home.scripts import log_and_require
from home.models import *
# Create your views here.

@log_and_require(methods=("GET", ""), login=True,)
def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')

@log_and_require(methods=("GET"), login=True,)
def company_detail(request, ticker):
    companyticker = CompanyTicker.objects.get(ticker=ticker)
    company = companyticker.company
    companyfoundingyear = CompanyFoundingYear.objects.filter(company=company)[0]
    companylistingyear = CompanyListingYear.objects.filter(company=company)[0]
    companydescription = CompanyDescription.objects.get(company=company)
    companyhq = CompanyHeadquarters.objects.get(company=company)
    companysector = CompanySector.objects.get(company=company)
    companyfinancialyearend = CompanyFinancialYearEnd.objects.get(company=company)
    # companysubsidiaries = Su

    context = {
        "companyticker":companyticker,
        "company":company,
        "companyfoundingyear":companyfoundingyear,
        "companylistingyear":companylistingyear,
        "companydescription":companydescription,
        "companyhq":companyhq,
        "companysector":companysector,
        "companyfinancialyearend":companyfinancialyearend,
    }

    return render(request, 'home/company_detail.html', context)