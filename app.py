#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Autor: Maciej Kiełek, nr albumu 420204, I rok magisterski Bioinformatyki na Wydziale MIM, UW.
Projekt zaliczeniowy z pythona 1.
Program określa na podstawie słownika, który mu się dostarcza po przez argument -s w formie pliku tekstowego trudność
języka stron internetowych. (Słownik frekwencyjny powinien być zapisany w postaci pliku tekstowego gdzie w każdej linii
jest podane słowo oraz po spacji jego częstość)
Strony internetowa można podać na 3 sposoby po przez argument -w:
1. Plik tekstowy w formacie .txt ze adresami stron internetowych, każdy w osobnej linii
2. Adres pojedynczej strony internetowej (np.: adresstrony.pl ; dopuszczalne też są adresy o podwójnych domenach typu adresstrony.com.pl)
3. Adres dostarczony w formie Standard input.
Program nie posiada funkcji '-help'.
Chciałem użyć argpare żeby było to troszkę bardziej intuicyjne, ale wymagany był getopt().
'''

import requests as req
import re
import sys
import getopt

#tutaj tworzę parser, który przyjmuje dwa argument - slownik (s) oraz adresy url (w)

argv = sys.argv[1:]
if len(argv) == 4:
	opts, args = getopt.getopt(argv, 's:w:')
	for opt, arg in opts:
		if opt in ['-s']:
			nazwa_slownika = arg
		if opt in ['-w']:
			urle = arg

else:
	argv = sys.argv[5:]
	opts, args = getopt.getopt(argv, 's:w:')
	for opt, arg in opts:
		if opt in ['-s']:
			nazwa_slownika = arg
		if opt in ['-w']:
			urle = arg
# print(urle)
#tworzę słownik, pozbywam się słowa "się" z czasowników zwrotnych
f = open(nazwa_slownika)
slownik_txt = f.read()
f.close()
slownik_txt = re.sub(' się ', ' ', slownik_txt)
slownik_txt = re.split('\W', slownik_txt)
slownik_txt = dict(slownik_txt[i:i+2] for i in range(0, len(slownik_txt), 2))
slownik_txt = dict([key, int(value)] for key, value in slownik_txt.items())

#program sprawdza czy ma do czynienia z plikiem z adresami url(.txt), adresem strony, bądź standard input

if re.search('.+\.txt', urle) != None:
	urle_txt = open(urle).read()
	linki = urle_txt.split('\n')
	linki.pop()
elif re.search('.*\.?.+\.?.+\..+', urle) != None:
	linki = []
	linki.append(urle)
elif urle == '-':
	linki = []
	for line in sys.stdin:
		print(line)
else:
	linki = []
	print('Podano blednie url badz plik z adresami url.')




#funkcja przyjmującą jako argument adres strony
def score_strony(adres):

#słwoniki, które później przydadzą się przy web scrapingu - tekst ze stron będzie wyciągany na podstawie kluczy zawartych w poniższych słownikach
	kodowniki = {'span': [], 'a': [], 'p': [], 'li': [], 'pre': [], 'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [],
				 'div': []}
	lista_slow = {'span': [], 'a': [], 'p': [], 'li': [], 'pre': [], 'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [],
				  'div': []}

#przedziały wg których będzie ewaluwoany tekst napisany na stronie
	trudnosc = {'trudnym': 0.2, 'srednio-trudnym': 0.4, 'srednim': 0.6, 'srednio-latwym': 0.8, 'latwym': 1}

	text = []
	text0 = []
	text1 = []
	wyrazy = []
	score = 0
	wyraz_nrozp = 0

	link = str(adres)

	strona = (req.get(link)).text


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
		info_nrozp = str(wyraz_nrozp) + ', czyli ' + (str(wsp_wyraz_nrozp) + ' % wszystkich wyrazow ze strony internetowej {} nie zostalo rozpoznanych w podanym słowniku. W celu uzyskania lepszego wyniku, sprobuj uzyc obszerniejszego slownika.').format(link)
	else:
		info_nrozp = str(wyraz_nrozp) + ', czyli ' + (str(wsp_wyraz_nrozp) + ' % wszystkich wyrazow ze strony internetowej {} nie zostalo rozpoznanych w podanym słowniku.').format(link)

	info_l_wyraz = 'Liczba odczytanych wyrazow wynosi: ' + str(len(text))


	info_adres_strony = 'Analizowana strona to: ' + link

	return info_adres_strony, info_l_wyraz, info_norm_score, info_nrozp

if len(linki) != 0:
	for link in linki:
		if link != re.search('[^http://]', link):
			link = 'http://'+link
			for element in score_strony(link):
				print(element)
			print('\n---------------------------------------------\n')
		else:
			for element in score_strony(link):
				print(element)
			print('\n---------------------------------------------\n')

