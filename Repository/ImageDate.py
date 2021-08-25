from datetime import datetime, timedelta
import requests
from Properties.Properties import *
import json
from Repository.Conversions import *


def postPixelCountService(polygonCoordinatesString, numberOfDays=30):
    today = datetime.now()
    urlPost = urlPixels + f'&startDate={((today - timedelta(days=numberOfDays)).strftime("%Y-%m-%d"))}' + f'&endDate={today.strftime("%Y-%m-%d")}'
    polygonCoordinatesStringList = list(polygonCoordinatesString.strip().split(","))
    polygonCoordinatesStringPairList = arrayToArrayOfPairs(polygonCoordinatesStringList)
    polygonCoordinatesStringPairList.append(polygonCoordinatesStringPairList[0])
    bodyJson = {"type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [polygonCoordinatesStringPairList]
                }}
    bodyJson = json.dumps(bodyJson)
    response = requests.post(urlPost, data=bodyJson)
    responseJson = response.json()
    return responseJson


def getOptimalDate(polygonCoordinatesString):
    ok = 0
    days = 30
    max = 0
    maxDate = 0
    polygonCoordinatesString = polygonCoordinatesString.replace(" ","")
    print(polygonCoordinatesString)
    while ok == 0:
        responseJson = postPixelCountService(polygonCoordinatesString, days)
        maxDate = responseJson['results'][0]['date']
        if responseJson['results'][0]['result']['average'] != 'NaN':
            max = float(responseJson['results'][0]['result']['average'])
        else:
            max = 0
        for i in range(len(responseJson['results'])):
            if responseJson['results'][i]['result']['average'] != 'NaN' and float(responseJson['results'][i]['result']['average']) > max:
                max = float(responseJson['results'][i]['result']['average'])
                maxDate =responseJson['results'][i]['date']
        if max > 0.5:
            ok = 1
        days += 30
    outputStringList = []
    outputStringList.append(maxDate)
    outputStringList.append(max)
    return outputStringList

print(getOptimalDate(polygonCoordinatesString))





