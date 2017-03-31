import json
import httplib
from includes.define import *

class resultHandler:
    def __init__(self):
        self.code   = UB_SUCCESS
        self.result = []

class city:
    def __init__(self):
        self.city   = ''
        self.ret = resultHandler()

    def valid_city(self, lat, lng):
        # using google geocoding APIs
        if not self.city:
            print 'undefined city'
            return False

        valid = False

        try:
            conn = None
            conn = httplib.HTTPSConnection(GOOGLE_MAPS_API, httplib.HTTPS_PORT)
            conn.request('GET', '/maps/api/geocode/json?latlng=' + str(lat) + ',' + str(lng) )

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
            self.result.code = UB_SYSTEM_ERR
            valid = False
        finally:
            if conn:
                conn.close()

            return valid

