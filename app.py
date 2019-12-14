#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests as req
import re
import sys
import getopt

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 's:w:')
for opt, arg in opts:
	if opt in ['-s']:
		nazwa_slownika = argv[1]
	if opt in ['-w']:
		if argv[3] == re.search('.+\..+\..+', argv[3]):
			print(argv[3])
			adres = str(argv.pop[3])
			print(adres)

f = open(nazwa_slownika)
slownik_txt = f.read()
f.close()
slownik_txt = re.sub(' się ', ' ', slownik_txt)
slownik_txt = re.split('\W', slownik_txt)
slownik_txt = dict(slownik_txt[i:i+2] for i in range(0, len(slownik_txt), 2))
slownik_txt = dict([key, int(value)] for key, value in slownik_txt.items())


def score_strony(adres):
	kodowniki = {'span': [], 'a': [], 'p': [], 'li': [], 'pre': [], 'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [],
				 'div': []}
	lista_slow = {'span': [], 'a': [], 'p': [], 'li': [], 'pre': [], 'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [],
				  'div': []}

	trudnosc = {'trudnym': 0.2, 'srednio-trudnym': 0.4, 'srednim': 0.6, 'srednio-latwym': 0.8, 'latwym': 1}

	text = []
	text0 = []
	text1 = []
	wyrazy = []
	score = 0
	wyraz_nrozp = 0

	link = str(adres)

	strona = (req.get(link)).text

	# wyciągam na podstawie <span>, <a>, <p>
	for wyraz in kodowniki:
		kodowniki[wyraz] = re.findall('<' + wyraz + '.*?>\s*.+\s*<\/' + wyraz + '>', strona)
		for kod in kodowniki[wyraz]:
			wyraz_zformatowany = re.sub('<' + wyraz + '.*?>', '', kod)
			wyraz_zformatowany = re.sub('</' + wyraz + '.*?>', '', wyraz_zformatowany)
			wyraz_zformatowany = re.sub('\n*', '', wyraz_zformatowany)
			wyraz_zformatowany = re.sub('.*>', '', wyraz_zformatowany)
			lista_slow[wyraz].append(wyraz_zformatowany)

	for wyraz in lista_slow:
		text0 += lista_slow[wyraz]

	for i in text0:
		i = re.sub('&.*?;', '', i)
		i = re.sub('www\..*', '', i)
		i = re.sub('<.*>', '', i)
		words_list = re.split('[:;,\|?!% \'"\]\[0-9]', i)
		if len(words_list) > 0:
			wyrazy += words_list

	for wyraz in wyrazy:
		if wyraz != '' and wyraz != '.' and wyraz != '-' and wyraz != '...':
			text.append(wyraz)


	for wyraz in text:
		if wyraz in slownik_txt:
			score += int(slownik_txt[wyraz])
		else:
			if len(wyraz) >= 4 and wyraz[:-1] in slownik_txt:
				score += int(slownik_txt[wyraz[:-1]])
			elif len(wyraz) >= 6 and wyraz[:-2] in slownik_txt:
				score += int(slownik_txt[wyraz[:-2]])
			elif len(wyraz) >= 8 and wyraz[:-3] in slownik_txt:
				score += int(slownik_txt[wyraz[:-3]])
			else:
				wyraz_nrozp += 1

	wsp_wyraz_nrozp = round((wyraz_nrozp / len(text) * 100), 3)		#obliczam współczynnik wyrazów nierozpoznanych i zaokrąglam do 3 miejsc po przecinku
	sr_score = score/len(text)
	wartosci_sort = list(sorted(slownik_txt.values()))				#uzyskuję listę wartości w słowniku do przyszłej normalizacji danych
	max_wartosc = wartosci_sort[-1]
	min_wartosc = wartosci_sort[0]
	norm_score = (sr_score-min_wartosc)/(max_wartosc-min_wartosc)	#wykonuję normalizajcę z uwzglęgnieniem wartości min i max w słowniku
	for i in list(sorted(trudnosc.values())):
		if norm_score <= i:
			info_norm_score = ('Tekst zostal napisany ' + str([key for key, value in trudnosc.items() if i == value].pop()) + ' jezykiem. Score wynosi: ' + str(round(norm_score, 4)))
			break
	if wsp_wyraz_nrozp >= 50:
		info_nrozp = (str(wsp_wyraz_nrozp) + ' % wyrazow ze strony internetowej {} nie zostalo rozpoznanych w podanym słowniku. W celu uzyskania lepszego wyniku, sprobuj uzyc obszerniejszego slownika.').format(link)
	else:
		info_nrozp = (str(wsp_wyraz_nrozp) + ' % wyrazow ze strony internetowej {} nie zostalo rozpoznanych w podanym słowniku.').format(link)

	info_l_wyraz = print('Liczba odczytanych wyrazow wynosi: ' + str(len(text)))

	return info_l_wyraz, info_norm_score, info_nrozp

print(score_strony(adres))
