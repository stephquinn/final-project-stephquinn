[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=10834836)
# final-project
FINAL UPDATE:

My app uses data from the Maryland Water and Science Administration's reporting on inspections and enforcement actions it conducts on sites throughout the state that discharge waste into the state's waters. My aim was to shed light on the behavior of the WSA and the sites it oversees by a) calculating and displaying aggregates and b) bringing together data from the WSA's inspection and enforcement action datasets, which are published separately. It's deployed via codespaces.

My first step was to store WSA inspection and action data in a SQLite database and display it on a page. I drew this data from separate inspection and action csv files. I used a bash file to insert the data from these csv files into my SQLite database. Initially, I think I only defined one Inspection model in my app.py and displayed all of the columns in my index.html. I didn't realize at first that every time I ran the bash file, it was adding the data from the csv into my db on top of the same data that was already there. I had to add code to my bash file to remove the existing db before reloading the data.

The next week, I revamped the index page to display the total numbers of inspections - and numbers of inspections that detected "significant noncompliance" and "noncompliance" - for each county and the City of Baltimore. To do this, I used my existing Inspection table to create a new table containing these aggregates in a separate aggregates.py file. I also linked each county name on the index page to a detail page displaying inspections and enforcement actions for that area. Multiple tables and multiple pages!

From there, I quickly got very confused. I had a lot of trouble figuring out how the various files fit together and where I was creating a label that could be as random as "donkey" and when I had to be very precise in referring to a specific existing label. I struggled to get the tables on my detail page to display the records in reverse chronological order, which I realized was because the dates in the records were not formatted correctly. I used an update_data.py page to change these dates in my inspection and action tables, which meant that I then had to remember the order in which I had to run the various files to get my app up and running. Revising my bash data file to run both my aggregates and update_data files was very helpful.

I distinguished between county detail pages that displayed the most recent inspections and actions and further detail pages that listed all that county's inspections and actions separately. I realized that I hadn't really done anything to allow users to track the state's history of inspecting and penalizing individual sites, so I linked each site name in the detail page to a site page listing all the inspections and actions for that site.

In the end, writing my blog post tonight was a gamechanger in forcing me to write out how different elements of my app fit together. I think if I had been more diligent about explaining to myself my understanding of how the app worked throughout this process, I might have felt less lost. On the other hand, I feel proud of what I've accomplished, even though there's a lot more that I could do.

If I were to really "publish" this app, I would probably write a scraper and a yaml file so my app could update with new WSA data and to automate the app's workflow. Right now, I'm using old data that isn't updating, which is a weakness.




--
breadcrumbs?

5/5 update:
Things to fix/change:
1. Make sure I've added slug columns to all my tables (compliance and actions csv files and their corresponding models plus CountyInspectionTotals model) and that the slug values are in the correct column.
2. Display correct numbers of "significant noncompliance" inspections for each county on index page. This means calculating these numbers correctly on aggregates.py and getting them to display on the index page.
3. Define routes and variables needed to display index, county detail, inspections detail and actions detail pages.
4. Write code so that slug refers to the county represented on the county detail page, so that actions and inspections detail pages populate the tables for those page with the data. (Is this by correctly defining the href in the templates?)
5. Do I need two separate update_date.py and aggregates.py pages? Can any of this be put in the same file?

This was how I got the tables on my county detail page to display in reverse chronological order:
I was having trouble getting the tables on my detail page to display in reverse chronological order. The changes you sent me using the csv module worked for the inspections table, but not for the actions table. For the actions table, I think it didn't work because of the NAs in the date column. ChatGPT gave me a possible solution (adding this: if row['enforcement_action_issued'] != 'NA':) that for some reason worked for some but not all of the rows with NAs, and then it recommended pandas as an alternative. This worked! So now my tables are in reverse chronological order.

This was my original to-do list for this week:
put totals of inspections and actions at the top
then there could be a second detail page showing ALL the inspections for the county or ALL the actions for the county
/county/slug/inspections
/county/slug/actions

Regarding look and feel, I'm shooting for basic, clean design and consistency across pages. It might be good to do more to highlight the most important elements on the page. For instance, I could probably make the text delivering important information about numbers of violations bigger. Maybe numbers of significant violations could be in bold on the index page?


4/28 update: I accomplished a lot this week! What I have right now is:
- an index page that lists Maryland counties in order of most violations to least, with the numbers of violation for each county and each county name linked to its detail page 
- detail pages that display the number of events (inspections and enforcement actions) for that county, as well as tables showing inspections and enforcement actions in the county

I got the data on the page! I feel like I had a breakthrough this week.

Some relatively simple things to do: 
- Add "significant compliance" and other "out of compliance" categories to filter on index page.
- Display table results in chronological order.

Right now, my app allows users to search for WSA inspections and enforcement actions by county. [oops I lied - maybe for next turn-in] Although it occurs to me that since there aren't that many counties in Maryland the search bar might be more useful if it allowed people to search by zip code, or maybe if it were a full text search? That way, if users were curious about a particular site or the immediate vicinity of where they live, they could find relevant results quickly.

I'd like to work on how data is displayed on the detail page. Right now, it's pretty difficult to parse the results, especially for counties that have the most inspections and enforcement actions. Also, right now the inspections and enforcement actions are displayed separately. Eventually I want people to be able to trace the relationship between inspections and enforcement actions. What if I display the inspections and enforcement actions as one table, in chronological order, on the county detail page, and from the county detail page, give users the option of clicking on a site name to see its history of inspections and enforcement actions on another detail page? Is that too many detail pages?

