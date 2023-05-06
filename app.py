from peewee import *
from sqlite_utils import *
import requests
import json
from flask import Flask
from flask import render_template
from arrow import Arrow
app = Flask(__name__)

#create a Sqlite database to hold my tables (one for inspections and one for enforcement actions)
db = SqliteDatabase('wsa.db')

#define column names and data types for my inspections table
class Inspection(Model):
    document = CharField()
    site_no = IntegerField()
    site_name = CharField()
    city_state_zip = CharField()
    county = CharField()
    inspection_type = CharField()
    inspection_date = DateField()
    permit_no = CharField()
    npdes_no = CharField()
    complaint_tracking_no = CharField()
    inspection_reason = CharField()
    site_status = CharField()
    site_condition = CharField()
    recommended_actions = TextField()
    compliance_assist = BooleanField()
#name the table and set primary key
    class Meta:
        table_name = "inspections"
        database = db
        primary_key = CompositeKey('site_no', 'inspection_date', 'inspection_type')

#define column names and data types for my actions table
class Action(Model):
    document = CharField()
    site_no = IntegerField()
    site_name = CharField()
    city_state_zip = CharField()
    county = CharField()
    enforcement_action = CharField()
    enforcement_action_number = CharField()
    enforcement_action_issued = DateTimeField()
    case_closed = DateTimeField()
    media = CharField()
    program = CharField()
#name the table and set primary key
    class Meta:
        table_name = "actions"
        database = db
        primary_key = CompositeKey('site_no', 'enforcement_action_issued', 'media')

class CountyInspectionTotal(Model):
    county = CharField()
    sig_count = IntegerField()
    non_count = IntegerField()
    total_count = IntegerField()

    class Meta:
        table_name = "county_inspection_totals"
        database = db

#define variables to be displayed on index page
@app.route('/')
def index():
    inspection_count = Inspection.select().count()
    county_totals = CountyInspectionTotal.select().order_by(CountyInspectionTotal.sig_count.desc())
    template = "index.html"
    return render_template(template, inspection_count=inspection_count, county_totals=county_totals)
   
@app.route('/county/<slug>')
def detail(slug):
    county = slug
    inspections = Inspection.select().where(Inspection.county==slug).order_by(Inspection.inspection_date.desc()).limit(10)
    actions = Action.select().where(Action.county==slug).order_by(Action.enforcement_action_issued.desc()).limit(10)
    inspections_count = len(Inspection.select().where(Inspection.county==slug))
    actions_count = len(Action.select().where(Action.county==slug))
    return render_template("detail.html", county=county, inspections=inspections, actions=actions, inspections_count=inspections_count, actions_count=actions_count)

@app.route('/county/<slug>/actions')
def actions(slug):
    county = slug
    actions = Action.select().where(Action.county==slug).order_by(Action.enforcement_action_issued.desc())
    actions_count = len(Action.select().where(Action.county==slug))
    return render_template("actions.html", county=county, actions=actions, actions_count=actions_count)

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)