import math
import numpy
import json
import sys
from termcolor import colored

mult_dict = { 0.094: 1.0,0.135137432: 1.5,0.16639787: 2.0,0.192650919: 2.5,0.21573247: 3.0,0.236572661: 3.5,0.25572005: 4.0,0.273530381: 4.5,0.29024988: 5.0,0.306057377: 5.5,0.3210876: 6.0,0.335445036: 6.5,0.34921268: 7.0,0.362457751: 7.5,0.37523559: 8.0,0.387592406: 8.5,0.39956728: 9.0,0.411193551: 9.5,0.42250001: 10.0,0.432926419: 10.5,0.44310755: 11.0,0.4530599578: 11.5,0.46279839: 12.0,0.472336083: 12.5,0.48168495: 13.0,0.4908558: 13.5,0.49985844: 14.0,0.508701765: 14.5,0.51739395: 15.0,0.525942511: 15.5,0.53435433: 16.0,0.542635767: 16.5,0.55079269: 17.0,0.558830576: 17.5,0.56675452: 18.0,0.574569153: 18.5,0.58227891: 19.0,0.589887917: 19.5,0.59740001: 20.0,0.604818814: 20.5,0.61215729: 21.0,0.619399365: 21.5,0.62656713: 22.0,0.633644533: 22.5,0.64065295: 23.0,0.647576426: 23.5,0.65443563: 24.0,0.661214806: 24.5,0.667934: 25.0,0.674577537: 25.5,0.68116492: 26.0,0.687680648: 26.5,0.69414365: 27.0,0.700538673: 27.5,0.70688421: 28.0,0.713164996: 28.5,0.71939909: 29.0,0.725571552: 29.5,0.7317: 30.0,0.734741009: 30.5,0.73776948: 31.0,0.740785574: 31.5,0.74378943: 32.0,0.746781211: 32.5,0.74976104: 33.0,0.752729087: 33.5,0.75568551: 34.0,0.758630378: 34.5,0.76156384: 35.0,0.764486065: 35.5,0.76739717: 36.0,0.770297266: 36.5,0.7731865: 37.0,0.776064962: 37.5,0.77893275: 38.0,0.781790055: 38.5,0.78463697: 39.0,0.787473578: 39.5,0.79030001: 40.0,0.79030001: 40 }
d = sorted(mult_dict.iteritems())

output = {}
limit = 1

mon = str(sys.argv[1]).title()
my_atk = int(sys.argv[2])
my_def = int(sys.argv[3])
my_sta = int(sys.argv[4])

if len(sys.argv) > 5:
    max_print = int(sys.argv[5])
else:
	max_print = 0

batk = 0
run = [mon]
evo_table = {}
pokemon_data = {}

with open('pogo-mon-data.json') as json_file:  
    data = json.load(json_file)
    for p in data:
    	pokemon_data[str(p['name']).title()] = {'atk': int(p['atk']), 'def': int(p['def']), 'sta': int(p['sta'])}
    	evo_table[str(p['name']).title()] = []
    	for evo in p['evolutions']:
    		evo_table[str(p['name']).title()].append(evo)

if not mon in pokemon_data.keys():
	print("Sorry, cannot find '"+mon+"', did you misspell it?")
	exit()

for mon in run:
	if mon in evo_table.keys():
		if len(evo_table[mon]) > 0:
			for evo in evo_table[mon]:
				if evo not in run:
					run.append(evo)
	else:
		run.remove(mon)

if len(run) > 0:
	for mon in run:
		if not mon in pokemon_data.keys():
			continue
		batk = pokemon_data[mon]['atk']
		bdef = pokemon_data[mon]['def']
		bsta = pokemon_data[mon]['sta']
		max_cp = max(10,int( 0.6245741058 * (batk+15) * math.sqrt((bdef+15)*(bsta+15))/10))
		if max_cp < 1100:
			continue
		gl_out = { }
		processing = []
		for atkiv in range(16):
			for defiv in range(16):
				for staiv in range(16):
					glvl = 0
					gl_mult = 0.094
					gl_mult = math.sqrt( (15010.0/(batk+atkiv)/ math.sqrt((bdef+defiv)*(bsta+staiv)) ) )
					for mult, lvl in d:
						if (mult > gl_mult ):
							break
						glvl = lvl
						gmult = mult
					ghp = max(10,int(gmult*(staiv + bsta)))
					gl_comb = float(gmult * (atkiv + batk))
					sp = float((gmult ** 2) * (atkiv + batk) * (defiv + bdef) * ghp)
					processing.append({ "atkval": gl_comb, "sp": sp, "atkv": atkiv, "defv": defiv, "stav": staiv, "lvl": glvl})
		s = sorted(processing, key = lambda x: (x['atkval'], x['sp']), reverse=True)
		for item in s:
			dupe = False
			gl_comb = item['atkval'] * 10000000
			gl_comb = gl_comb + item['sp']
			if gl_comb in gl_out.keys():
				dupe = True
			while gl_comb in gl_out.keys():
				gl_comb = numpy.nextafter(gl_comb, 1)
			gl_out[gl_comb] = { "atkv": item['atkv'], "defv": item['defv'], "stav": item['stav'], "lvl": item['lvl'], "dupe": dupe, "tatk": item['atkval']}
		out = sorted(gl_out.items(), reverse=True)
		i = 0
		for sp, data in out:
			if max_print > 0 and i <= max_print:
				print(colored(mon+' | Rank: '+str(i+1)+' | Level: '+str(data['lvl'])+' | Stats: '+str(data['atkv'])+' '+str(data['defv'])+' '+str(data['stav'])+' | Attack: '+str(data['tatk'])+' | Stat Product: '+str(sp), 'cyan'))
			if data['dupe'] != True:
				i += 1
			color = 'green'
			if i >= 100:
				color = 'yellow'
			if i >= 500:
				color = 'red'
			if int(my_atk) == data['atkv'] and int(my_def) == data['defv'] and int(my_sta) == data['stav']:
				mcp = ' | Max CP: '+str(max_cp) if max_cp < 1500 else ''
				print(colored(mon+' | Rank: '+str(i)+' | Level: '+str(data['lvl'])+' | Attack: '+str(data['tatk'])+' | Stat Product: '+str(sp)+mcp, color))
