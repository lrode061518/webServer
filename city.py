import json
import httplib
import web
from includes.define import RETCODE, API, invalid_latlng
from database import allStationsFull, findnearest

class resultHandler:
    def __init__(self):
        self.code   = RETCODE.SUCCESS
        self.result = []

class city:
    def __init__(self):
        self.ret         = resultHandler()
        self.city        = ''
        self.searchLimit = 2

    def GET(self):

        web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
        while True:
            val = web.input(lat = '', lng = '')

            # Err check -
            # check latitude & longitude
            if invalid_latlng( float(val.lat), float(val.lng)):
                print 'invalid latlng'
                self.ret.code = RETCODE.INVALID_LATLNG
                break
            # check in current city
            if not self.in_the_city(val.lat, val.lng):
                print 'not in the correspond city'
                self.ret.code = RETCODE.NOT_IN_CITY
                break
            # check all station status
            if allStationsFull():
                print 'All stations are full now'
                self.ret.code = RETCODE.ALL_FULL
                break

            # Start processing -
            reqlist = findnearest(float(val.lat), float(val.lng), self.searchLimit )

            self.ret.result = reqlist
            
            if not reqlist:
                print 'No station available...'
                #self.ret.code = RETCODE.ALL_EMPTY ??

            break

        return json.dumps(self.ret.__dict__, ensure_ascii=False)

    def in_the_city(self, lat, lng):
        # using google geocoding APIs
        if not self.city:
            print 'undefined city'
            return False

        valid = False

        try:
            conn = None
            conn = httplib.HTTPSConnection( API.GOOGLE_MAPS, httplib.HTTPS_PORT )
            conn.request('GET', API.GOOGLE_GEOMAP_LAT_LNG.format( lat , lng ))

            response = conn.getresponse()
            if response.status != httplib.OK:
                raise httplib.HTTPException('get response failed')

            res = response.read()
            dicResponse = json.loads(res)

            # start process googleapies response

            if dicResponse['status'] != 'OK':
                raise httplib.HTTPException('response status not OK')

            for addr_cmpnts in dicResponse['results']:
                if any( self.city in subitem['long_name'] for subitem in addr_cmpnts['address_components'] ):
                    valid = True

        except Exception, err:
            print 'Exception occur'
            print err
            self.result.code = RETCODE.SYSTEM_ERR
            valid = False
        finally:
            if conn:
                conn.close()

            return valid

