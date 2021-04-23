# this file is only intended for the initial cache
# after that the cache can be refreshed from the xkcd cog

import json
from urllib import request

latest = json.loads(request.urlopen("https://xkcd.com/info.0.json").read().decode())['num'] + 1
oldest = 1
_dict = {
    "titles": [],
    "alt_texts": [],
    "title_correspondences": {

    },
    "alt_correspondences": {

    }

}

for i in range(oldest, latest):
    if i == 404: continue
    data = json.loads(request.urlopen(f"https://xkcd.com/{i}/info.0.json").read().decode())
    print(f"{data['num']}: {data['safe_title']}")
    _dict['titles'].append(data['safe_title'].lower())
    _dict['alt_texts'].append(data['alt'].lower())
    _dict['title_correspondences'][data['safe_title'].lower()] = data['num']
    _dict['alt_correspondences'][data['alt'].lower()] = data['num']


with open("xkcd_cache.json", "w") as f:
    try:
        json.dump(_dict, f, indent=2)
    except:
        print(_dict)
    else:
        print(f"Dumpbed {_dict} \n (Dumped) ")
