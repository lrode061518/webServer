'''
return code
1  : all ubike stations are full <--- empty or full ??
0  : OK
-1 : invalid latitude or longitude
-2 : given location not in Taipei City
-3 : system error
'''

UB_SUCCESS  = 0
UB_ALL_FULL = 1
UB_INVALID_LATLNG = -1
UB_NOT_IN_CITY    = -2
UB_SYSTEM_ERR     = -3

GOOGLE_MAPS_API = 'maps.googleapis.com'
#DATA_TAIPEI_API = 'data.taipei'
#DATA_TAIPEI_BIKE_ID = '8ef1626a-892a-4218-8344-f7ac46e1aa48'
DATA_TAIPEI_UBIKE = 'http://data.taipei/youbike'
TEMP_GZ_FILE = 'tmp.gz'

urls = (
    '/', 'index' ,
    '/v1/ubike-station/taipei', 'taipei'
)

def valid_latlng(lat, lng):
    if -90 > lat > 90:      return False
    if -180 > lat > 180:    return False
    return True

