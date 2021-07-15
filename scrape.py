import PyPDF4
import fitz
from pathlib import Path
from tqdm import tqdm

print('Scraping data from PDF')

places = ['alger', 'adrar', 'djelfa']

for place in places:
	Path(f'./pages/{place}/timing').mkdir(parents=True, exist_ok=True)
	Path(f'./pages/{place}/offset').mkdir(parents=True, exist_ok=True)

	file = fitz.open(f'./1442/{place}.pdf')

	i = 1
	for page in tqdm(file, f'  Scraping Timing ({place})'):
		out = open(f'./pages/{place}/timing/page-{i}.txt', 'wb')
		i += 1
		out.write(page.getText().encode('utf-8'))

	pdfFileObj = open(f'./1442/{place}.pdf', 'rb')
	pdfReader = PyPDF4.PdfFileReader(pdfFileObj, strict=False)

	for i in tqdm(range(3, 15), f'  Scraping Offset ({place})'):

		pageObj = pdfReader.getPage(i - 1)
		pages_text = pageObj.extractText()

		open(f'./pages/{place}/offset/page-{i}.txt', 'w', encoding='utf-8').write(' '.join(pages_text.split('\n')))