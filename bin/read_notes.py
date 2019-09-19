#! /usr/bin/python3

import re
import time
from datetime import datetime

# <note id="4" lat="36.7232991" lon="68.8641500" created_at="2013-04-24T08:07:02Z" closed_at="2016-08-07T14:51:37Z">
class Note():
    counter = 0
    closed = 0

    open_buckets = dict()
    closed_buckets = dict()

    def __init__(self):
        Note.counter += 1
        self.id = ""
        self.lat = ""
        self.lon = ""
        self.created_at = ""
        self.closed_at = ""

    def __str__(self):
        return '{},{},{},{},{},{},{}'.format(self.id, self.lat, self.lon, self.created_at, self.closed_at, self.days_to_close, self.open_for)

    def __del__(self):
        try:
            yyyymm = self._date_to_year_month(self.created_at)
            Note.open_buckets[yyyymm] += 1
        except:
            Note.open_buckets[yyyymm] = 1


        if self.isclosed:
            Note.closed += 1
            try:
                yyyymm = self._date_to_year_month(self.closed_at)
                Note.closed_buckets[yyyymm] += 1
            except:
                Note.closed_buckets[yyyymm] = 1

    def _date_to_year_month(self, string):
        match = re.match(r"^(\d+-\d\d)-\d\dT.*", string)
        if match:
            return match.group(1)

    def _to_date(self, string):
        # 2019-09-12T00:36:24Z
        #return int(time.mktime(time.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ")))
        return datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ")

    @property
    def days_to_close(self):
        if self.isclosed:
            delta = self._to_date(self.closed_at) - self._to_date(self.created_at)
            return delta.days
        else:
            return ""

    @property
    def open_for(self):
        if not self.isclosed:
            delta = self._to_date("2019-09-12T00:54:34Z") - self._to_date(self.created_at) 
            return delta.days
        else:
            return ""

    @property
    def isclosed(self):
        if len(self.closed_at) == 0:
            return False
        return True


# We will output as id,lat,lon,created,closed,age
regex = r"(([a-zA-Z_]+)=\"([^\"]*)\")"

#fh = open("./planet-notes-190424.sample", "r")

fh = open("./planet-notes-latest.osn", "r")
for line in fh:
    if line.find("<note id=", 0, 9) != -1:

        note_dict = dict()
        note = Note()

        # Extract data:
        matches = re.finditer(regex, line)

        for matchNum, match in enumerate(matches, start=1):
            setattr(note, match.group(2), match.group(3))
        
        if not note.isclosed:
            print(note)


#print(Note.counter)
#print(Note.closed)

note_dates = []
opened = []
closed = []

for yymm in Note.open_buckets.keys():
    note_dates.append(yymm)
    opened.append(str(Note.open_buckets[yymm]))
    closed.append(str(Note.closed_buckets[yymm]))

#print(opened)
#print(closed)
#print(",".join(note_dates))
#print(",".join(opened))
#print(",".join(closed))

