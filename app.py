from peewee import *
import requests
from flask import Flask
from flask import render_template
app = Flask(__name__)

db = SqliteDatabase('wsa.db')

class Inspection(Model):
    url= TextField()
    ai_id= IntegerField()
    site_name= CharField()
    addressinfo= CharField()
    city_state_zip= CharField()
    county= CharField()
    inspection_type= CharField()
    fir_inspection_date= DateField()
    permit_no= CharField()
    npdes_no= CharField()
    site_status= CharField()
    site_condition= CharField()
    recommended_actions= TextField()
    compliance_assist= BooleanField()

    class Meta:
        table_name = "inspections"
        database = db

class EnforcementAction(Model):
    #START HERE

@app.route("/")
def wsa_compliance():
    url = "https://opendata.maryland.gov/resource/hxmu-urvx.json"
    response = requests.get(url)
    wsa_compliance = response.json()
    return wsa_compliance

@app.route("/sitename/<slug>")


@app.route("/")
def index():
    template = 'index.html'
    return render_template(template)

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)