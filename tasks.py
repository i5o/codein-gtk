import json

f = open("tasks.json", "r")
tasks = json.load(f)['results']
f.close()

for task in tasks:
    print json.dumps(task, indent=4)
    break
