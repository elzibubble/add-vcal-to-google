#!/usr/bin/python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import argparse
import httplib2
import icalendar
import os.path
import sys

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import tools


def read_ical_event(f):
    content = f.read()
    # Thanks, https://github.com/dmedvinsky/mutt-ics
    ics_text = content.replace("\nDTSTART:1601", "\nDTSTART:1901")

    cal = icalendar.Calendar.from_ical(ics_text)
    ev = [x for x in cal.subcomponents if x.name == 'VEVENT'][0]
    attendees = ev['ATTENDEE']
    if not isinstance(attendees, list):
        ev['ATTENDEE'] = [attendees]
    return ev


def get_creds():
    flow = OAuth2WebServerFlow(
        "23276227116-vq4tg8dd781j9ij9lm6p2asnr2urvc8h"
        ".apps.googleusercontent.com",
        "jCEWeCP8nvGmXnr8LjGlk1MH",
        'https://www.googleapis.com/auth/calendar',
        redirect_uri='http://localhost:8080/')
    storage = Storage(os.path.expanduser('~/.add-vcal.dat'))

    creds = storage.get()
    if creds is None or creds.invalid:
        creds = tools.run_flow(flow, storage, flags)
    return creds


def get_calendar(creds):
    http = httplib2.Http()
    http = creds.authorize(http)
    return build('calendar', 'v3', http=http)


def datefmt(d):
    return d.isoformat("T") + "Z"  # FIXME


def add_event(service, event):
    return service.events().insert(calendarId='primary', body=event).execute()


iev = read_ical_event(sys.stdin)
request = {
    'summary': iev['SUMMARY'],
    'location': iev['LOCATION'],
    'start': {'dateTime': datefmt(iev['DTSTART'].dt)},
    'end': {'dateTime': datefmt(iev['DTEND'].dt)},
    'attendees': [{'displayName': a.params['CN'],
                   'email': a.replace('MAILTO:', '')}
                  for a in iev['ATTENDEE']],
}

# import json
# print(json.dumps(request))
# raise SystemExit

parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()
creds = get_creds()
service = get_calendar(creds)
gev = add_event(service, request)

# print(gev['id'])
