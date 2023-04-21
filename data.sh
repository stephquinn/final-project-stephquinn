

wget -O inspections.json "https://opendata.maryland.gov/resource/hxmu-urvx.json"

sqlite-utils insert wsa.db inspections inspections.json

wget -0 actions.json "https://opendata.maryland.gov/resource/qbwh-5vec.json"

sqlite-utils insert wsa.db actions actions.json