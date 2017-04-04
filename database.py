import sys, os
import gzip
import urllib
import json
from pymongo import MongoClient
from includes.define import API ,DOC_KEY, UB, \
                            DB_NAME, COLLECTION_NAME, \
                            TEMP_GZ_FILE

def getBikeData():
    urllib.urlretrieve(API.DATA_TAIPEI_UBIKE, TEMP_GZ_FILE)
    f = gzip.open(TEMP_GZ_FILE, 'r')
    data = f.read()
    f.close()
    os.remove(TEMP_GZ_FILE)
    return data

def updateDB():
    try:
        # get new data
        data = getBikeData()
        dicBike = json.loads(data)

        # update db
        if dicBike[ UB.RETURN_CODE ] != UB.RET_OK :
            raise Exception('return status error with code {}'.format(dicBike['retCode']))

        resultObj = dicBike[ UB.RETURN_VALUE ]

        for attr, value in resultObj.iteritems():

            doc = {
                    DOC_KEY.NAME    : value[ UB.STATION_NAME ].encode('utf-8'),
                    DOC_KEY.LOC     : {
                                        'type' : 'Point',
                                        'coordinates' : [ float(value['lng']), float(value['lat']) ]
                                        },
                    DOC_KEY.TOT     : int( value[ UB.TOTAL_BIKES ] ),
                    DOC_KEY.CUR     : int( value[ UB.CURRENT_BIKES ] ),
                    DOC_KEY.ENA     : True if value[ UB.STATION_STATUS ] == UB.STAT_OK  else False
                    }

            if collection.count({ DOC_KEY.NAME : doc[DOC_KEY.NAME] }) :
                collection.find_one_and_update( 
                                                { DOC_KEY.NAME : doc[DOC_KEY.NAME] } , 
                                                { '$set' : doc } 
                                                )
            else:
                collection.insert_one(doc)


    except Exception, err:
        print 'Get Bike exception'
        print err

def allStationsFull():
    return True if collection.find( 
        {   '$where' : 'this.{} === this.{}'.format(DOC_KEY.TOT, DOC_KEY.CUR) }
        ).count() > 0 else False

def findnearest(lat, lng, count):
    reqlist = []
    print 'start finding nearest {} station(s)'.format(count)
    for doc in collection.find( {
        DOC_KEY.LOC : {
            '$near' :  {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': [lng, lat]
                    }
                }
            }
        } ):

        #print u'find station {}'.format( doc[ DOC_KEY.NAME ] )

        if not doc[ DOC_KEY.ENA ]:
            print ' but not able to used ...'
            continue

        if doc[ DOC_KEY.CUR ] <= 0:
            print ' but current no bikes ...'
            continue

        reqlist.append( { 
            'station' : doc[ DOC_KEY.NAME ],
            'num_ubike' : doc[ DOC_KEY.TOT ] - doc[ DOC_KEY.CUR ]
            } )

        count -= 1

        if not count:
            break

    return reqlist


# create db client
if 'MONGODB_URI' in os.environ:
    MONGODB_URI = os.environ['MONGODB_URI']
    client = MongoClient(MONGODB_URI)
else:
    client = MongoClient()

db = client[ DB_NAME ]
collection = db[ COLLECTION_NAME ]
collection.create_index( [( 'loc' , '2dsphere' )] )


# handle input option
opt = ''
argc = len( sys.argv )
if argc == 2:
    if sys.argv[1].startswith('-'):
        opt = sys.argv[1][1:]
elif argc > 2:
    print 'Wrong option input ....'

if opt.upper() == 'U':
    updateDB()
