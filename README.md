Project Description

Professionals and companies are looking for their best new colleagues. An application that can match them would be great.

The application has two main parts:

Employer Part – the companies can create job ads.

Professionals Part – Individuals create a “company ads” - to show what they can do (qualifications) and what they want and search for.

Functional Requirements

Public Part

The public part must be accessible without authentication.

Login endpoints (for both employers and professionals) (must) – required to access the private endpoints of the application. Login requires username and password.

Register endpoints (for both employers and professionals) (must) –

- Requires username, first name, last name, and password (professionals)

- Requires username, company name and password (companies)

Private part

Accessible only if the user is authenticated.

For Companies: (any of the below can be either a different endpoint, or combined)

o There must be a way to view and edit the Company info

o There must be a way to view all company’s active Job ads

o There must be a way to view all company’s archived (that are matched) Job ads

o There must be a way to create a Job ad

o There must be a way to view and edit details for a Job ad

o There must be a way to search in Company ads

For Professionals:

o There must be a way to view and edit the own Professional info.

o There must be a way to view all own Company ads (more than one are possible)

o There should be a way to set up a “main” ad.

o There must a way to create, view and edit a Company ad.

o There must be a way to search in Job ads.

Company Info

o Description

o Location (city)

o Contacts

o Picture/logo - (should)

o Currently active number of Job ads

o Number of successful matches so far

Professional Info

o Brief summary

o Location (city)

o Status

· Active – the only status that allows active Company ads

· Busy – all Company ads must be hidden or private

o Picture/photo – (should)

o Currently active number of Company ads

o List of matches (must) – could be visible or hidden (should)

Job ads

Only companies can create Job ads.

o Salary range

o Job description

o Location (city or remote or both)

o Status

· Active – visible

· Archived – matched with professional and no longer active

o Set of requirements

· Preset collection of requirements

· Or ability to add requirements – should

· Or ability to add requirements that need to be approved – could

· Requirement levels – should

o List of match requests – visible to the creator only

o Functionality to match a request

· The ad is Archived

· The professional is set on Busy

Company ads

Only professionals can create Company ads.

o Salary range

o Short motivation/description

o Location (city or full remote or both office and remote)

o Status

· Active – the ad is visible in searches

· Hidden – the ad is not visible for anyone but the creator

· Private – the ad can be viewed by id, but do not appear in searches should

· Matched – when is matched by a company

o Skillset

· Preset collection of skills

· Or ability to add skills – should

· Or ability to add skills that need to be approved - could

· Skill level – should

o List of match requests – visible to the creator only

o Functionality to match a request

· The ad status is set to Matched

· The professional is set on Busy

Searching

Both companies and professionals can initiate search

o Companies can search for company ads (must)

o Companies can search for professionals (should)

o Companies can search for other companies (could)

o Professionals can search for job ads (must)

o Professionals can search for companies (should)

o Professionals can search for other professionals (could)

o Search threshold can be set (should) – a way to accept results that are not an exact match.

o Salary range search range (must)

· Search threshold – percent of ads range increase (should)

o List of Skills/Requirements (must)

· Search threshold – number of skills that may be missing from the ads (should)

o Location (must)

o Returns a result where all conditions are met:

o There is intersection between the salary search range and the ad range

· Threshold application: the range of all ads is extended by the given percent symmetrically – min salary is lowered, and maximum salary is increased

§ Example: Threshold 20% - ad range 1000 – 1200 becomes 980 – 1220 for the search i.e., this ad will match search range 900 - 990

o All skills from the search list are in the list of skills/requirements in the ads

· Any combination of (n – t) skills in the search is present in the ad, where n is the number of skills in the search and t is the threshold

o Location matches the city and all full remote ads

Matching

Both companies and professionals can initiate match request.

o Companies can match more than one company ads (must)

o Professionals can match a job ad (must)

Administration

Optionally, create application administration functionality (could)

o Admins approve companies’ and professionals’ registration

o Admins can block/unblock companies and professionals

o Admins can delete application data (profiles, ads etc.)

o Admins can add/delete or approve skills/requirements