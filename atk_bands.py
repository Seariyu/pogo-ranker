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
    print_all = int(sys.argv[5])
else:
	print_all = 0

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
		spr_out = { }
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
			gl_out[gl_comb] = { "atkv": item['atkv'], "defv": item['defv'], "stav": item['stav'], "sp": item['sp'], "lvl": item['lvl'], "dupe": dupe, "tatk": item['atkval']}
			dupe = False
			gl_comb = item['sp']
			if gl_comb in gl_out.keys():
				dupe = True
			while gl_comb in gl_out.keys():
				gl_comb = numpy.nextafter(gl_comb, 1)
			spr_out[gl_comb] = { "atkv": item['atkv'], "defv": item['defv'], "stav": item['stav'], "sp": item['sp'], "lvl": item['lvl'], "dupe": dupe, "tatk": item['atkval']}
		spr_srt = sorted(spr_out.items(), reverse=True)
		out = sorted(gl_out.items(), reverse=False)
		i = 0
		j = 0
		k = 0
		pj = 31
		ratk = 0.0
		msp = 0.0
		best = ''
		trough = False
		bivs = ''
		bsp = 0.0
		bspa = 0.0
		bbsp = 0.0
		bbspa = 0.0
		asum = 0.0
		spsum = 0.0
		for idx, data in out:
			k += 1
			asum += data['tatk']
			spsum += data['sp']
			atkst = data['tatk']
			if data['sp'] > bbsp:
				bbsp = data['sp']
				bbspa = data['tatk']
				bblvl = data['lvl']
				bbstats = 'Stats: '+str(data['atkv'])+' '+str(data['defv'])+' '+str(data['stav'])
				bband = i
			if ratk != atkst:
				i += 1
				trough = True if i > 5 and j < 25 and pj < 25 and k > 50 else False
				color = 'green' if trough else 'yellow'
				pj = j
				if print_all != 0 and ratk > 0:
					print(colored(mon+' | Band: '+str(i)+' | Attack: '+str(data['tatk'])+' | Count: '+str(j)+' | Max Stat Product: '+str(msp)+best, color))
				j = 0
				ratk = atkst
				msp = data['sp']
				best = ' | Level: '+str(data['lvl'])+' | Stats: '+str(data['atkv'])+' '+str(data['defv'])+' '+str(data['stav'])
				if trough:
					if bbsp > bsp:
						bsp = bbsp
						bspa = bbspa
						rlu = bbstats
						bivs = colored(mon+' | Band: '+str(i)+' | Attack: '+str(data['tatk'])+' | Stat Product: '+str(bbsp)+' | Level: '+str(bblvl)+' | '+bbstats, 'white')
				bbsp = 0.0
				bbspa = 0.0
			if data['sp'] > msp:
				msp = data['sp']
				best = ' | Level: '+str(data['lvl'])+' | Stats: '+str(data['atkv'])+' '+str(data['defv'])+' '+str(data['stav'])
			j += 1
			if int(my_atk) == data['atkv'] and int(my_def) == data['defv'] and int(my_sta) == data['stav']:
				mcp = ' | Max CP: '+str(max_cp) if max_cp < 1500 else ''
				print(colored(mon+' | Band: '+str(bband)+' | Attack: '+str(data['tatk'])+' | Stat Product: '+str(data['sp'])+mcp, 'cyan'))
		print('Total Bands: '+str(i))
		l = 0
		for sp, rdata in spr_srt:
			l += 1
			if rlu == 'Stats: '+str(rdata['atkv'])+' '+str(rdata['defv'])+' '+str(rdata['stav']):
				rank = l
				break
		print(bivs+colored(' | SP Rank : '+str(rank), 'white'))
		avg_atk = asum / k
		avg_sp = spsum / k
		print(colored('Average Attack: '+str(avg_atk)+' | Average Stat Product: '+str(avg_sp), 'cyan'))
