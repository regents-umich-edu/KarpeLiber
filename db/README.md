# `db` Directory

This directory contains two sets of scripts for migrating data from the current production Oracle database to a new production MariaDB one.

The data in these databases does not contain any sensitive information.  They are simply the data required to maintain the indices of the volumes.  This data may be committed to the git repository for posterity.  They could be deleted at a later date, but they will remain available in the repository's history.

* `dev-dump` — This directory contains scripts for dumping the local development MariaDB to SQL scripts, which are then imported into the new production MariaDB.
  * `dump-local-dev.sh` — Shell script to run `mysqldump` on the development MariaDB and produce a `karpeliber_dump_`*`yyyymmddHHMMSS`*`.sql` script.
* `prod-dump` — This directory contains SQL scripts for creating views in the current production Oracle DB.  The views will transform data from the tables into schemas compatible with the new MariaDB.  These views will be dumped to CSV, then imported into the local development MariaDB.
  * `queries.txt` — Oracle SQL statements used create transformative views of the original tables.  These correct the data to be more compatible with the new schema.  Mostly things like adding IDs, removing dead references, removing poorly-formatted values, etc.
  * `views.sql` — An Oracle SQL script for creating the views.



---

## Migrating Data

The following describes the process of migrating data from the current production DB to the new DB.

### Dump Production DB

1. Create views in the production DB using the queries in `prod-dump/views.sql`.
2. Use a DB client (e.g., DBeaver) to connect to the production DB and export each of the views' contents to CSV files.  That will produce files like:
   1. V_ITEM_*nnnnnnnnnnnn*.csv
   2. V_ITEM_NOTE_*nnnnnnnnnnnn*.csv
   3. V_ITEM_PAGE_*nnnnnnnnnnnn*.csv
   4. V_NOTE_TYPE_*nnnnnnnnnnnn*.csv
   5. V_PAGE_MAPPING_*nnnnnnnnnnnn*.csv
   6. V_TOPIC_*nnnnnnnnnnnn*.csv
   7. V_TOPIC_NOTE_*nnnnnnnnnnnn*.csv
   8. V_VOLUME_*nnnnnnnnnnnn*.csv
3. Verify dump success by comparing the number of rows in each view to the number of lines in the CSV files.

### Import Into Development DB

1. If the development DB has already been in use, duplicate the folder to make a backup copy.
2. Truncate all tables corresponding to the CSV files.  Note that because of foreign constraints, it may be necessary to use the "force" option when truncating.  (DBeaver's CSV import offers a feature to truncate tables before loading data, but it never works, hence this truncation step.)
3. For each of the CSV files, import the data into the corresponding tables.  Ensure the following import options are specified:
   1. Set empty strings to NULL
   2. Date/time format: "yyyy-MM-dd[ HH:mm:ss[.S]]"
4. DBeaver won't disable referential integrity while importing CSV.  So, import tables in this order to avoid foreign constraint errors:
   1. note_type
   2. volume
   3. page_mapping
   4. topic
   5. topic_note
   6. item
   7. item_note
   8. item_page
5. Verify import success by comparing the number of rows in each table to the number of lines in the CSV files.

### Dump Development DB

1. TODO: Add steps…

### Import Into New Production DB

1. TODO: Add steps…

