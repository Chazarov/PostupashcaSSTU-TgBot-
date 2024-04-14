import requests
from bs4 import BeautifulSoup as Bs
from config import FACULTS


def sort(l):
    return int(l[1])

for num in FACULTS.keys():
    URL = FACULTS[num]
    WAY = requests.get(URL)
    soup = Bs(WAY.text, 'html.parser')

    all_entrans = soup.find_all('div', class_='rasp-block')

    counter = 0
    for i in all_entrans: counter += 1

    c = 0
    entrans = dict()
    for i in all_entrans:
        c += 1
        if c < counter: continue
        general_comp = i.find('tbody', class_='text-center').find_all('tr')
        for entran in general_comp:
            name = str(entran.find('td', class_='align-middle text-left').get_text()).strip()
            dop_inf = name[-80:].strip()
            name = name[:100].strip()
            name += ' '*abs(35 - len(name))
            entrans[name] = []

            k = 0
            for data_of_ent in entran.find_all('td', class_='align-middle'):
                k += 1
                if k < 3 or k > 10: continue
                info = str(data_of_ent.get_text()).strip()
                entrans[name] += [info]

    for i in entrans.keys():
        try:
            entrans[i][0] = int(entrans[i][0])
        except ValueError:
            entrans[i][0] = float(entrans[i][0].replace(',', '.'))

    entrans = dict(sorted(entrans.items(), key = lambda x:x[1], reverse = True))

    c = 0
    pars = ''
    for i in entrans:
        c += 1
        pars += f" =№{c}     {i}  сумма: {entrans[i][0]} \n \
 приоритет поступления:  {entrans[i][5]} " + '\n'

    print(c)
    with open('facults/' + num + '.txt', 'w') as file:
        file.write(pars)