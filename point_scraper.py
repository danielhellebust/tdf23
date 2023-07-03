import time
import requests
import bs4
import pandas as pd


with open('./riders.txt', 'r') as f:
    rider_list = f.read().splitlines()

df_list = []
#rider_list = rider_list[0:2]


for i in rider_list:
    print(i)
    pointList = ['/results/career-points-time-trial', '/results/career-points-sprint',
                 '/results/career-points-climbers']
    rider_name = i.split('/')[-1]
    for j in pointList:
        try:
            point_type = j[23:]
            rider_url = i + j
            req = requests.get(rider_url)
            soup = bs4.BeautifulSoup(req.text, "html.parser")
            table = soup.find('table', {'class': 'basic'})
            rider = soup.find('div', {'class': 'main'}).text
            riderName = rider.split('»')[0].strip()
            riderTeam = rider.split('»')[1].strip()

            df = pd.read_html(str(table))[0]
            df['rider'] = riderName
            df['team'] = riderTeam
            df['point_type'] = point_type
            df_list.append(df)

            time.sleep(2)
        except:
            pass


df = pd.concat(df_list)

print(df)
df.to_csv('./rider_points.csv', index=False)







