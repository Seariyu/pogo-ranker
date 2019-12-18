import math
import numpy
import json
import sys

mult_dict = { 0.094: 1.0,0.135137432: 1.5,0.16639787: 2.0,0.192650919: 2.5,0.21573247: 3.0,0.236572661: 3.5,0.25572005: 4.0,0.273530381: 4.5,0.29024988: 5.0,0.306057377: 5.5,0.3210876: 6.0,0.335445036: 6.5,0.34921268: 7.0,0.362457751: 7.5,0.37523559: 8.0,0.387592406: 8.5,0.39956728: 9.0,0.411193551: 9.5,0.42250001: 10.0,0.432926419: 10.5,0.44310755: 11.0,0.4530599578: 11.5,0.46279839: 12.0,0.472336083: 12.5,0.48168495: 13.0,0.4908558: 13.5,0.49985844: 14.0,0.508701765: 14.5,0.51739395: 15.0,0.525942511: 15.5,0.53435433: 16.0,0.542635767: 16.5,0.55079269: 17.0,0.558830576: 17.5,0.56675452: 18.0,0.574569153: 18.5,0.58227891: 19.0,0.589887917: 19.5,0.59740001: 20.0,0.604818814: 20.5,0.61215729: 21.0,0.619399365: 21.5,0.62656713: 22.0,0.633644533: 22.5,0.64065295: 23.0,0.647576426: 23.5,0.65443563: 24.0,0.661214806: 24.5,0.667934: 25.0,0.674577537: 25.5,0.68116492: 26.0,0.687680648: 26.5,0.69414365: 27.0,0.700538673: 27.5,0.70688421: 28.0,0.713164996: 28.5,0.71939909: 29.0,0.725571552: 29.5,0.7317: 30.0,0.734741009: 30.5,0.73776948: 31.0,0.740785574: 31.5,0.74378943: 32.0,0.746781211: 32.5,0.74976104: 33.0,0.752729087: 33.5,0.75568551: 34.0,0.758630378: 34.5,0.76156384: 35.0,0.764486065: 35.5,0.76739717: 36.0,0.770297266: 36.5,0.7731865: 37.0,0.776064962: 37.5,0.77893275: 38.0,0.781790055: 38.5,0.78463697: 39.0,0.787473578: 39.5,0.79030001: 40.0,0.79030001: 40 }
d = sorted(mult_dict.iteritems())

cup = [ "Abomasnow", "Aggron", "Altaria", "Amoonguss", "Bibarel", "Blaziken", "Breloom", "Bronzong", "Charizard", "Claydol", "Cloyster", "Cradily", "Durant", "Empoleon", "Excadrill", "Exeggutor", "Exeggutor (Alolan)", "Farfetchd", "Froslass", "Gastrodon (East Sea)", "Gastrodon (West Sea)", "Gloom", "Golbat", "Golem", "Graveler", "Gyarados", "Haunter", "Heracross", "Honchkrow", "Houndoom", "Infernape", "Ivysaur", "Kingdra", "Lairon", "Lanturn", "Ludicolo", "Lunatone", "Magcargo", "Magneton", "Magnezone", "Mamoswine", "Marowak (Alolan)", "Marshtomp", "Monferno", "Muk (Alolan)", "Nidoqueen", "Ninetales (Alolan)", "Noctowl", "Pidgeot", "Piloswine", "Poliwrath", "Probopass", "Quagsire", "Raticate (Alolan)", "Roselia", "Roserade", "Sandshrew (Alolan)", "Sealeo", "Shiftry", "Skuntank", "Slowbro", "Slowking", "Sneasel", "Staraptor", "Swampert", "Swellow", "Togekiss", "Torterra", "Toxicroak", "Venomoth", "Venusaur", "Victreebel", "Vileplume", "Weavile", "Weepinbell", "Whiscash", "Wigglytuff", "Yanma" ]

output = {}

whitelist_g = [202]

min_cp_g = 1220
lim = 1000

mon = str(sys.argv[1]).title()

batk = 0
run = [mon]
evo_table = {}
pokemon_data = {}
processing = []
unsorted_output = []
output_data = ""
max_iatk = 0.0
min_iatk = 10000000000.0
my_avg = 0.0

