import requests
import re
from lxml import html
import datetime
import unicodecsv as csv
from requests.exceptions import ConnectionError
import xlsxwriter
import scrapy_name
import scrapy_email
import os
import configparser
from time import gmtime, strftime


fn     = "config.txt"

config = configparser.ConfigParser()

config.read(fn)

N = 15

unlimit = False

dirName = 'Excel'

try:
  os.mkdir(dirName)
  print("Directory " , dirName ,  " Created ") 
except:
  print("Directory " , dirName ,  " already exists")


try:
  civil_depart      = config['DEFAULT']['civil_list'].strip()
  civil_depart_list = civil_depart.split(', ')
  unlimit = True
except KeyError:
    unlimit = False







case_type_list          = ['general', 'probate', 'family']
provate_department_list = ['Probate Department 5', 'Probate Department 2D', 'Probate Department 9', 'Probate Department 11', 'Probate Department 29', 'Probate Department 67', 'Probate Department 79']

current_time   = strftime("%Y-%m-%d %H-%M-%S", gmtime())
__current_time = strftime("%H", gmtime())

if int(__current_time)  > 13 and int(__current_time) < 15:
  N = 8
elif int(__current_time) > 15 and int(__current_time) <= 17:
  N = 9
elif int(__current_time) >= 17 and int(__current_time) <= 19:
  N = 10
elif int(__current_time) >= 19 and int(__current_time) <= 21:
  N = 11
elif int(__current_time) >= 21 and int(__current_time) <= 23:
  N = 12
elif int(__current_time) >= 0 and int(__current_time) <= 1:
  N = 15
elif int(__current_time) >= 1 and int(__current_time) <= 3:
  N = 16

