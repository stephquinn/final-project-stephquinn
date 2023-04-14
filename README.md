[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=10834836)
# final-project

Ideally, my news app would show which kinds of violations the Maryland Department of the Environment's Water and Science Administration is likely to act on - and which it tends to ignore. It would also be great if it could enable users to see whether the broad state-wide trends that the app underlines also pertain where they live. This would require joining two datasets: WSA compliance inspections (https://opendata.maryland.gov/Energy-and-Environment/Maryland-Department-of-the-Environment-Water-and-S/hxmu-urvx) and WSA enforcement actions (https://opendata.maryland.gov/Energy-and-Environment/Maryland-Department-of-the-Environment-Water-and-S/qbwh-5vec).

A scaled-down (and maybe more achievable) version of my news app would build on WSA's current compliance dashboard (https://opendata.maryland.gov/stories/s/iape-ym8p) by adding a map showing geographical distribution of cases where WSA inspections revealed noncompliance, filtering for the past five years. It would also allow users to click on cells in individual rows to go to detail pages. Would it be possible, for instance, to click on "Frederick" in the county cell of a row and open up a page saying how many inspections conducted in Frederick County resulted in rulings of noncompliance and/or enforcement actions? And would it be possible to click on a particular site and open up a page showing all inspection results and any enforcement actions?

Right now, WSA's dashboard does a pretty good job showing users things about where and what kind of inspections it does - the user can use the filter bar at the top of the dashboard to see the sites and counties where WSA has conducted the most inspections, and it's possible to filter by date. You can filter by site name, too, but you can't really see the aggregate results of inspections. Which sites, for instance, have the worst inspection records? Are they concentrated somewhere? It would be great to be able to filter by the result of an inspection (site_status) combined with site name or county.

-
The violations dataset covers March 4, 2004 to the present and contains 1,875 records. The compliance inspections dataset covers July 1, 2016 to the present and contains some 31,800 records. The enforcement actions dataset covers October 15, 1998 to the present and contains 1,211 records. 

This page (https://mde.maryland.gov/programs/water/Compliance/Pages/index.aspx) is the best explanation of the compliance data that I've found. Each row is an inspection, there are 39 values that appear in the "inspection_type" column, and inspections can result in a variety of dispositions ("site_status"), including "noncompliance," "significant noncompliance" and "satisfactory/compliance." Nowhere near all the instances of noncompliance show up in the violations table. When I used R to filter for all inspections where the site_status was "noncompliance" or "significant noncompliance," I got almost 11,000 rows since 2018, while there are only 507 rows if I filter the violations table with a floor date of 2018-01-01. It might also be difficult to match individual instances of noncompliance with specific enforcement actions, but I can probably use the site numbers to pull together rows from the two datasets related to the same site.

With all that in mind, I think I should start by trying to make something like the "first news app" we built in class for the WSA compliance data, filtering for noncompliance to begin with and potentially narrowing things down further  to particular kinds of inspections later in the process.
-
Sane Data Updates questions:

The data updates daily, according to MDE. There's no "last updated" column, but I think I could probably use the inspection_date column in the compliance dataset and the enforcement_action_issued column in the enforcement dataset as proxies. So in order to do incremental updates, I can follow the pseudocode guidance from Sane Data Updates of checking for values in the above date columns from the past day and process new records accordingly. 

Thinking about what counts as an update, I'm thinking new records, as well updates where there's a date range within a single row. For instance, in the enforcement data, there are two date columns: enforcement_action_issued and case_closed. I don't see a primary key. For a natural key, I think I'd have to use more than two columns: site_no, media, program and enforcement_action_issued? That seems crazy. Maybe I'll just stick with new records.

To alert users to changes, I'm thinking of using an update timeline that lists records in reverse chronological order.

I don't have ethical qualms about displaying any of this data, but some of it might not be super relevant to the average user.

