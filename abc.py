import re
import mechanize
import urllib,codecs
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint



excel = codecs.open("./finaldata.csv", "w", "latin-1")
excel.write('First Name, Last Name, Title, Phone, Address, City, State, Accept New Patients, Gender, Specialties\n')

zipcode = "90025"
url = "http://www.abctcentral.org/xFAT/?fa=search_Advanced"
br = mechanize.Browser(factory=mechanize.RobustFactory())
br.set_handle_robots(False)   
br.set_handle_refresh(False)  
br.addheaders = [('User-agent', 'Firefox')]
response = br.open(url)
br.form = list(br.forms())[0] 
br["vZip"] = str(zipcode)
br["vRadius"] = ["100"]
response1 = br.submit()
html = response1.read()

print html