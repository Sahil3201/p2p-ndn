import graphviz, json

with open("interfaces.json", 'r') as load_f:
    load_dict = json.load(load_f)

# Crops device
crops_sensors = ["humidity", "oxygen", "ethylene", "carbonDioxide", "temperature", "moisture", "rainGauge", "camera"]
dot = graphviz.Digraph(comment='Crops Device Graph', format='png')
for i in crops_sensors:
    dot.node('crop_'+i, i)
dot.node('crops')
for i in crops_sensors:
    dot.edge('crops', f'crop_{i}')
dot2 = dot.unflatten(stagger=3)
dot2.render('network architecture/Crops Device Graph')  

# Soils device
soils_sensors = ["moisture", "erosion", "salinity", "winds", "organicMatter", "temperature", "pH", "alert"]
dot = graphviz.Digraph(comment='Soils Device Graph', format='png')
for i in soils_sensors:
    dot.node('soil_'+i, i)
dot.node('soils')
for i in soils_sensors:
    dot.edge('soils', f'soil_{i}')
dot2 = dot.unflatten(stagger=3)
dot2.render('network architecture/Soils Device Graph')  

# Network graph
dot = graphviz.Digraph(comment='Network Graph', format='png')
for i in load_dict:        
    name = list(i.keys())[0]
    if len(name.split('/'))!=3: continue
    for j in i[name][1]['neighbors']:
        dot.edge(name[-5:], j[-5:])
dot2 = dot.unflatten(stagger=3)
dot2.render('network architecture/Network Graph')
