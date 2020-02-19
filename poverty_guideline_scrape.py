import bs4, requests, re

res = requests.get('https://aspe.hhs.gov/prior-hhs-poverty-guidelines-and-federal-register-references')
# res = requests.get('https://aspe.hhs.gov/poverty-guidelines')
soup = bs4.BeautifulSoup(res.text, 'html.parser')
# poverty = soup.select(
    # 'table.footable:nth-child(3) > tbody:nth-child(2) > tr:nth-child(5) > td:nth-child(2)')

poverty_table = soup.select('.footable')

# now parse poverty table to get a dict of the year and 
# the corresponding poverty level for a family of four
th = soup.thead.findAll('th')
headers = [th[0].text, re.sub('\s+',' ',th[3].text )]
print(headers)
# rows
test_dict = {}
# I need td[0] (year) and td[3] for each tr in tbody
for tr in soup.tbody.findAll('tr'):
    if len(tr.findAll('td')) > 1:
        test_dict[tr.findAll('td')[0].text[:4]] = int(tr.findAll('td')[3].text[2:-1].replace(',','')) 
    else:
        pass


prnt_str = f'{headers[0]}: 2007, {headers[1]}: {test_dict["2007"]}'
print(prnt_str) 
print(test_dict)       