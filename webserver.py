#!/usr/bin/python
# coding:utf-8
import web
from includes.define import *
from city   import *
from database import *

class index:
    def GET(self):
        return 'Usage:  current.url.and/v1/ubike-station/taipei?lat=xxxxxxx&lng=xxxxxxxx'

class taipei(city):
    def __init__(self):
        city.__init__(self)
        self.city = 'Taipei'

    def GET(self):

        while True:
            val = web.input(lat = -999, lng = -999)

            # Err check -
            # check latitude & longitude
            if not valid_latlng(val.lat, val.lng):
                print 'invalid latlng'
                self.ret.code = UB_INVALID_LATLNG
                break
            # check in current city
            if not self.valid_city(val.lat, val.lng):
                print 'not in the correspond city'
                break

            # Start processing -
            reqlist = findnearest(float(val.lat), float(val.lng) )

            self.ret.result = reqlist

            break


        web.header('Content-Type', 'application/json; charset=utf-8', unique=True)

        return json.dumps(self.ret.__dict__)

if __name__ == "__main__":
    app = web.application(urls, globals())
    response = app.request('/v1/ubike-station/taipei?lat=25.034153&lng=121.568509')

    print response.data
    print response.status
    print response.headers['Content-Type']
    #app.run()
