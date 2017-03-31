import sys
import gzip
import urllib
import json
from pymongo import MongoClient
from includes.define import *

NAME = u'name'
LOC  = u'loc'
TOT  = u'total'
CUR  = u'curr'
ENA  = u'enabled'

def updateDB():
    try:
        # get new data
        urllib.urlretrieve(DATA_TAIPEI_UBIKE, TEMP_GZ_FILE)
        f = gzip.open(TEMP_GZ_FILE, 'r')
        data = f.read()
        f.close()
        #print data
        dicBike = json.loads(data)

        # update db
        if dicBike['retCode'] != 1 :
            raise Exception('return status error with code {}'.format(dicBike['retCode']))

        resultObj = dicBike['retVal']

        for attr, value in resultObj.iteritems():
            print 'start adding'
            print type( value['sna'] )
            print value['sna']
            doc = {
                    NAME    : value['sna'].encode('utf-8'),
                    LOC     : {
                                    u'type' : u'Point',
                                    u'coordinates' : [ float(value['lng']), float(value['lat']) ]
                                    },
                    TOT     : int( value['tot'] ),
                    CUR     : int( value['sbi'] ),
                    ENA     : True if value['act'] == '1'  else False
                    }
            print doc

            print 'with station :  '+(value[u'sna'])
            if collection.count({ NAME : doc[NAME] }) :
                print 'find_one_and_update'
                collection.find_one_and_update( { NAME : doc[NAME] } , { u'$set' : doc } )
            else:
                print 'insert_one'
                collection.insert_one(doc)


    except Exception, err:
        print 'Get Bike exception'
        print err
    finally:
        pass

def findnearest(lat, lng, count = 2):
    reqlist = []
    print 'start finding nearest {} stations'.format(count)
    for l in collection.find( {
        LOC : {
            '$near' :  {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': [lng, lat]
                    }
                }
            }
        } ):

        print u'find station {}'.format( l[NAME] )

        if not l[ENA]:
            print ' but not able to used ...'
            continue

        if l[CUR] <= 0:
            print ' but current no bikes ...'
            continue

        reqlist.append( { 'station' : l[NAME], 'num_ubike' : l[TOT] - l[CUR] } )
        count -= 1

        if not count:
            break

    print 'find {} stations'.format(len(reqlist))
    return reqlist


# create db client
client = MongoClient()
db = client.bike_db
collection = db.bike_collection
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
