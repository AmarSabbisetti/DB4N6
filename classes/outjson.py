import json
def output_json(data):
    for i in data:
        print(i)
        for k,v in data[i].items():
            print(k,v)