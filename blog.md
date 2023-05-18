I’m going to write about how I learned how to build a table of aggregates by querying state government data and use that table to display aggregates as part of a news app.

My data was from the Maryland Water and Science Administration’s reporting on its inspections of sites that discharge waste into state waters - and on the enforcement actions it takes when sites repeatedly violate the state and federal terms of those permits. WSA provides inspection and enforcement data in separate tables. I wanted to make it easier to see which sites have the worst inspection records and when noncompliance results in state penalties.

At a certain point in my development process, I wanted to provide some aggregates at the top of detailed tables for counties and sites to help users interpret the data.

I already had a table my app created from WSA’s inspections data in my aggregates.py file. This table, called CountyInspectionTotal, showed the total number of inspections that WSA had reported in each county in the state (and the City of Baltimore), as well as the numbers of inspections in each area where the result was “significant noncompliance” and “noncompliance.” 

Building on this table, I wanted to add two columns to show what kind of inspections were the most common in each area and, secondly, how often those inspection types occurred in each area. 

In my aggregates.py file, I indicated the names and data types of the columns I wanted to add to my CountyInspectionTotal table. In the "Meta" section, I named the table and specified the database where the data would live. (Note that I had already defined db=wsa.db earlier in the file.)

class CountyInspectionTotal(Model):
    county = CharField()
    sig_count = IntegerField() #This was the number of inspections resulting in a "significant noncompliance" rating
    non_count = IntegerField() #This was the number of inspections resulting in a "noncompliance" rating
    total_count = IntegerField() #This was the total number of inspections for the area
    slug = CharField()
    inspection_type_name = CharField() #This one was new!
    inspection_type_count = IntegerField() #This one was new!

    class Meta:
        table_name = "county_inspection_totals"
        database = db

As I figured out what to do next, it helped me to visualize the table I was creating. I knew that for each county, there was going to be a type of inspection that had happened the most often and number of times that inspection type had happened. Two columns: inspection_type_name and inspection_type_count.

County      Sig_count       Non_count       Total_count ... Inspection_type_name       Inspection_type_count
PG          28              514             1644            NPDES Construction Activity     840

I'm new to Python, so when figuring out how to define these new variables, I thought about what I would do in R.

This was my first stab:

inspections%/%
    group_by(inspection_type)%/% #For each inspection_type value...
    summarize(count=n())%/% #Count the number of occurrences...
    arrange(desc(count)) #And list the inspection types in order from most to least common.

In this day and age, ChatGPT is a natural ally for writing code in a language you are only beginning to learn.  So I asked it to translate my R into Python. I had to specify that I wanted to use Peewee ORM. This is what it gave me:


from peewee import *

# Assuming you have a Peewee model named 'Inspection' for the 'wsa_compliance' table

# Group by inspection_type and calculate the count
grouped = Inspection.select(Inspection.inspection_type, fn.COUNT().alias('count')) \
                    .group_by(Inspection.inspection_type)

# Sort the grouped data in descending order based on count
sorted_data = grouped.order_by(fn.COUNT().desc())

# Print the sorted data
for item in sorted_data:
    print(item.inspection_type, item.count)

Not bad! I combined the grouping, calculating and sorting, and I added a .where() so that I could limit the results to one county. I had forgotten to do that in my R code.

Here's what I ended up with:
inspection_types = Inspection.select(Inspection.inspection_type, fn.COUNT().alias('type_count')).where(Inspection.county == county.county).group_by(Inspection.inspection_type).order_by(fn.COUNT().desc())

A couple of things to look out for:
1. Check to make sure the attributes you're referencing in your model match the column_names you defined earlier. Thus inspection_type can't be inspection_variety or type_inspection. It has to match the model!
2. For the .where(), Inspection.county==county.county means that you are filtering out records where the value in the county column of the Inspection table matches the value corresponding to the specific county you are filtering for.

So inspection_types gives us this for the given county:
inspection_type     type_count
a                   5
b                   4
c                   3
d                   2
e                   1

What we want is just the first cell in each column. Time to define more variables!

# Get the name of the most common inspection type
    inspection_type_name = inspection_types[0].inspection_type  #In the first record/row of inspection_types, isolate the value in the column inspection_type.

# Get the number of that kind of inspection
    inspection_type_count = inspection_types[0].type_count  #In the first record/row of inspection_types, isolate the value in the column type_count.

Now we have our data!

Now to display it. That means