current_date   = datetime.datetime.now().strftime("%m/%d/%Y")
ahead_date     = (datetime.datetime.now() + datetime.timedelta(days=N)).strftime("%m/%d/%Y")
_ahead_date    = (datetime.datetime.now() + datetime.timedelta(days=N)).strftime("%Y-%m-%d")
print(__current_time+"  "+ahead_date)
headers = {
    'Connection'     : 'keep-alive',
    'Cache-Control'  : 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent'     : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}
response = requests.get('http://www.lacourt.org/', headers=headers)
NET_SessionId = response.cookies['ASP.NET_SessionId']

cookies = {
    'ASP.NET_SessionId': NET_SessionId,
}

def csv_merge():
  global _ahead_date
  print("merge")
  dt    = _ahead_date
  tmp   = 0
  workbook       = xlsxwriter.Workbook(os.path.join(r'./Excel', "Stanley Mosk Courthouse "+ str(dt) + ".xlsx"))  
  case_type_list = ['civil', 'probate', 'family']
  
  for case_type in case_type_list:
    worksheet = workbook.add_worksheet(case_type)
    file_name = ("Stanley_Mosk_Courthouse_"+ str(current_time) + " ("+case_type+ ")" + ".csv").encode('utf-8')
    file      = open(os.path.join('./Excel',file_name), "rb")
    reader    = csv.reader(file)
    index     = 0
    # tmp += 1
    for no, row in enumerate(reader):
      index += 1
      if index == 1:
        worksheet.write(0, 0, "Department")
        worksheet.set_column(0, 0, 15)
        worksheet.write(0, 1, "Date")
        worksheet.set_column(1, 1, 15)
        worksheet.write(0, 2, "Time")
        worksheet.set_column(2, 2, 15)
        worksheet.write(0, 3, "Event")
        worksheet.set_column(3, 3, 30)
        worksheet.write(0, 4, "Case Number")
        worksheet.set_column(4, 4, 15)
        worksheet.write(0, 5, "Case Title")
        worksheet.set_column(5, 5, 35)
        worksheet.write(0, 6, "Attorney's name")
        worksheet.set_column(6, 6, 30)
        worksheet.write(0, 7, "Attorney's email")
        worksheet.set_column(7, 7, 30)
        worksheet.write(0, 8, "Attorney city")
        worksheet.set_column(8, 8, 25)
        continue
      print(row[4])  
      print(no)
      worksheet.write(no, 0, row[0])
      worksheet.write(no, 1, row[1])
      worksheet.write(no, 2, row[2])
      worksheet.write(no, 3, row[3])
      worksheet.write(no, 4, row[4])
      worksheet.write(no, 5, row[5])
      worksheet.write(no, 6, row[6])
      worksheet.write(no, 7, row[7])
      worksheet.write(no, 8, row[8])
      tmp = no
  
  workbook.close() 


def filter_department_no(department_no):
  department_no = department_no.replace("Probate Department", "").replace("Department", "").strip()
  return department_no


def write_csv(writer, csvfile, data):  
  Department_No = data['Department_No'].strip()
  Hearing_Date = "  "+data['Hearing_Date'].strip()+"  "
  Hearing_Time = data['Hearing_Time'].strip()
  Event = data['Event'].strip()
  Case_No = data['Case_No'].strip()
  Case_Title = data['Case_Title'].strip()
  Attorney_Name = data['Attorney_Name'].strip()
  Attorney_Email = data['Attorney_Email'].strip()
  Attorney_City = data['Attorney_City'].strip()
  row = {
    'Department': Department_No, 'Date': Hearing_Date, 'Time' : Hearing_Time, 
    'Event': Event, 'Case Number': Case_No, 'Case Title': Case_Title, "Attorney's name": Attorney_Name, "Attorney's email": Attorney_Email,
    'Attorney city' : Attorney_City
  }
  writer.writerow(row)
  csvfile.flush()


def start():
  global ahead_date
  global N
  global headers
  global NET_SessionId
  csvfile = "result"
  dt = _ahead_date
  for case_type in case_type_list:
    if case_type == 'general':
      file_name = ("Stanley_Mosk_Courthouse_"+ str(current_time) + " (civil).csv").encode('utf-8')
    else:
      file_name = ("Stanley_Mosk_Courthouse_"+ str(current_time) + " ("+case_type+ ")" + ".csv").encode('utf-8')
    directory_in_str = './Excel/'+file_name.decode()
    print(directory_in_str)
    # directory = os.fsencode(directory_in_str)
    with open(directory_in_str, 'wb')as csvfile:
      fieldnames = ['Department', 'Date', 'Time', 'Event', 'Case Number', 'Case Title', "Attorney's name", "Attorney's email", 'Attorney city']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()
      
      if case_type == "probate":
        department_list = get_department(case_type)
        department_list = provate_department_list
      else:
        department_list = get_department(case_type)
      for department_no in department_list:
        print(department_no)
        print(case_type)
        try:
          data_list = get_table(str(department_no), case_type)
          print(data_list)
          for data in data_list:
            data['Department_No'] = filter_department_no(data['Department_No'])
            print(data['Case_No'])
            case_no = data['Case_No']
            try:
              print("A")
              names = scrapy_name.get_name(case_no, NET_SessionId, headers)
              print("dddd"+department_no)
              print(case_type)
              print(names)
              for name in names:
                print("hgjh")
                emails_cities = scrapy_email.get_email_city(name)
                print(emails_cities)
                emails = emails_cities["email"]
                cities = emails_cities["city"]
                a_names = emails_cities["a_name"]
                for index, email in enumerate(emails):
                  print("cgccu")
                  if email != 'Not Available':
                    # print(name)
                    print(email)
                    # print(cities[index])
                    data['Attorney_Name'] = a_names[index]
                    data['Attorney_Email'] = email
                    data['Attorney_City'] = cities[index]
                    write_csv(writer, csvfile, data)
            except Exception as e:
              print("Avoid recaptcha....")
        except Exception as e:
          print("Avoid recaptcha....")

def get_department(case_type):

  print("GETTING DEPARTMENT.....")
  # print(case_type)
  params = (
      ('CaseType', case_type),
  )

  response = requests.get('http://www.lacourt.org/CivilCalendar/ui/mainpanel.aspx', headers=headers, params=params, cookies=cookies)

  response_text = response.text
  # print(response_text)
  # try:
  parser = html.fromstring(response_text)
  try:
    __VIEWSTATE = parser.xpath("//input[@name='__VIEWSTATE']")[0].get('value')
    __EVENTVALIDATION = parser.xpath("//input[@name='__EVENTVALIDATION']")[0].get('value')


    data = [
      ('__VIEWSTATE', __VIEWSTATE),
      ('__VIEWSTATEGENERATOR', '2AD3A5A0'),
      ('__EVENTVALIDATION', __EVENTVALIDATION),
      ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$butDisclaimer', 'I Agree'),
    ]

    response = requests.post('http://www.lacourt.org/CivilCalendar/ui/mainpanel.aspx', headers=headers, params=params, cookies=cookies, data=data)

    response_text = response.text

    final_parser = html.fromstring(response_text)

    __VIEWSTATE = final_parser.xpath("//input[@name='__VIEWSTATE']")[0].get('value')
    __EVENTVALIDATION = final_parser.xpath("//input[@name='__EVENTVALIDATION']")[0].get('value')
  except:
    __VIEWSTATE = parser.xpath("//input[@name='__VIEWSTATE']")[0].get('value')
    __EVENTVALIDATION = parser.xpath("//input[@name='__EVENTVALIDATION']")[0].get('value')
  

  data = [
    ('__EVENTTARGET', 'ctl00$ctl00$siteMasterHolder$basicBodyHolder$ddlLocation2'),
    ('__EVENTARGUMENT', ''),
    ('__LASTFOCUS', ''),
    ('__VIEWSTATE', __VIEWSTATE),
    ('__VIEWSTATEGENERATOR', '2AD3A5A0'),
    ('__EVENTVALIDATION', __EVENTVALIDATION),
    ('CaseNumber', ''),
    ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$dateFrom', ahead_date),
    ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$dateTo', ahead_date),
    ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$ddlLocation2', 'LAM;LA;Stanley Mosk Courthouse;111 North Hill Street, Los Angeles, CA 90012'),
    ('hdnType', ''),
  ]

  response = requests.post('http://www.lacourt.org/CivilCalendar/ui/mainpanel.aspx', headers=headers, params=params, cookies=cookies, data=data)

  response_text = response.text

  parser = html.fromstring(response_text)


  department_data = parser.xpath("//select[@id='siteMasterHolder_basicBodyHolder_ddlDept']/option")
  department_list = []
  for department_no in department_data:
    department_list.append(department_no.text)
  print(department_list)
  print("END GET DEPARTMENT")
  return department_list

def get_table(department_no, case_type):
  # global cookies
  # print(cookies)
  # global final_parser
  print(ahead_date)
  isConnect = False
  while isConnect == False:
    try:
      print("START GETTABLE")
      params = (
          ('CaseType', case_type),
      )

      response = requests.get('http://www.lacourt.org/CivilCalendar/ui/mainpanel.aspx', headers=headers, params=params, cookies=cookies)

      response_text = response.text

      parser = html.fromstring(response_text)
     

      __VIEWSTATE = parser.xpath("//input[@name='__VIEWSTATE']")[0].get('value')
      __EVENTVALIDATION = parser.xpath("//input[@name='__EVENTVALIDATION']")[0].get('value')

      data = [
        ('__EVENTTARGET', 'ctl00$ctl00$siteMasterHolder$basicBodyHolder$ddlLocation2'),
        ('__EVENTARGUMENT', ''),
        ('__LASTFOCUS', ''),
        ('__VIEWSTATE', __VIEWSTATE),
        ('__VIEWSTATEGENERATOR', '2AD3A5A0'),
        ('__EVENTVALIDATION', __EVENTVALIDATION),
        ('CaseNumber', ''),
        ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$dateFrom', current_date),
        ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$dateTo', ahead_date),
        ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$ddlLocation2', 'LAM;LA;Stanley Mosk Courthouse;111 North Hill Street, Los Angeles, CA 90012'),
        ('hdnType', ''),
      ]

      
      response = requests.post('http://www.lacourt.org/CivilCalendar/ui/mainpanel.aspx', headers=headers, params=params, cookies=cookies, data=data)

      response_text = response.text
      #print(response_text)
      parser = html.fromstring(response_text)

      # parser = init()
      __VIEWSTATE = parser.xpath("//input[@name='__VIEWSTATE']")[0].get('value')
      __EVENTVALIDATION = parser.xpath("//input[@name='__EVENTVALIDATION']")[0].get('value')

      

      data = [
        ('__EVENTTARGET', ''),
        ('__EVENTARGUMENT', ''),
        ('__LASTFOCUS', ''),
        ('__VIEWSTATE', __VIEWSTATE),
        ('__VIEWSTATEGENERATOR', '2AD3A5A0'),
        ('__EVENTVALIDATION', __EVENTVALIDATION),
        ('CaseNumber', ''),
        ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$dateFrom', current_date),
        ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$dateTo', ahead_date),
        ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$ddlLocation2', 'LAM;LA;Stanley Mosk Courthouse;111 North Hill Street, Los Angeles, CA 90012'),
        ('ctl00$ctl00$siteMasterHolder$basicBodyHolder$ddlDept', department_no),
        ('hdnType', 'TYPE'),
        ('Loc', 'LAM'),
        ('Loc2', 'LA'),
        ('LocName', 'Stanley Mosk Courthouse'),
        ('LocAddress', '111 North Hill Street, Los Angeles, CA 90012'),
        ('Calendar', 'General Jurisdiction Civil Calendar'),
        ('DivCode', 'CV'),
      ]

      response = requests.post('http://www.lacourt.org/CivilCalendar/ui/mainpanel.aspx', headers=headers, params=params, cookies=cookies, data=data)

      response_text = response.text
      #print(response_text)
      parser = html.fromstring(response_text)


      table = parser.xpath("//table[@id='siteMasterHolder_basicBodyHolder_calendarDeptDate_tblResults']/tr")
      index = 0
      search_data = []
      for row in table:
        _search_data = {}
        index += 1
        if index == 1:
          continue
        try:
          _search_data['Department_No'] = str(department_no)
          print(str(department_no))
          _search_data['Hearing_Date'] = row[0].text
          _search_data['Hearing_Time'] = row[1].text
          _search_data['Event'] = row[2].text
          _search_data['Case_No'] = row[3].xpath("./a")[0].text
          _search_data['Case_Title'] = row[4].text
          search_data.append(_search_data)
        except ConnectionError as e:
          print("Avoiding....")
      isConnect = True
    except ConnectionError as e: 

      print("--------ConnectionError------------")
      isConnect = False
  print("END GETTABLE")    
  return search_data

start()
csv_merge()
for case_type in case_type_list:
  file_name = ("Stanley_Mosk_Courthouse_"+ str(current_time) + " ("+case_type+ ")" + ".csv").encode('utf-8') 
  if case_type == 'general':
    case_type = 'civil'
    file_name = ("Stanley_Mosk_Courthouse_"+ str(current_time) + " ("+case_type+ ")" + ".csv").encode('utf-8')
  os.remove(b"./Excel/"+file_name)
exit()

