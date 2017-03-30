import gzip
import urllib
from pymongo import MongoClient

def updateDB():
    try:
        urllib.urlretrieve(DATA_TAIPEI_UBIKE, TEMP_GZ_FILE)
        f = gzip.open(TEMP_GZ_FILE, 'r')
        data = f.read()
        f.close()
        print data
        dicBike = json.loads(data)






    except Exception, err:
        print 'get Bike exception'
        print err
    finally:
        pass


uri = 'mongodb://USERNAME:password@host?authSource=source'
client = MongoClient(uri)
