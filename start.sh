#!/bin/sh
trap kill `jobs -p` EXIT

# init database
#mongod --dbpath `pwd`/data/db --fork --logpath `pwd`/data/mongod.log #&


if [ False ]; then
# workaround to register/unregister updateDB work 
crontab -l > origin.cr
cp origin.cr tmp.cr
echo "*/1 * * * * `pwd`/updateDB.sh -U" > tmp.cr
crontab tmp.cr
fi

# start server
python webserver.py

# stop routine work
crontab origin.cr


# terminate