Looking back at my original vision for the app, I'm also reminded of the filter bar here: https://opendata.maryland.gov/stories/s/iape-ym8p. Would it be really hard to build that?

Next week I might focus on adding full-text search to the index page, as well as enabling users to click to an additional detail page listing inspections and actions for individual sites.

--

4/21 update: My main goal this week was to write code to load data from the WSA inspections table and display it in table form - which I have more or less done, with a lot of help. Since I know that my final product will use data from both the inspections and enforcement actions tables, I described the column names and datatypes for both in my app.py file, and my data bash file loads data from both tables. That said, I am currently only displaying data from the inspections table, because I need to look more closely at my data to figure out how I want to use data from the actions table.

Blockers: 

I used the sqlite utils documentation for the code I originally used to load my inspection data, and that code included pk=id as a placeholder. In keeping this code, I inadvertently established the expectation that a column named id (which didn't exist) would be the primary key. So peewee kept giving me an error, and I couldn't load my table. With your help (thank you!), I deleted my db file and redefined my primary key. So now I have a basic table. 

I also learned the importance of keeping variable and table names consistent - and keeping files for loading and displaying data separate. 

Right now, I'm not sure I understand why inspections appear to repeat when I fire up the server. For instance, why do there seem to be four identical inspection rows for 24 Duck Hollow Dr in Elkton from May 20? There has to be a way to write code to not display duplicate rows. Maybe that can be one thing I do this coming week.

Also, what will I do about sites that are residential addresses, like 24 Duck Hollow Dr? This is the kind of information I would probably omit for someone's house, but there's no other site name. Also, there are some things that are formatted strangely in my table - spaces missing between words and a hard-to-read date-time format, for instance. I will aim to fix those this week too.

Plans: 

This coming week, it would be great to link site ids from the inspections table to site ids in the actions table and make it so that users can click on site names to call up enforcement actions for those sites on a detail page. I think I can probably figure out the basics of how to do this from my repos for our First and Second News Apps.

--
First update:
Just wanted to preface this by saying that I'd really appreciate guidance about what to prioritize/what's doable or not/where to start!

Ideally, my news app would show which kinds of violations the Maryland Department of the Environment's Water and Science Administration is likely to act on - and which it tends to ignore. It would also be great if it could enable users to see whether the broad state-wide trends that the app underlines also pertain where they live. This would require joining two datasets: WSA compliance inspections (https://opendata.maryland.gov/Energy-and-Environment/Maryland-Department-of-the-Environment-Water-and-S/hxmu-urvx) and WSA enforcement actions (https://opendata.maryland.gov/Energy-and-Environment/Maryland-Department-of-the-Environment-Water-and-S/qbwh-5vec). 

A scaled-down (and maybe more achievable) version of my news app would build on WSA's current compliance dashboard (https://opendata.maryland.gov/stories/s/iape-ym8p). Right now, WSA's dashboard does a pretty good job showing users where and what kind of inspections it does - the user can use the filter bar at the top of the dashboard to see the sites and counties where WSA has conducted the most inspections, and it's possible to filter by date. You can filter by site name, too, to get an idea of how individual sites have performed. But you can't really see the aggregate results of inspections. Which sites, for instance, have the worst inspection records? Are they concentrated somewhere? It would be great to be able to filter by the result of an inspection (site_status) combined with site name or county.

One possibility might be to add site_status and maybe recommended_actions to the current filter bar.

I could add a map showing geographical distribution of cases where WSA inspections revealed noncompliance. (Would it be possible to do that while still showing all inspections in the table below, including ones that were "satisfactory" or that had other inspection outcomes?)

I'm trying to figure out what useful detail pages would look like. I'm thinking I could use the site numbers, which appear in both the compliance and enforcement datasets, to pull together rows from the two datasets related to the same site. Clicking on a site name in a row could then open up a page listing inspections and enforcement actions for that site. And maybe clicking on a county name in a row could open a page showing how many inspections in that county resulted in rulings of noncompliance and/or enforcement actions?

Would it be crazy to have the table part of the app show both enforcement actions and compliance data? If I want to pull together compliance and enforcement data for the site detail pages, I would need both sets of data in the table, right?

Sane Data Updates questions:

The data updates daily, according to MDE. There's no "last updated" column, but I think I could probably use the inspection_date column in the compliance dataset and the enforcement_action_issued column in the enforcement dataset as proxies. So in order to do incremental updates, I can follow the pseudocode guidance from Sane Data Updates of checking for values in the above date columns from the past day every day and process new records accordingly. 

Thinking about what counts as an update, I'm thinking new records, and maybe updates where there's a date range within a single row. For instance, in the enforcement data, there are two date columns: enforcement_action_issued and case_closed. I don't see a primary key. For a natural key, I think I'd have to use more than two columns: site_no, media, program and enforcement_action_issued? That seems crazy and maybe not a top priority. Maybe I'll just stick with new records.

To alert users to changes, it would be great if I could have the table part of the app display rows in reverse chronological order. WSA's current dashboard does not do this. Would it be difficult to do that in my app?

I don't think it's necessary to display complete addresses - I would probably just display the city/town and county. I think some of the addresses are private residences, and I wouldn't want to display those. Some of the data might not be super relevant to the average user. From the compliance dataset, I might filter out the NPDES number, permit number or complaint number, since most users won't have those. For enforcement, I could probably filter out the enforcement action number.