with open('pogo-mon-data.json') as json_file:  
    data = json.load(json_file)
    for p in data:
    	if str(p['name']).title() == mon:
	    	batk = int(p['atk'])
	    	bdef = int(p['def'])
	    	bsta = int(p['sta'])
	    	num = int(p['id'])
	    	my_max_atk = 0.0
	    	my_min_atk = 10000000000.0
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
	    				atkval = float(gmult * (atkiv + batk))
	    				sp = float((gmult ** 2) * (atkiv + batk) * (defiv + bdef) * ghp)
	    				processing.append({ "atkval": atkval, "sp": sp, "atkv": atkiv, "defv": defiv, "stav": staiv, "lvl": glvl})
	    	s = sorted(processing, key = lambda x: (x['sp'], x['atkval']), reverse=True)
	    	i = 0
	    	for data in s:
	    		i += 1
	    		if i >= lim:
	    			break
	    		if i <= 100:
	    			max_iatk = data['atkval'] if data['atkval'] > max_iatk else max_iatk
	    			min_iatk = data['atkval'] if data['atkval'] < min_iatk else min_iatk
	    			my_avg += data['atkval']
	    		my_max_atk = data['atkval'] if data['atkval'] > my_max_atk else my_max_atk
	    		my_min_atk = data['atkval'] if data['atkval'] < my_min_atk else my_min_atk
	    	output_data += "['"+p['name']+"', "+str(my_min_atk)+", "+str(min_iatk)+", "+str(max_iatk)+", "+str(my_max_atk)+"],\n"
	    	my_avg = my_avg / 100.0

with open('pogo-mon-data.json') as json_file:  
    data = json.load(json_file)
    for p in data:
    	if p['name'] not in cup or str(p['name']).title() == mon:
    		continue
    	batk = int(p['atk'])
    	bdef = int(p['def'])
    	bsta = int(p['sta'])
    	num = int(p['id'])
    	evos = p['evolutions']

    	max_cp = max(10,int( 0.6245741058 * (batk+15) * math.sqrt((bdef+15)*(bsta+15))/10))
    	if max_cp < min_cp_g and not int(num) in whitelist_g:
    		continue

    	gl_out = { }
    	max_atk = 0.0
    	min_atk = 10000000000.0
    	max_iatk = 0.0
    	min_iatk = 10000000000.0

    	aw_processing = []
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
					atkval = float(gmult * (atkiv + batk))
					mon_sp = float((gmult ** 2) * (atkiv + batk) * (defiv + bdef) * ghp)
					gl_comb = mon_sp + atkval
					dupe = False

					while gl_comb in gl_out.keys():
						gl_comb = numpy.nextafter(gl_comb, 1)
						dupe = True
					gl_out[gl_comb] = { "atkv": atkiv, "defv": defiv, "stav": staiv, "lvl": glvl, "atkval": atkval, "sp": mon_sp, "dupe": dupe }
    	out = sorted(gl_out.items(), reverse=True)
    	i = 0
    	mean = 0.0
    	for sp, data in out:
    		if i >= lim:
    			break
    		i += 1
    		max_atk = data['atkval'] if data['atkval'] > max_atk else max_atk
    		min_atk = data['atkval'] if data['atkval'] < min_atk else min_atk
    		if i <= 100:
    			max_iatk = data['atkval'] if data['atkval'] > max_iatk else max_iatk
    			min_iatk = data['atkval'] if data['atkval'] < min_iatk else min_iatk
    			mean += data['atkval']
    	if ( min_atk >= my_min_atk and min_atk <= my_max_atk ) or ( max_atk <= my_max_atk and max_atk >= my_min_atk ):
    		mean = mean / 100.0
    		unsorted_output.append({ "name": p['name'], "1": str(min_atk), "2": str(min_iatk), "3": str(max_iatk), "4": str(max_atk), "diff": abs(mean - my_avg) })
s = sorted(unsorted_output, key = lambda x: (x['diff']), reverse=False)
for p in s:
	output_data += "['"+p['name']+"', "+p['1']+", "+p['2']+", "+p['3']+", "+p['4']+"],\n"


output ="""<html>
  <head>
    <script type=\"text/javascript\" src=\"https://www.gstatic.com/charts/loader.js\"></script>
    <script type=\"text/javascript\">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable([
      """+output_data+"""
    ], true);

    var options = {
      legend:'none'
    };

    var chart = new google.visualization.CandlestickChart(document.getElementById('chart_div'));

    chart.draw(data, options);
  }
    </script>
  </head>
  <body>
    <div id=\"chart_div\" style=\"width: 3000px; height: 1080px;\"></div>
  </body>
</html>"""

outF = open(mon+'.html', 'w')
outF.write(output)
