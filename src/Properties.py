HEIGHT = 250
WIDTH = 250
PIXEL_SIZE = 100
url = 'https://services.terrascope.be/wms/v2'
urlPixels = 'https://services.terrascope.be/timeseries/v1.0/ts/TERRASCOPE_S2_NDVI_V2/geometry?'
defaultArguments = '?service=WMS&version=1.3.0&request=GetMap&layers=CGS_S2_NDVI&format=image/png&srs=EPSG:3857'
jsonOutputs = 'outputs/JsonOutputs.json'
croppedImageBlackBackground = 'resources/images/dst.png'
croppedImageBlackBackgroundName = 'dst'
croppedImageWhiteBackgroundName = 'dst2'
token = '36aef768-3076-43ad-8566-4818fd82c73c'
colors = ['green', 'yellow', 'brown']
imageLocation = 'resources/images/image.png'
date = '2021-05-15'
polygonCoordinates = [27.199243, 45.910026, 27.209468, 45.911885, 27.209607, 45.906525, 27.200563, 45.904793]
coordinatesBBOX = [3028959.60, 5766239.96, 3027805.88, 5765105.34]
polygonCoordinatesString = '27.199243,45.910026,27.209468,45.911885,27.209607,45.906525,27.200563,45.904793'