import pytest
import requests
from app.calulateApp import calculateEmission, calculateCost, calculateEnergy

def test_Emissions():
    postcode = "LS6 2QF"
    shortcode = "LS6"
    energy = 1000

    url = f"https://api.carbonintensity.org.uk/regional/postcode/{shortcode}"
    response = requests.get(url)
    data = response.json()
    intensity = data['data'][0]['data'][0]['intensity']['forecast']
    emission = intensity*energy

    assert calculateEmission(energy, postcode) == emission

def test_Cost():
    rate = 0.1
    energy = 1000
    assert calculateCost(rate, energy) == 100

def test_Energy():
    power = 10 
    time = 40

    assert calculateEnergy(power, time) == power*time*0.001