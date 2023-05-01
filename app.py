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

#define variables to be displayed on index page
@app.route('/', methods=['GET', 'POST'])
def index():
    significant_noncompliance = (Inspection
         .select(Inspection.county, fn.COUNT(Inspection.site_status).alias('sig_count'))
         .where(Inspection.site_status == 'Significant Noncompliance')
         .group_by(Inspection.county)
         .order_by(fn.COUNT(Inspection.site_status).desc()))
    noncompliance = (Inspection
         .select(Inspection.county, fn.COUNT(Inspection.site_status).alias('non_count'))
         .where(Inspection.site_status == 'Noncompliance')
         .group_by(Inspection.county)
         .order_by(fn.COUNT(Inspection.site_status).desc()))
    total_county_inspections = (Inspection
        .select(Inspection.county, fn.COUNT().alias('total_count'))
        .group_by(Inspection.county)
        .order_by(fn.COUNT().desc()))
    union_query = (significant_noncompliance
               .select(significant_noncompliance.county.alias('county_display'), significant_noncompliance.sig_count.alias('sig_count'))
               .union(noncompliance.select(noncompliance.county, noncompliance.non_count.alias('non_count')))
               .union(total_county_inspections.select(total_county_inspections.county, total_county_inspections.total_count.alias('total_count')))
               .order_by(significant_noncompliance.sig_count.desc()))
    inspection_count = Inspection.select().count()
    template = "index.html"
    return render_template(template, inspection_count=inspection_count, noncompliance=noncompliance, significant_noncompliance=significant_noncompliance, total_county_inspections=total_county_inspections, union_query=union_query)
   
@app.route('/county/<slug>')
def detail(slug):
    county = slug
    inspections = Inspection.select().where(Inspection.county==slug)
    actions = Action.select().where(Action.county==slug)
    events_count = len(Action.select().where(Action.county==slug)) + len(Inspection.select().where(Inspection.county==slug))
    return render_template("detail.html", county=county, inspections=inspections, actions=actions, events_count=events_count)

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)