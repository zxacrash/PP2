from datetime import datetime, timedelta
import re
import math

def parse(line):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2}) UTC([+-])(\d{2}):(\d{2})', line)
    y, mo, d, s, hh, mm = m.groups()
    dt = datetime(int(y), int(mo), int(d))
    offset = timedelta(hours=int(hh), minutes=int(mm))
    if s == '+':
        utc = dt - offset
        tz = offset
    else:
        utc = dt + offset
        tz = -offset
    return dt, utc, tz

# Input processing
line1 = input().strip()
line2 = input().strip()

birth_local, _, birth_tz = parse(line1)
_, current_utc, _ = parse(line2)

bmo, bd = birth_local.month, birth_local.day

def is_leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

def make_bday(y):
    d = bd
    if bmo == 2 and bd == 29 and not is_leap(y):
        d = 28
    # Midnight on birthday in local time converted to UTC
    local = datetime(y, bmo, d)
    return local - birth_tz

cy = current_utc.year

# Find first birthday UTC >= current_utc
for y in [cy, cy+1]:
    b_utc = make_bday(y)
    if b_utc >= current_utc:
        diff_seconds = (b_utc - current_utc).total_seconds()
        # Use ceiling of full days
        diff_days = math.ceil(diff_seconds / 86400)
        print(diff_days)
        break