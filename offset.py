import re
from pathlib import Path
from tqdm import tqdm
import os

print('\nParsing Offset')

places = ['alger', 'adrar', 'djelfa']
p = {'alger': 25, 'djelfa': 24, 'adrar': 16}

for dir in os.listdir('./pages'):
	if (re.match(r'\d{4}', dir)):
		for place in places:
			Path(f'./output/{dir}/{place}/offset').mkdir(parents=True, exist_ok=True)

			for i in tqdm(range(3, 15), f'  Parsing Offset ({place})'):
				output = open(f'./output/{dir}/{place}/offset/{i-2}.txt', 'w', encoding='utf-8')

				file = open(f'./pages/{dir}/{place}/offset/page-{i}.txt', 'r', encoding='utf-8')

				if place == 'adrar':
					matches = tuple(re.finditer(r'(-?(\d+)\s{1,2}){96}', file.read()))

					first = list(filter(None, matches[0].group().split(' ')))
					first = [first[i:i + p[place]] for i in range(0, len(first), p[place])]

					second = list(filter(None, matches[1].group().split(' ')))
					second = [second[i:i + p[place]] for i in range(0, len(second), p[place])]

					lines = ''
					for a in first: lines += '\n' + '|'.join(a)
					lines += '\n'
					for a in second: lines += '\n' + '|'.join(a)

				else:
					matches = tuple(re.finditer(r'(-?(\d+)\s{1,2}){138,151}', file.read()))

					arr = list(filter(None, matches[0].group().split(' ')))
					arr = [arr[i:i + p[place]] for i in range(0, len(arr), p[place])]

					lines = ''
					for a in arr:
						if len(a) == p[place] : lines += '\n' + '|'.join(a)
						
				output.write(lines[1:])