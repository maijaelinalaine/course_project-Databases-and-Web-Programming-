# event_calendar

Event calendar website for a student association, inspired by University of Helsinki student associations' event calendars.

- Registered users are members of the association
- Users can:
  - register, log in and log out
  - add, edit and delete own events, choose a category for events (party, sits, appro, excursion, cruise, sports, meeting/hangout)
  - sign up for events and cancel sign ups
  - see information of all future events and list of signed up members
  - search events
- Website has a profile page, with future and past events that user has organized, potential payment information of events
- Events as primary data items and sign ups as secondary data items

Steps to run the app

- Install flask:
  $ pip install flask

- Create database:
  $ sqlite3 database.db < schema.sql

- Run
  $ flask run
