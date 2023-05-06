#remove existing db to avoid duplicate records
rm wsa.db

sqlite-utils insert wsa.db inspections static/compliance2.csv --csv

sqlite-utils insert wsa.db actions static/actions2.csv --csv




