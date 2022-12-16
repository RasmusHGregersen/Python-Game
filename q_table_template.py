import json

a_str=''
hit_bound_list=[]
for i in range(0,2):
    for j in range(0,2):
        for k in range(0,2):
            for m in range(0,2):
                a_str+= f"{i}{j}{k}{m}"
                hit_bound_list.append(a_str)
                a_str=""

                
widths = ['0','1','-']
heights = ['2','3','-']

states = {}
for i in widths:
    for j in heights:
        for k in hit_bound_list:
                states[str((i,j,k))] = [0,0,0,0]

with open("qtable.json", "w") as f:
    json.dump(states, f)