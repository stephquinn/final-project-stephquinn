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
    ai_id = IntegerField()
    site_name = CharField()
    city_state_zip = CharField()
    county = CharField()
    inspection_type = CharField()
    fir_inspection_date = DateTimeField()
    permit_no = CharField()
    npdes_no = CharField()
    site_status = CharField()
    site_condition = CharField()
    recommended_actions = TextField()
#name the table and set primary key
    class Meta:
        table_name = "inspections"
        database = db
        primary_key = CompositeKey('ai_id', 'fir_inspection_date')

#define column names and data types for my actions table
class Action(Model):
    ai_id = IntegerField()
    ai_name = CharField()
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
        primary_key = CompositeKey('ai_id', 'enforcement_action_issued')
#define variables to be displayed on index page
@app.route("/")
def index():
    inspection_count = Inspection.select().count()
    #recent_inspections = Inspection.select().order_by(Inspection.fir_inspection_date.desc()).limit(10)
    most_violations = (Inspection
         .select(Inspection.site_name, fn.COUNT(Inspection.result).alias('count'))
         .where(Inspection.result == 'Noncompliance')
         .group_by(Inspection.site_name)
         .order_by(fn.DESC('count'))),limit(10)
    template = "index.html"
    return render_template(template, inspection_count=inspection_count, recent_inspections = recent_inspections, most_violations=most_violations)
   

if __name__ == '__main__':
    # Fire up the Flask test server
    app.run(debug=True, use_reloader=True)