

wget -O inspections.json "https://opendata.maryland.gov/resource/hxmu-urvx.json"

sqlite-utils insert wsa.db inspections inspections.json