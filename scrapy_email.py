import requests
import re
from lxml import html
import datetime
import unicodecsv as csv
import re
from nameparser import HumanName



def countword(str):
	_len = len(str.split())
	return _len


def removesuffix(name):
	suffix_list = ['JR', 'II', 'III', 'SR']
	for item in suffix_list:
		if item in name:
			name = name.replace(item, "")
			break
	return name

def removelastComma(name):
	if name[-1] == ".":
		return name[:-1]
	else:
		return name 
def include_str(name):
	remove_list = ["&", "LAW GROUP", "LEGAL GROUP", "LAW FIRM", "STRATEGIC LEGAL PRACTICES", "|", "LAW CORPORATION"]
	_include = False
	for item in remove_list:
		if item in name:
			name = name.replace(item, "")
			_include = True
			break
	return _include

def nameType(name):
	_len = len(name.split())
	if _len == 2:
		return "plain"
	elif _len == 3:
		return "full"
	else:
		return "unknown"

def includeSuffix(name):
	suffix_list = [' JR.', ' II', ' III', ' SR.']
	_suffix_list = ['Jr', 'II', 'III', 'Sr']
	result = "None"
	suffix = "None"
	for no, item in enumerate(suffix_list):
		if item in name:
			result = name.replace(item, "")
			suffix = _suffix_list[no]

			break
	return {"name": result, "suffix": suffix}

def filter(name):
	if nameType(name) == "full":
		if re.search("([A-Z]+)\s([A-Z]+)\s([A-Z]+)", name):
			# print("aa")
			return name
		elif re.search("([A-Z]+)\s([A-Z]\.)\s([A-Z]+)", name):
			m = re.search("([A-Z]+)\s([A-Z]\.)\s([A-Z]+)", name)
			# print("bb")
			return m.group(3) + " " + m.group(1) + " " + m.group(2)
		else: 
			return name
	elif nameType(name) == "plain":
		return name
	else:
		return name


def _get_email_city(_name, _full_name=""):
	a_names = []
	emails = []
	cities = []
	data = {"email": emails, "city": cities, "a_name": a_names}
	_name = filter(_name)
	name = HumanName(_name)

	name.capitalize()
	if nameType(_name) == "full":
		full_name = name.first + ", "+name.middle + " " + name.last
		full_name = [removelastComma(full_name)]
	else:
		full_name = [name.first + ", " + name.last, name.last + ", " + name.first]

	# print(full_name)
	for item in full_name:
		# print(item)
		isExist = False
		params = (
		    ('FreeText', item),
		    ('SoundsLike', 'false'),
		)
		# print(item)
		response = requests.get('http://members.calbar.ca.gov/fal/LicenseeSearch/QuickSearch', headers=headers, params=params, cookies=cookies)

		response_text = response.text
		parser = html.fromstring(response_text)
		result =  parser.xpath("//table[@id='tblAttorney']/tbody/tr")
		
		for _item in result:
			_result = _item.xpath("./td[1]/a")[0].text

			if countword(_result) == countword(item):
				if item in _result:
					# isExist = True
					t_email = ''
					email = ''
					_full_name = _result
					# print("no: %s ---- %s" %(no+1, _result))
					_result_number = _item.xpath("./td[1]/a")[0].get('href')
					city = _item.xpath("./td[4]")[0].text
					result_number = _result_number.split("/")[4]
					# print(result_number)
					response1 = requests.get('http://members.calbar.ca.gov/fal/Licensee/Detail/'+result_number, headers=headers, cookies=cookies)
					# print(response1.text)
					parser1 = html.fromstring(response1.text)
					try:
						style = parser1.xpath("//style")[0].text
						m = re.search("{display:none;}#e([0-9]+){display:inline;}", style)
						_no = m.group(1)
						# print(_no)
						temp_email = parser1.xpath('//div[@id="moduleMemberDetail"]/div/p[6]/span[@id="e'+str(_no)+'"]/text()')
						for temp in temp_email:
							t_email += "."+temp
						for letter in range(1,len(t_email)):
							email += t_email[letter] 
						
					except Exception as e:
						# print(e)
						email = "Not Available "
					# print(city+"   " + email)
					a_names.append(_result)
					emails.append(email)
					cities.append(city)

	return data

def get_email_city(name):
	
	if include_str(name) == True:
		return ""
	else:
		# name = name_filter(name)
		# print(name)
		if includeSuffix(name)["name"] == "None":
			# print("AAA")
			return _get_email_city(name)
		else:
			name_suffix = includeSuffix(name)
			name = name_suffix["name"]
			suffix = name_suffix["suffix"]
			return _get_email_city(name)


headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

params = (
    ('ResultType', '0'),
    ('SearchType', '0'),
    ('SoundsLike', 'False'),
)

response = requests.get('http://members.calbar.ca.gov/fal/LicenseeSearch/QuickSearch', headers=headers, params=params)

NET_SessionId = response.cookies['ASP.NET_SessionId']
cookie1 = response.cookies['BIGipServerpool_211_cluster-members.calbar.org_80']
cookie2 = response.cookies['TS01b2ed66']

cookies = {
    'ASP.NET_SessionId': NET_SessionId,
    'BIGipServerpool_211_cluster-members.calbar.org_80': cookie1,
    'TS01b2ed66': cookie2,
}




