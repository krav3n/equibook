#!/usr/bin/env sh

# Start MySQL
/usr/bin/mysqld_safe > /dev/null 2>&1 &

# Sleep to ensure that mysql server is up and running...
sleep 3

# Create Databases
mysql -e "DROP DATABASE IF EXISTS \`dev\`;"
mysql -e "CREATE DATABASE \`dev\`;"
mysql -e "GRANT ALL ON \`dev\`.*  TO ''@'%' IDENTIFIED BY 'abcd';"
mysql -e "GRANT ALL ON \`test\`.* TO ''@'%' IDENTIFIED BY 'abcd';"
mysql -e "DROP DATABASE IF EXISTS \`loggerdev\`;"
mysql -e "CREATE DATABASE \`loggerdev\`;"
mysql -e "GRANT ALL ON \`loggerdev\`.*  TO ''@'%' IDENTIFIED BY 'abcd';"
mysql -e "GRANT ALL ON \`loggertest\`.* TO ''@'%' IDENTIFIED BY 'abcd';"

# Shutdown MySQL
killall -9 mysqld_safe mysqld
