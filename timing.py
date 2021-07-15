import re
from pathlib import Path
from tqdm import tqdm

print('\nParsing Timing')

places = ['alger', 'adrar', 'djelfa']

for place in places:
	Path(f'./output/{place}/timing').mkdir(parents=True, exist_ok=True)

	for i in tqdm(range(3, 15), f'  Parsing Timing ({place})'):
		output = open(f'./output/{place}/timing/{i-2}.txt', 'w', encoding='utf-8')

		file = open(f'./pages/{place}/timing/page-{i}.txt', 'r', encoding='utf-8')
		text = file.read()

		dates = re.finditer(r'((20\d{2}(\-|\/)(0?[1-9]|1[012])(\-|\/)(0[1-9]|[​12][0-9]|3[01]))|((0[1-9]|[​12][0-9]|3[01])(\-|\/)(0?[1-9]|1[012])(\-|\/)20\d{2}))', text)
		for date in dates:
			d = date.group().replace('/', '-')
			if (re.match(r'((0[1-9]|[​12][0-9]|3[01])(\-|\/)(0?[1-9]|1[012])(\-|\/)20\d{2})', d)):
				d = '-'.join(d.split('-')[::-1])
			text = text.replace(date.group(), f' {d} ===== ')

		lines = text.split('\n')
		l = ''
		for line in lines:
			times = tuple(re.finditer(r'(([01]\d|2[0-3])|//):(([0-5]\d)|//)', line))
			if (len(times)):
				for time in tuple(times):
					line = line.replace(time.group(), f'|{time.group()}|')
				l += '\n' + line.split('=====')[0].replace('| ', '|').replace('||', '|').replace('||', '|')[1:]

		output.write(l[1:])