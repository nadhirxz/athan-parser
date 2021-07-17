import os
import json
import re

places = ['alger', 'adrar', 'djelfa']

p = {
    'alger': ['Oran', 'Mostaganem', 'Relizane', 'Chlef', 'Ain Defla', 'Tipaza', 'Medea', 'Blida', 'Boumerdes', 'Bouira', 'Dellys', 'Tizi Ouzou', 'Msila', 'Bordj Bou Arreridj', 'Setif', 'Jijel', 'Mila', 'Constantine', 'Skikda', 'Oum El Bouaghi', 'Guelma', 'Annaba', 'Souk Ahras', 'El Taref'],
    'adrar': ['Beni Ounif', 'Tindouf', 'Bechar', 'Timimoun', 'Reggane', 'Bordj Badji Mokhtar', 'Beni Abbes', 'In Salah', 'El Menia', 'Ghardaia', 'Ouargla', 'Tamanrasset', 'In Guezzam', 'Illizi', 'Djanet', 'In Amenas'],
    'djelfa': ['Maghnia', 'Sebdou', 'Ain Temouchent', 'Tlemcen', 'Ben Badis', 'Naama', 'Mascara', 'Saida', 'El Bayadh', 'Tiaret', 'Tissemsilt', 'Ain Oussera', 'Laghouat', 'Hassi R\'Mel', 'Ain El Melh', 'Bou Saada', 'Biskra', 'Touggourt', 'Batna', 'El Oued', 'Khenchela', 'Bir El Ater', 'Tebessa']
}

out = {}

for dir in os.listdir('./output'):
	if (re.match(r'\d{4}', dir)):
		out[dir] = {}
		for place in places:
			timing = f'./output/{dir}/{place}/timing'
			offset = f'./output/{dir}/{place}/offset'
			out[dir][place] = {'timing': {}, 'places': p[place], 'offset': []}

			for file_name in os.listdir(timing):
				file = open(os.path.join(timing, file_name), 'r').read()
				lines = [l.strip() for l in file.split('\n')]
				for line in lines:
					line = line.split('|')
					out[dir][place]['timing'][line[-1]] = line[:-1][::-1]

			for file_name in os.listdir(offset):
				file = open(os.path.join(offset, file_name), 'r').read()
				if (place == 'adrar'):
					out[dir][place]['offset'].append({'first': [], 'second': []})
					parts = file.split('\n\n')
					for i, part in enumerate(parts):
						a = 'first' if i % 2 == 0 else 'second'
						part = part.split('\n')
						for line in part:
							out[dir][place]['offset'][int(file_name.split('.')[0]) - 1][a].append(line.split('|'))
				else:
					out[dir][place]['offset'].append([])
					lines = [l.strip() for l in file.split('\n')]
					for line in lines:
						out[dir][place]['offset'][int(file_name.split('.')[0]) - 1].append(line.split('|'))

def stringify(out):
	output = json.dumps(out, indent=4)
	output = output.replace('    ', '	')
	output = re.sub(r'\[\n\s+"', '["', output)
	output = re.sub(r'",\s+', '", ', output)
	return re.sub(r'"\s+\]', '"]', output)

open('./output/output.json', 'w').write(stringify(out))

for dir in os.listdir('./output'):
	if (re.match(r'\d{4}', dir)):
			open(f'./output/{dir}/{dir}.json', 'w').write(stringify(out[dir]))
			for place in places:
				open(f'./output/{dir}/{place}/{place}.json', 'w').write(stringify(out[dir][place]))