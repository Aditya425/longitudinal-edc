🚧 Remaining Features
1️⃣ Study Setup

Currently missing completely.

Need:

Study Detail
    ↓
Study Setup

Allow coordinator to configure:

Visit types
Required visits
Visit windows

Currently your visit definitions are hardcoded:

VISIT_TYPES = [
    ...
]

Instead they should come from the database.

Difficulty:
⭐⭐⭐⭐

2️⃣ Visit Detail Page

Currently only list of visits exists.

Need a page like:

Visit

Participant
Status

Due Date

Window

Actual Date

Forms

Complete Visit

Difficulty:
⭐

3️⃣ Complete Visit

Need

Mark Completed

Should

update actual_date
update status
save completion

Difficulty:
⭐

4️⃣ Window Validation

Currently missing.

Need:

if actual_date outside window:

show warning

require deviation reason

This is common in clinical trials.

Difficulty:
⭐⭐

5️⃣ Deviation Model

Need something like

VisitDeviation

visit

reason

created_by

timestamp

Difficulty:
⭐⭐

6️⃣ Audit Trail ⭐⭐⭐

Currently not built.

Need model

AuditEvent

actor

action

entity_type

entity_id

before_json

after_json

timestamp

Then automatically log

participant created
participant edited
visit completed
form submitted
export started

Difficulty:
⭐⭐⭐⭐

This is probably the biggest missing clinical feature.

7️⃣ Export CSV

Need

Export Visits

Download CSV

Flatten

Participant

Visit

Status

Due Date

Actual Date

Forms

Difficulty:
⭐⭐

8️⃣ Export Jobs

Currently missing

Need

ExportJob

status

created_by

created_at

file_path

Later

Celery

Difficulty:
⭐⭐⭐

9️⃣ Forms Improvements

Currently

age

weight

notes

Need

Required fields

Dropdown

Checkbox

Date picker

Validation

Difficulty:
⭐⭐⭐

🔟 View Submitted Forms

Currently

Fill Form

Need

View Form

Edit Form

See answers

Difficulty:
⭐⭐

11️⃣ Edit Participant

Need

Edit Participant

Difficulty:
⭐

12️⃣ Edit Study

Need

Edit Study

Difficulty:
⭐

13️⃣ Delete Operations

Need

Delete

Study

Participant

Forms

Visit

Difficulty:
⭐

14️⃣ Authentication

Currently

Anyone can do everything.

Need

Login

Logout

Permissions

Coordinator

Data Manager

Admin

Difficulty:
⭐⭐⭐

15️⃣ Better Dashboard

Current

List only

Could add

Cards

Studies: 5

Participants: 48

Visits Today: 12

Overdue Visits: 3

Difficulty:
⭐⭐

16️⃣ Search

Participant search

Study search

Difficulty:
⭐

17️⃣ Pagination

Participant list

Visit list

Difficulty:
⭐

18️⃣ Filters

Visits by

Completed

Missed

Scheduled

Overdue

Difficulty:
⭐

19️⃣ REST API

Using Django REST Framework

Need endpoints

Studies

Participants

Visits

Forms

Difficulty:
⭐⭐⭐

20️⃣ Tests

Currently

No tests

Need

Models

Views

Scheduling

Forms

Difficulty:
⭐⭐⭐