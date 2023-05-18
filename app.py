from peewee import *
from sqlite_utils import *
import requests
import json
from flask import Flask
from flask import render_template
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
    slug = CharField()

#name the table and set primary key
    class Meta:
        table_name = "inspections"
        database = db
        primary_key = CompositeKey('site_no', 'inspection_date', 'inspection_type')

#define column names and data types for my actions table
class Action(Model):
    document = CharField()
    site_no = CharField()
    site_name = CharField()
    city_state_zip = CharField()
    county = CharField()
    enforcement_action = CharField()
    enforcement_action_number = CharField()
    enforcement_action_issued = DateField()
    case_closed = DateField()
    media = CharField()
    program = CharField()
    slug = CharField()

    class Meta:
        table_name = "actions"
        database = db
        primary_key = CompositeKey('site_no', 'enforcement_action_issued', 'media')

class CountyTotal(Model):
    county = CharField()
    sig_count = IntegerField()
    non_count = IntegerField()
    total_count = IntegerField()
    slug = CharField()
    inspection_type_name = CharField()
    inspection_type_count = IntegerField()
    action_type_name = CharField()
    action_type_count = IntegerField()

    class Meta:
        table_name = "county_total_table"
        database = db

#define variables to be displayed on index page
@app.route('/')
def index():
    inspection_count = Inspection.select().count()
    county_totals = CountyTotal.select().order_by(CountyTotal.sig_count.desc())
    template = "index.html"
    return render_template(template, inspection_count=inspection_count, county_totals=county_totals)
   
@app.route('/county/<slug>')
def detail(slug):
    slug = slug
    inspections = Inspection.select().where(Inspection.slug==slug).order_by(Inspection.inspection_date.desc()).limit(10)
    actions = Action.select().where(Action.slug==slug).order_by(Action.enforcement_action_issued.desc()).limit(10)
    inspections_count = len(Inspection.select().where(Inspection.slug==slug))
    actions_count = len(Action.select().where(Action.slug==slug))
    county = inspections[0].county
    county_total = CountyTotal.select().where(CountyTotal.slug==slug).get()
    return render_template("detail.html", slug=slug, county=county, inspections=inspections, actions=actions, inspections_count=inspections_count, actions_count=actions_count, county_total=county_total)

# if i'm capturing a value in a url, it needs to be surrounded by <> in the route
@app.route('/site/<site_no>')
def site(site_no):
    actions = Action.select().where(Action.site_no==site_no).order_by(Action.enforcement_action_issued.desc())
    actions_count = len(Action.select().where(Action.site_no==site_no))
    inspections = Inspection.select().where(Inspection.site_no==site_no).order_by(Inspection.inspection_date.desc())
    inspections_count = len(Inspection.select().where(Inspection.site_no==site_no))
    return render_template("site.html", actions=actions, actions_count=actions_count, inspections=inspections, inspections_count=inspections_count)

@app.route('/county/<slug>/actions')
def actions(slug):
    slug = slug
    actions = Action.select().where(Action.slug==slug).order_by(Action.enforcement_action_issued.desc())
    actions_count = len(Action.select().where(Action.slug==slug))
    inspections_count = len(Inspection.select().where(Inspection.slug==slug))
    county = actions[0].county
    county_total = CountyTotal.select().where(CountyTotal.slug==slug).get()
    return render_template("actions.html", county=county, slug=slug, actions=actions, actions_count=actions_count, inspections_count=inspections_count, county_total=county_total)

@app.route('/county/<slug>/inspections')
def inspections(slug): 
    slug = slug
    inspections = Inspection.select().where(Inspection.slug==slug).order_by(Inspection.inspection_date.desc())
    inspections_count = len(Inspection.select().where(Inspection.slug==slug))
    actions_count = len(Action.select().where(Action.slug==slug))
    county = inspections[0].county
    county_total = CountyTotal.select().where(CountyTotal.slug==slug).get()
    return render_template("inspections.html", slug=slug, county=county, inspections=inspections, inspections_count=inspections_count, actions_count=actions_count, county_total=county_total)

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)