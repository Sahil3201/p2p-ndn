# Put output on https://dreampuf.github.io/GraphvizOnline/ 
import json, os

print('digraph G {')
with open("interfaces.json", 'r') as load_f:
    load_dict = json.load(load_f)

for i in load_dict:        
    name = list(i.keys())[0]
    if len(name.split('/'))!=3: continue
    # else: print(name)
    for j in i[name][1]['neighbors']:
        ret = ''.join((name.replace('/','_'), '->', j.replace('/','_')))
        print(ret.replace('soil','s').replace('crop','c'))

print('}')
