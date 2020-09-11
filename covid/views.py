from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import time
from bs4 import BeautifulSoup as BS


def index(request):
    # creating url using country name

    country_name = request.POST.get("query")

    url = f"https://www.worldometers.info/coronavirus/country/{country_name}/"
    if country_name is None:
        url = "https://www.worldometers.info/coronavirus/"
        country_name = "World"
    else:
        country_name

    # getting the request from url
    data = requests.get(url)

    # converting the text
    soup = BS(data.text, 'html.parser')

    # finding meta info for cases
    cases = soup.find_all("div", class_="maincounter-number")

    if len(cases) == 0 or len(cases) == None:
        return render(request, "err.html")
    # getting total cases number
    total = cases[0].text
    total = total[1: len(total) - 2]

    # getting recovered cases number
    recovered = cases[2].text
    recovered = recovered[1: len(recovered) - 1]

    # getting death cases number
    deaths = cases[1].text
    deaths = deaths[1: len(deaths) - 1]

    context = {'ct_name': country_name, 'total': total,
               'recovered': recovered, 'deaths': deaths}
    return render(request, "home.html", context)
