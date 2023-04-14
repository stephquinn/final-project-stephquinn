[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=10834836)
# final-project

Just wanted to preface this by saying that I'd really appreciate guidance about what to prioritize/what's doable or not/where to start!

Ideally, my news app would show which kinds of violations the Maryland Department of the Environment's Water and Science Administration is likely to act on - and which it tends to ignore. It would also be great if it could enable users to see whether the broad state-wide trends that the app underlines also pertain where they live. This would require joining two datasets: WSA compliance inspections (https://opendata.maryland.gov/Energy-and-Environment/Maryland-Department-of-the-Environment-Water-and-S/hxmu-urvx) and WSA enforcement actions (https://opendata.maryland.gov/Energy-and-Environment/Maryland-Department-of-the-Environment-Water-and-S/qbwh-5vec). 

A scaled-down (and maybe more achievable) version of my news app would build on WSA's current compliance dashboard (https://opendata.maryland.gov/stories/s/iape-ym8p). Right now, WSA's dashboard does a pretty good job showing users where and what kind of inspections it does - the user can use the filter bar at the top of the dashboard to see the sites and counties where WSA has conducted the most inspections, and it's possible to filter by date. You can filter by site name, too, to get an idea of how individual sites have performed. But you can't really see the aggregate results of inspections. Which sites, for instance, have the worst inspection records? Are they concentrated somewhere? It would be great to be able to filter by the result of an inspection (site_status) combined with site name or county.

One possibility might be to add site_status and maybe recommended_actions to the current filter bar.

I could add a map showing geographical distribution of cases where WSA inspections revealed noncompliance. (Would it be possible to do that while still showing all inspections in the table below, including ones that were "satisfactory" or that had other inspection outcomes?)

I'm trying to figure out what useful detail pages would look like. I'm thinking I could use the site numbers, which appear in both the compliance and enforcement datasets, to pull together rows from the two datasets related to the same site. Clicking on a site name in a row could then open up a page listing inspections and enforcement actions for that site. And maybe clicking on a county name in a row could open a page showing how many inspections in that county resulted in rulings of noncompliance and/or enforcement actions?

Would it be crazy to have the table part of the app show both enforcement actions and compliance data? If I want to pull together compliance and enforcement data for the site detail pages, I would need both sets of data in the table, right?

Sane Data Updates questions:

The data updates daily, according to MDE. There's no "last updated" column, but I think I could probably use the inspection_date column in the compliance dataset and the enforcement_action_issued column in the enforcement dataset as proxies. So in order to do incremental updates, I can follow the pseudocode guidance from Sane Data Updates of checking for values in the above date columns from the past day every day and process new records accordingly. 

Thinking about what counts as an update, I'm thinking new records, as well updates where there's a date range within a single row. For instance, in the enforcement data, there are two date columns: enforcement_action_issued and case_closed. I don't see a primary key. For a natural key, I think I'd have to use more than two columns: site_no, media, program and enforcement_action_issued? That seems crazy. Maybe I'll just stick with new records.

To alert users to changes, it would be great if I could have the table part of the app display rows in reverse chronological order. WSA's current dashboard does not do this. Would it be difficult to do that in my app?

I don't have ethical qualms about displaying any of this data, but some of it might not be super relevant to the average user.

