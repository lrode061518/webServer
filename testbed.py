import unittest
import httplib
import json
from includes.define import DEFAULT_ADDR, DEFAULT_PORT, RETCODE

TEST_SERVER_ADDR = DEFAULT_ADDR
TEST_SERVER_PORT = str(DEFAULT_PORT)
TEST_URL = '/v1/ubike-station/taipei?lat={}&lng={}'

INVALID_LATLNG_LIST = [
	( -29.100201 , 184.223383 ),    # invalid longitude
	( 223.012892 , 138.309586 ),	# invalid latitude
	( 192.203894 , -483.203243 ),   # both invalid
    ( 'asdf'     , 'dkosooso' ),    # not number
    ( ''         , ''         ),    # no / or can't get input
]

NON_TAIPEI_LOC_LIST = [
	( 24.995077 , 121.293173 ),
	( 27.981977 , 120.656750 ),
	( 22.610670 , 120.319297 ),
	( 15.167067 , 121.178506 ),
	( -33.831047 , 151.205130 )
]

TAIPEI_LOCATIONS_LIST = [
	( 25.034153 , 121.568509 ),
	( 25.168711 , 121.446996 ),
	( 25.061145 , 121.532444 )
]

class mainServerTest(unittest.TestCase):
	def request(self, lat, lng):
		try:
			conn = httplib.HTTPConnection( TEST_SERVER_ADDR, TEST_SERVER_PORT )
			conn.request('GET', TEST_URL.format( lat , lng ))
			response = conn.getresponse()
			return json.loads(response.read())
		except Exception, err:
			print err
		finally:
			conn.close()

	def test_invalid_latlng(self):
		for case in INVALID_LATLNG_LIST:
			jsonObj = self.request(case[0], case[1])
                        self.assertTrue( jsonObj )
			self.assertEqual( jsonObj['code'] , RETCODE.INVALID_LATLNG )
			self.assertFalse( jsonObj['result'] )

	def test_not_in_taipei(self):
		for case in NON_TAIPEI_LOC_LIST:
			jsonObj = self.request(case[0], case[1])
                        self.assertTrue( jsonObj )
			self.assertEqual( jsonObj['code'] , RETCODE.NOT_IN_CITY )
			self.assertFalse( jsonObj['result'] )

	def test_common(self):
		# todo : think another way to check 'all full' case,
		#         maybe create a dummy db
		for case in TAIPEI_LOCATIONS_LIST:
			jsonObj = self.request(case[0], case[1])
                        self.assertTrue( jsonObj )
			self.assertEqual( jsonObj['code'] , RETCODE.SUCCESS )
			self.assertTrue( jsonObj['result'] )
			for station in jsonObj['result']:
				self.assertTrue( station['num_ubike'] > 0 )




# make sure the server is already running before testing
if __name__ == '__main__':
	unittest.main()
