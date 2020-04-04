import requests 
from bs4 import BeautifulSoup
import random
import string
import csv
import sys

# command line arguments must include a url, input filename, and output filename
if len(sys.argv) != 4:
    sys.exit('Please include 3 parameters: <url> <input filename> <output filename>')

url = sys.argv[1]
in_file = sys.argv[2]
out_file = sys.argv[3]

# create data array with headers
data = []
headers = ['sprayX', 'sprayY', 'in_play_result', 'batter']
data.append(headers)

player_id = {}

results = {'grounded out': 'GB', 'lined out': 'LD', 'flied out': 'FB', 'popped up': 'FB', 'fouled out': 'FB'}

# {<position>: [<x min>, <x max>, <y min>, <y max>]}
positions = {'1b': [.6, .68, .58, .75], '2b': [.5, .6, .5, .6], '3b': [.32, .4, .58, .75], 'ss': [.4, .5, .5, .6], 
'rf': [.6, .85, .15, .375], 'lf': [.15, .4, .15, .375], 'cf': [.4, .6, .1, .375]}

# capture player Ids
with open(in_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # id, first_name, last_name
    for row in csv_reader:
        player_id[row[2].lower()] = row[0]
        player_id[row[1].lower()[:1] + ' ' + row[2].lower()] = row[0]

# open website and create BeautifulSoup object
r = requests.get(url)
c = r.content
soup = BeautifulSoup(c,"html.parser")

games = soup.find_all('a', text='Box Score', href=True)

count = 1
dupUrl = []
for g in games:
    u = url[:url.index('.com')+5] + g['href']
    if u in dupUrl:
        continue
    dupUrl.append(u)

    count += 1
    r = requests.get(url[:url.index('.com')+4] + g['href'])
    c = r.content
    soup = BeautifulSoup(c,"html.parser")

    div = soup.find('div', {'id': 'inning-all'})
    # find all of the tables
    for table in div.find_all('table', {'class': 'sidearm-table play-by-play'}):
        body = table.find('tbody')
        # find all of the rows
        for row in body.find_all('tr'): 
            th = row.find('th')
            if th:
                f_initial = ''
                rest = ''

                text = th.text.lower()
                p_split = text.split('.')
                if len(p_split) < 2:
                    continue
                if len(p_split[0]) < 2:
                    f_initial = p_split[0]
                    rest = p_split[1]
                else:
                    rest = p_split[0]
                s_split = rest.split()
                if len(s_split) == 0:
                    continue
                last_name = s_split.pop(0)
                result = ' '.join([str(elem) for elem in s_split])

                # use a first initial if there is one
                name = f_initial + ' ' + last_name if f_initial else last_name
                if name in player_id:
                    ip_type = ''
                    x = ''
                    y = ''
                    for i in range(len(s_split)):
                        st = s_split[i].translate(str.maketrans('', '', string.punctuation))
                        st2 = ''
                        if i+1 < len(s_split):
                            st2 = s_split[i+1].translate(str.maketrans('', '', string.punctuation))

                        # determine what the in play type is
                        if st in results:
                            ip_type = results[st]
                        elif st + ' ' + st2 in results:
                            ip_type = results[st + ' ' + st2]

                        # determine the x and y coordinates
                        if st in positions:
                            box = positions[st]
                            x = round(random.uniform(box[0], box[1]), 6)
                            y = round(random.uniform(box[2], box[3]), 6)

                    if x and y:
                        data.append([x, y, ip_type, player_id[last_name]])
                        if not ip_type:
                            print(result)





# write data to the csv
f = open(out_file + '.csv', 'w')

with f:
    writer = csv.writer(f)
    writer.writerows(data)

print('Complete')


