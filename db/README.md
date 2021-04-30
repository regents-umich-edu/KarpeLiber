# `db` Directory

This directory contains two sets of scripts for migrating data from the current production Oracle database to a new production MariaDB one.

* `dev-dump` — This directory contains scripts for dumping the local development MariaDB to SQL scripts, which are then imported into the new production MariaDB.
  * `dump-local-dev.sh` — Shell script to run `mysqldump` on the development MariaDB and produce a `karpeliber_dump_`*`yyyymmddHHMMSS`*`.sql` script.
* `prod-extract` — This directory contains SQL scripts for creating views in the current production Oracle DB.  The views will transform data from the tables into schemas compatible with the new MariaDB.  These views will be dumped to CSV, then imported into the local development MariaDB.
  * `queries.txt` — Oracle SQL statements used for correcting the data to be more compatible with the new schema.  Mostly things like adding IDs, removing dead references, removing poorly-formatted values, etc.
  * `views.sql` — An Oracle SQL script for creating the views.

The data in these databases does not contain any sensitive information.  They are simply the data required to maintain the indices of the volumes.  This data may be committed to the git repository for posterity.  They could be deleted at a later date, but they will remain available in the repository's history.

