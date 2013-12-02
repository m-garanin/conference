# !/bin/sh

psql -d template1 -U postgres -c "DROP DATABASE test_conference;"
psql -d template1 -U postgres -c "CREATE DATABASE test_conference WITH OWNER postgres ENCODING='UNICODE';"



