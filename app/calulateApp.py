# This file contains the function required for calcualting energy, cost and co2 emission.
# be careful with the units but its good to handle everything in base units.

# 

import requests

### Main Functions ###

# Takes in a list of appliances and returns a list[energy (J), cost(pounds), emissions(em)]
def calculateSum(applianceList):
    
    result = [0.0, 0.0, 0.0]

    # assumes that everything is already calculated. 
    for appliance in applianceList:
        result[0] += appliance.energyUsed or 0.0
        result[1] += appliance.cost or 0.0
        result[2] += appliance.emissions or 0.0
    return result



# returns a list of related info (energy, cost, emission)
def calculateAll(power, time, rate, postCode):
    result = [0.0,0.0,0.0]
    result[0] = calculateEnergy(power, time)
    result[1] = calculateCost(rate, result[0])
    result[2] = calculateEmission(result[0], postCode)    
    return result


# Given power (W) and time(Hr) we return energy(kWH)
def calculateEnergy(power, time):
    return convertJoules(power*time*3600)

#given rate (Pounds per KWH) and energy(kWH) we return cost(Pounds)
def calculateCost(rate, energy):
    print(rate)
    return rate * energy

# given energy(kWH) and Co2 Intensity (em/kWH) from postcode, we return co2 emissions
def calculateEmission(energy, fullPostCode):
    # this must be an outwards postcode. i.e. its short form
    # all post codes are split into two parts with a space in the middle
    postcode = convertPostcode(fullPostCode)
    url = f"https://api.carbonintensity.org.uk/regional/postcode/{postcode}"
    response = requests.get(url)

    # Post code is in short form.
    if response.status_code == 200:
        data = response.json() 
        intensity = data['data'][0]['data'][0]['intensity']['forecast']

        return energy*intensity
    
    # If for some reason postcode is not in short form or incorrect
    # we use the national intensity
    else:
        url = f"https://api.carbonintensity.org.uk/intensity"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            nationalIntensity = data['data'][0]['intensity']['forecast']
            return energy*nationalIntensity


### Utility Functions ###

# converts energy in Joules to KWH
def convertJoules(joules):
    return joules/(3600000)

# converts full postcode to outer
def convertPostcode(fullPostCode):
    x = fullPostCode.split(" ")
    return x[0]