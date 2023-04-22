
#get WSA inspection files as json using Maryland Open Data API endpoint 
wget -O inspections.json "https://opendata.maryland.gov/resource/hxmu-urvx.json"
#insert the above data in a Sqlite database called wsa.db
sqlite-utils insert wsa.db inspections inspections.json

#get WSA enforcement actions as json using Maryland Open Data API endpoint
wget -O actions.json "https://opendata.maryland.gov/resource/qbwh-5vec.json"
#insert the above data in my Sqlite database
sqlite-utils insert wsa.db actions actions.json