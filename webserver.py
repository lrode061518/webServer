import web
from includes.define import *
from city   import *

def find2nearest(lat, lng):
    pass

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
                self.result.code = UB_INVALID_LATLNG
                break
            # check in current city
            if not self.valid_city(val.lat, val.lng):
                print 'not in the correspond city'
                break

            # Start processing -
            find2nearest(val.lat, val.lng)


            break

        return self.result.__dict__

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
