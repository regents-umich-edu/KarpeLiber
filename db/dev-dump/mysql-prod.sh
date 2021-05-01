#!/bin/sh --

cat << EOT
Before using this, ensure that:

1. login-path "regentsproceedingsindex-prod" has been configured in
   ~/.mylogin.cnf and connects to 127.0.0.1:7777 with the username and
   password of the production DB.  (See: mysql_config_editor)

2. Use the following OpenShift CLI command to connect port 7777 to the
   production database.  (Use "oc get pods" to get exact name of the
   pod to use in the command.)

     oc port-forward karpeliber-nn-xxxxx 7777 &

EOT

mysql --login-path=regentsproceedingsindex-prod regentsproceedingsindex
