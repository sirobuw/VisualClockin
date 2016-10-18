# encoding: utf-8

from datetime import datetime, timezone, timedelta

file_in = open('targetcal.ics', mode='r', encoding='utf8')
file_out = open('seperate.csv', mode='w', encoding='utf8')

columnname = '"日期","上班","全部下班","週一到週四下班","週五下班"' + '\n'
file_out.write(columnname)

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
    if value[1] == '加班':
        continue

    if value[1] == '下班':
        changeorder = [2, 3, 0, 1]
        value = [value[i] for i in changeorder]

    if value[2] < value[0]:
        value[2] += timedelta(days=1)
        clockout = value[2].strftime('%H%M')
        clockout = int(clockout) + 2400
    else:
        clockout = value[2].strftime('%H%M')

    if value[2].isoweekday() in range(1,5):
        monthu = clockout
        fri = ''

    if value[2].isoweekday() == 5:
        monthu = ''
        fri = clockout

    # value[0] = value[0].strftime('%Y/%m/%d %H:%M')
    # value[2] = value[2].strftime('%Y/%m/%d %H:%M')
    clockin = value[0].strftime('%H%M')
    # value[2] = value[2].strftime('%H%M')

    # line = key + ' ' + ', '.join(value) + '\n'
    line = '"' + key + '","' + clockin + '","' + str(clockout) + '","' + str(monthu) + '","' + str(fri) + '"\n'
    file_out.write(line)

file_in.close()
file_out.close()
