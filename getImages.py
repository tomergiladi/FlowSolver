import requests
import os
base = 'https://flowfreesolutions.com/solution-pictures/flow/'
pack = 'regular'
try :
    os.mkdir(f"data/{pack}")
except:
    pass
for i in range(1, 30):
    img_url = f'{base}/{pack}/flow-regular-{i}.png'
    response = requests.get(img_url)
    if response.status_code:
        fp = open(f'data/{pack}/{i}.png', 'wb')
        fp.write(response.content)
        fp.close()