import datetime
from peewee import *

db = SqliteDatabase('wsa.db')

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

    class Meta:
        table_name = "inspections"
        database = db
        primary_key = CompositeKey('site_no', 'inspection_date', 'inspection_type')

class CountyInspectionTotal(Model):
    county = CharField()
    sig_count = IntegerField()
    non_count = IntegerField()
    total_count = IntegerField()
    slug = CharField()

    class Meta:
        table_name = "county_inspection_totals"
        database = db

db.create_tables([CountyInspectionTotal])


# Query all the distinct counties
counties = Inspection.select(Inspection.county, Inspection.slug).distinct()

significant_noncompliance = (Inspection
                             .select(Inspection.county, fn.COUNT(Inspection.site_status).alias('sig_count'))
                             .where(Inspection.site_status == 'Significant Noncompliance')
                             .group_by(Inspection.county))
noncompliance = (Inspection
                 .select(Inspection.county, fn.COUNT(Inspection.site_status).alias('non_count'))
                 .where(Inspection.site_status == 'Noncompliance')
                 .group_by(Inspection.county))

total_county_inspections = (Inspection
                            .select(Inspection.county, fn.COUNT().alias('total_count'))
                            .group_by(Inspection.county))

inspection_types = (Inspection
                            .select(Inspection.county, fn.COUNT(Inspection.inspection_type).alias('type_count'))
                            .group_by(Inspection.inspection_type)
                            .order_by(fn.COUNT().desc()))

# Iterate through the counties and get the aggregate data
for county in counties:
    # Get the significant noncompliance count
    sig_count = significant_noncompliance.where(Inspection.county == county.county).first()
    sig_count = sig_count.sig_count if sig_count else 0

    # Get the noncompliance count
    non_count = noncompliance.where(Inspection.county == county.county).first()
    non_count = non_count.non_count if non_count else 0

    # Get the total inspection count
    total_count = total_county_inspections.where(Inspection.county == county.county).first()
    total_count = total_count.total_count if total_count else 0

    # Get the inspection_type count
    type_count = inspection_types.where(Inspection.county == county.county).first()
    type_count = type_count.type_count if type_count else 0

    # Insert the aggregated data into the CountyInspectionTotal table
    CountyInspectionTotal.create(
        county=county.county,
        slug=county.slug,
        sig_count=sig_count,
        non_count=non_count,
        total_count=total_count,
        inspection_type_name=county.inspection_types,
        inspection_type_count=type_count
    )