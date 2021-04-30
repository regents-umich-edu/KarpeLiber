#!/bin/sh --

dbPath='karpeliber-dev'
dbName='karpeliber'
tables='item item_note item_page note_type page_mapping topic topic_note volume'
timestamp=$(date +'%Y%m%d%H%M%S')
dumpFile="karpeliber_dump_${timestamp}.sql"

echo "Database: ${dbName}"
echo
echo 'Dumping to file "'${dumpFile}'"...'

# uses ~/.mylogin.cnf to find the connect/login info for $dbPath
# (use mysql_config_editor to manage ~/.mylogin.cnf contents)
mysqldump --login-path=${dbPath} ${dbName} ${tables} > ${dumpFile}
