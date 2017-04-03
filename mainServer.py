import web 
from city import city
from includes.define import urls, DEFAULT_ADDR, DEFAULT_PORT

class mainServer( web.application ):
    def run(self, port=DEFAULT_PORT, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (DEFAULT_ADDR, DEFAULT_PORT) )

class index:
    def GET(self):
        return (
        	'Find 2 nearest ubike stations\n'
        	'Usage:  .../v1/ubike-station/taipei?lat=latitude&lng=longitude\n'
        	'with correspond "latitude" and "longitude"'
        )

class taipei(city):
    def __init__(self):
        city.__init__(self)
        self.city = 'Taipei'

if __name__ == "__main__":
    app = mainServer(urls,  globals())
    app.run()