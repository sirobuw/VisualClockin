# encoding: utf-8

file_in = open('target.ics', mode='r', encoding='utf8')
file_out = open('parsed.txt', mode='w', encoding='utf8')

for line in file_in:
    if 'DTSTART' in line:
        file_out.write(line[8:])
    elif 'SUMMARY' in line:
        file_out.write(line[8:])

file_in.close()
file_out.close()
