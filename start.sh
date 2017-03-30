#!/bin/sh
trap kill `jobs -p` EXIT

# init database
mongod --dbpath `pwd`/data/db &

# workaround to register/unregister updateDB work 
crontab -l > origin.cr
cp origin.cr tmp.cr
echo "*/1 * * * * `pwd`/updateDB.sh" > tmp.cr
crontab tmp.cr

# start server
python webservice.py

# stop routine work
crontab origin.cr


# terminate
