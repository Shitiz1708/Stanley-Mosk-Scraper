import requests
import re
from lxml import html
import datetime
import unicodecsv as csv
import re
import six
import numpy
import io
import time

headers = {
    'Connection'     : 'keep-alive',
    'Cache-Control'  : 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent'     : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from requests.exceptions import ConnectionError
import random

proxies = []
fp = open('proxies.txt')
for proxy in fp:
    eachproxy = proxy[0:len(proxy)-1]
    proxies.append(eachproxy)
fp.close()

def name_filter(name):
	_suffix_list = ["Esq.", "Esq,", "Esq", "ESQ.", "ESQ,", "ESQ", "APC.", "APC", "A.P.C", "APLC.", "APLC", "LLP.", "LLP"]
	_suffix = "none"
	for item in _suffix_list:
		if item in name:
			_suffix = item
			break
	if _suffix != "none":
		name = name.split(_suffix)[0]
	name = name.replace("-", "").replace(":", "").replace("THE LAW OFFICE OF", "").replace("LAW OFFICES OF", "").replace("LAW OFFICE OF", "").replace("ATTORNEY AT LAW", "").replace("DEPUTY CITY ATTORNEY","").replace("CITY ATTORNEY", "").replace("DEPUTY ATTORNEY", "").replace("ATTORNEY GENERAL", "").replace("THE  ", "").strip()
	if (len(name.split(" ")) == 1):
		name = ""
	return name

def include_str(name):
	remove_list = ["&", "LAW GROUP", "LEGAL GROUP", "LAW FIRM", "STRATEGIC LEGAL PRACTICES", "|", "LAW CORPORATION", "INUMERABLE"]
	_include = False
	for item in remove_list:
		if item in name:
			name = name.replace(item, "")
			_include = True
			break
	return _include


def isName(name):
	_len = len(name.split())
	if  (_len > 1) and(_len < 4):
		return True
	else:
		return False
def get_name(case_no, NET_SessionId, headers):
	isConnect = False
	while isConnect == False:
		try:
			
			names = []		
			cookies = {
			    'ASP.NET_SessionId': NET_SessionId,
			}

			params = (
			    ('casetype', 'family'),
			)

			response = requests.get('http://www.lacourt.org/casesummary/ui/index.aspx', headers=headers, params=params, cookies=cookies)
			
			parser = html.fromstring(response.text)
			__VIEWSTATE = parser.xpath("//input[@name='__VIEWSTATE']")[0].get('value')
			__EVENTVALIDATION = parser.xpath("//input[@name='__EVENTVALIDATION']")[0].get('value')
			__VIEWSTATEGENERATOR = parser.xpath("//input[@name='__VIEWSTATEGENERATOR']")[0].get('value')
			data = [
			  ('__EVENTTARGET', ''),
			  ('__EVENTARGUMENT', ''),
			  ('__LASTFOCUS', ''),
			  ('__VIEWSTATE', __VIEWSTATE),
			  ('__VIEWSTATEGENERATOR', '30B793F7'),
			  ('__EVENTVALIDATION', __EVENTVALIDATION),
			  ('ctl00$ctl00$siteMasterHolder$basicCategoryHolder$ddlLanguages', 'en-us'),
			  ('CaseNumber', case_no),
			  ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$District', 'LAM')
			]
			proxy = {'https': random.choice(proxies)}
			print(proxy)
			print(data)
			#sh=open("scrapy_html.text","a")
			a=requests.post('http://www.lacourt.org/casesummary/ui/', headers=headers, cookies=cookies, data=data, proxies=proxy)
			f1=open("def.txt","w")
			f1.write(a.text)
			f1.close()
			print("1234567890")
			#response = requests.get('http://www.lacourt.org/casesummary/ui/casesummary.aspx', headers=headers, params=params, cookies=cookies, proxies=proxy)
			#f=open("ABC.txt","a")
			#f.write(response.text);
			#f.close()
			response=a;
			#print(response.text)
			# response = requests.get('http://www.lacourt.org/casesummary/ui/casesummary.aspx

			buf = io.StringIO(response.text)
			print("ASASAS")
			lines = buf.readlines()
			num_lines = len(lines)
			print(num_lines)
			suffix_list = ['- Attorney for Plaintiff/Petitioner', 'Atty for Defendant and Cross-Compl', '- Atty for Defendant and Cross-Compl', 
						'- Attorney for Defendant/Respondent', 'Attorney for Deft/Respnt', 'Former Attorney for Pltf/Petn', 'Former Attorney for Def/Respondent', 
						'Attorney for Pltf/Petn', ' - Attorney for Deft/Respnt', '-Attorney for Deft/Resp',
						'- Attorney for Deft/Resp', '- Associated Counsel', '- Atty for Defendant and Cross-Compl', '- Attorney for Real Pty in Interest',
						'- Attorney for Petitioner', '- Attorney for Respondent', 'Attorney for Petitioner for Petitioner', 'Attorney for Respondent for Respondent',
						'- Attorney for Respondent for Respondent', '- Attorney', '- Attorney for Claimant', '- Attorney for Converted Attorney',
						'- Converted Attorney', 'Attorney for Plaintiff:', 'Attorney for Defendant:', 'Attorney for Cross-Defendant:' ,
						'Attorney for Cross-Complainant', '- Attorney for Respondent for Trustee', 'Attorney for Respondent for Trustee',
						'Attorney:', 'Attorney for Cross-Complainant:']
			
			try:
				attorney_name_data = ''
				isStartParse = False
				print(isStartParse)
				for iLine in range(num_lines):
					#print(iLine)
					lineVal = lines[iLine].strip()
					print(lineVal)
					
					if lineVal == '<div id="siteMasterHolder_basicBodyHolder_CaseSummaryInfo1_PTYDOCREG1_NavPty_panUnlimited">':
						isStartParse = True
						print("enjwnd")
					if isStartParse == True:
						if lineVal == '<div id="siteMasterHolder_basicBodyHolder_CaseSummaryInfo1_PTYDOCREG1_panUnlimited">':
							isStartParse = False
							print("anjwnd")
							break
						else:
							attorney_name_data = lineVal
							print("vnjwnd")

				parser = html.fromstring(attorney_name_data)
				#print(parser)
				result = parser.xpath("//p")
				#print(result)

				for item in result:
					print("B")
					name = item.text
					_suffix = 'none'
					for suffix in suffix_list:
						if suffix in name:
							_suffix = suffix
							break
					if _suffix != 'none':

						name = name.split(_suffix)[0]
						name = name_filter(name)
						if (include_str(name) == False) and (isName(name) == True):
							names.append(name)
				isConnect = True
			except Exception as e:
				#print(e)
				try:
					_attorney_name_data = []
					isStartParse = False
					for iLine in range(num_lines):
						lineVal = lines[iLine].strip()
						if (lineVal == '<div id="siteMasterHolder_basicBodyHolder_CaseSummaryInfo1_PTYDOCREG1_NavPty_panLimited">'):
							isStartParse = True
						if isStartParse == True:
							if (lineVal == '<div id="siteMasterHolder_basicBodyHolder_CaseSummaryInfo1_PTYDOCREG1_NavROA_panLimited">'):
								isStartParse = False
								break
							else:
								_attorney_name_data.append(lineVal)

					attorney_name_data = _attorney_name_data[7]
					attorney_name_data= attorney_name_data.replace('<span class="boldText">', "")
					attorney_name_data = attorney_name_data.replace("</span>", "")
					attorney_name_data= attorney_name_data.replace("<BR> ", "<P>")
					parser = html.fromstring(attorney_name_data)
					result = parser.xpath("//p")
					for item in result:
		
						name = item.text
						if name != None:
							_suffix = 'none'
							for suffix in suffix_list:
								if suffix in name:
									_suffix = suffix
									break
							if (_suffix != 'none'):
								name = name.split(_suffix)[1]
								name = name_filter(name)
								if (include_str(name) == False) and (isName(name) == True):
									names.append(name)
					isConnect = True
				except Exception as e:
					print("Empty")
					isConnect = False
					return ""
			
		except Exception as e:
			print("Avoiding")
			isConnect = False
	return names




