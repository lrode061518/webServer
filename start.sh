#!/bin/sh
trap 'kill (jobs -p)' EXIT SIGINT SIGTERM

TEMP_CRONTAB='tmp.cr'
ORIGIN_CRONTAB='origin.cr'
MONGODB_PATH=`pwd`/data/db
MONGODB_LOG=`pwd`/data/mongod.log

# init database
mongod --dbpath $MONGODB_PATH --fork --logpath $MONGODB_LOG #&


if [ True ]; then
# workaround to register/unregister updateDB work 
crontab -l > $ORIGIN_CRONTAB
cp $ORIGIN_CRONTAB $TEMP_CRONTAB
echo "*/1 * * * * `pwd`/updateDB.sh -U" > $TEMP_CRONTAB
crontab $TEMP_CRONTAB
fi

# start server
python webserver.py

# stop routine work
crontab origin.cr
rm $TEMP_CRONTAB $ORIGIN_CRONTAB

# terminate