'''
return code
1  : all ubike stations are full <--- empty or full ?? what about all stations are empty?
0  : OK
-1 : invalid latitude or longitude
-2 : given location not in Taipei City
-3 : system error
'''

class RETCODE:
	SUCCESS  = 0
	ALL_FULL = 1
	INVALID_LATLNG = -1
	NOT_IN_CITY    = -2
	SYSTEM_ERR     = -3

class API:
	GOOGLE_MAPS      	  = 'maps.googleapis.com'
	GOOGLE_GEOMAP_LAT_LNG = '/maps/api/geocode/json?latlng={},{}'
	DATA_TAIPEI_UBIKE     = 'http://data.taipei/youbike'

class DOC_KEY:
	NAME = 'name'
	LOC  = 'loc'
	TOT  = 'total'
	CUR  = 'curr'
	ENA  = 'enabled'

class UB:
	RET_OK		   = 1     # APIs return code
	STAT_OK		   = '1'
	RETURN_CODE    = 'retCode'
	RETURN_VALUE   = 'retVal'
	STATION_NAME   = 'sna'
	TOTAL_BIKES    = 'tot'
	CURRENT_BIKES  = 'sbi'
	STATION_STATUS = 'act'

# MISC
urls = (
    '/', 'index' ,
    '/v1/ubike-station/taipei', 'taipei'
)

import os
if 'MONGODB_URI' in os.environ:
	DB_NAME = 'heroku_35nzq90c'
else:
	DB_NAME = 'bike_db'
COLLECTION_NAME = 'bike_collection'
TEMP_GZ_FILE = 'tmp.gz'
DEFAULT_ADDR = '127.0.0.1'
DEFAULT_PORT = 8090

# As we are current using GooleMaps ... 
# we follow GoogleMaps' latlngBound as below: 
#  Latitude: -85 to +85
#  Longitude: -180 to +180
def invalid_latlng(lat, lng):
	if -85.0 > lat or lat  > 85.0:
		return True
	if -180.0 > lng or lng > 180.0:
		return True

	return False