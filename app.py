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
    inspection_date = DateTimeField()
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
    site_name = CharField
    city_state_zip = CharField()
    county = CharField()
    enforcement_action = CharField()
    enforcement_action_no = CharField()
    enforcement_action_issued = DateTimeField()
    case_closed = DateTimeField()
    media = CharField()
    program = CharField()
#name the table and set primary key
    class Meta:
        table_name = "actions"
        database = db
        primary_key = CompositeKey('site_no', 'enforcement_action_issued', 'media')

#define variables to be displayed on index page
#maybe eventually add "significant noncompliance" and other noncompliance categories
@app.route('/', methods=['GET', 'POST'])
def index():
    inspection_count = Inspection.select().count()
    recent_inspections = Inspection.select().order_by(Inspection.inspection_date.desc()).limit(10)
    most_violations = (Inspection
         .select(Inspection.county, fn.COUNT(Inspection.site_status).alias('count'))
         .where(Inspection.site_status == 'Noncompliance')
         .group_by(Inspection.county)
         .order_by(fn.COUNT(Inspection.site_status).desc()))
    template = "index.html"
    return render_template(template, inspection_count=inspection_count, recent_inspections = recent_inspections, most_violations=most_violations)
   
@app.route('/county/<slug>')
def detail(slug):
    county = slug
    inspections = Inspection.select().where(Inspection.county==slug)
    actions = Action.select().where(Action.county==slug)
    events_count = (Inspection.select(fn.SUM(Inspection.inspections).alias('sum'))
                    .where(Inspection.county==slug)
                    .scalar() 
                    + Action.select(fn.SUM(Action.actions).alias('sum'))
                    .where(Action.county==slug)
                    .scalar())
    return render_template("detail.html", county=county, inspections=inspections, actions=actions, events_count=events_count)

  

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)