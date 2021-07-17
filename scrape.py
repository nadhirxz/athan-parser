import PyPDF4
import fitz
from pathlib import Path
from tqdm import tqdm
import os
import re

INPUT_FOLDER = './input'

print('Scraping data from PDF')

for dir in os.listdir(INPUT_FOLDER):
	if (re.match(r'\d{4}', dir)):
		p = os.path.join(INPUT_FOLDER, dir)
		places = ['alger', 'adrar', 'djelfa']

		for place in places:
			Path(f'./pages/{dir}/{place}/timing').mkdir(parents=True, exist_ok=True)
			Path(f'./pages/{dir}/{place}/offset').mkdir(parents=True, exist_ok=True)

			file = fitz.open(f'{p}/{place}.pdf')

			i = 1
			for page in tqdm(file, f'  Scraping Timing ({place.capitalize()} - {dir})'):
				out = open(f'./pages/{dir}/{place}/timing/page-{i:02}.txt', 'wb')
				i += 1
				out.write(page.getText().encode('utf-8'))

			pdfFileObj = open(f'{p}/{place}.pdf', 'rb')
			pdfReader = PyPDF4.PdfFileReader(pdfFileObj, strict=False)

			for i in tqdm(range(3, 15), f'  Scraping Offset ({place.capitalize()} - {dir})'):

				pageObj = pdfReader.getPage(i - 1)
				pages_text = pageObj.extractText()

				open(f'./pages/{dir}/{place}/offset/page-{i:02}.txt', 'w', encoding='utf-8').write(' '.join(pages_text.split('\n')))