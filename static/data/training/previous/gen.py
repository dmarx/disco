# https://harishgarg.com/writing/how-to-fine-tune-gpt-3-api/


import json
from types import SimpleNamespace

from nbformat import write


data = json.load(open("static/data/training/tags.json"))

out = []

for k in data.keys():
    artist = k
    tags = data[k]["tags"].split(",")
    for j in range(len(tags)):
        pair = {"prompt": tags[j], "completion": "by " + k}
        out.append(pair)


jsonStr = json.dumps(out)  # .__dict__, default=lambda obj: obj.__dict__)
with open("static/data/training/out.json", "w") as outfile:
    outfile.write(jsonStr)


# {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
# {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
