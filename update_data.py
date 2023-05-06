import csv
import datetime

rows = []

with open("static/compliance.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        row['inspection_date'] = datetime.datetime.strptime(row['inspection_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
        rows.append(row.values())

with open("static/compliance2.csv", "w") as output:
    writer = csv.writer(output)
    writer.writerow(["document","site_no","site_name","street_address","city_state_zip","county","inspection_type","inspection_date","permit_no","npdes_no","complaint_tracking_no","inspection_reason","site_status","site_condition","recommended_actions","compliance_assist"])
    writer.writerows(rows)