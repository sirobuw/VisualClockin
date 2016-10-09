# encoding: utf-8

from datetime import datetime, timezone, timedelta

file_in = open('targetcal.ics', mode='r', encoding='utf8')
file_out = open('parsed.txt', mode='w', encoding='utf8')

caldict = {}
datekey = ''

for line in file_in:
    if 'DTSTART' in line:
        utctime = datetime.strptime(line[8:].strip(), '%Y%m%dT%H%M%SZ')
        localtime = utctime.replace(tzinfo=timezone.utc).astimezone(None)
        datekey = localtime.strftime('%Y%m%d')

        if datekey in caldict:
            clockinoutlist = caldict.get(datekey)
            clockinoutlist.append(localtime)

        else:
            clockinoutlist = [localtime]

        caldict[datekey] = clockinoutlist

    elif 'SUMMARY' in line:
        clockinoutlist = caldict.get(datekey)
        clockinoutlist.append(line[8:].strip())
        caldict[datekey] = clockinoutlist

for key, value in sorted(caldict.items()):
    if value[1] == '下班':
        changeorder = [2, 3, 0, 1]
        value = [value[i] for i in changeorder]

    if value[2] < value[0]:
        value[2] += timedelta(days=1)

    value[0] = value[0].strftime('%Y/%m/%d %H:%M')
    value[2] = value[2].strftime('%Y/%m/%d %H:%M')

    line = key + ' ' + ', '.join(value) + '\n'
    file_out.write(line)

file_in.close()
file_out.close()
