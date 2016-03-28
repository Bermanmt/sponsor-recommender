import requests
from bs4 import BeautifulSoup

def get_cupons_yuplon(url):
	res_yuplon = requests.get(url).text
	soup_yuplon = BeautifulSoup(res_yuplon,'html.parser')
	promos_yuplon=soup_yuplon.find_all(class_='extra-campaign')
	promos_all = []
	keys =['titulo','link','precio','ahorro','imagen','pagina']
	for promo in promos_yuplon:
		titulo = promo.find(class_='offer-small-title').text
		link = 'http://www.yuplon.com/'+promo.a['href']
		precio = promo.find(class_='price').text
		ahorro= promo.find(class_='discount').text
		imagen= promo.img['src'].split('110x66')
		imagen=''.join(imagen)
		pagina='yuplon'
		promo_info = [titulo,link,precio,ahorro,imagen,pagina]
		promo_dict = dict(zip(keys,promo_info))
		promos_all.append(promo_dict)
	return promos_all








