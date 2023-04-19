from peewee import *
import requests
from flask import Flask
from flask import render_template
app = Flask(__name__)

db = SqliteDatabase('wsa.db')

class Inspection(Model):
    ai_id= IntegerField(unique=True)
    site_name= CharField()
    city_state_zip= CharField()
    county= CharField()
    inspection_type= CharField()
    fir_inspection_date= DateTimeField()
    permit_no= CharField()
    npdes_no= CharField()
    site_status= CharField()
    site_condition= CharField()
    recommended_actions= TextField()
    compliance_assist= BooleanField()

    class Meta:
        table_name = "inspections"
        database = db

class Enforcement(Model):
    ai_id: IntegerField(unique=True)
    ai_name: CharField()
    city_state_zip: CharField()
    county: CharField()
    enforcement_action: CharField()
    enforcement_action_number: CharField()
    enforcement_action_issued: DateTimeField()
    case_closed: DateTimeField()
    media: CharField()
    program: CharField()

    class Meta:
        table_name = "enforcements"
        database = db

def get_compliance():
    url = "https://opendata.maryland.gov/resource/hxmu-urvx.json"
    response = requests.get(url)
    wsa_compliance = response.json()
    return wsa_compliance

@app.route("/")
def index():
    inspection_count = Inspection.select().count()
    template= "index.html"
    return render_template(template, count=inspection_count)


if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)