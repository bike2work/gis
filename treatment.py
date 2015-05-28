import re
import mechanize
import urllib,codecs
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.datadetail = []

		self.resultContent = 0
		self.name = 0
		self.writeName = 0
		self.title = 0
		self.address = 0
		self.phone = 0
		self.info = 0


	def handle_starttag(self, tag, attrs):
		if tag == 'div':
			for name, value in attrs:
				if name == 'class' and value == 'resultContent':
					self.resultContent = 1

		if tag == 'div':
			for name, value in attrs:
				if name == 'class' and value == 'resultInfo':
					self.name = 1

		if tag == 'a' and self.name == 1:
			self.writeName = 1
		
		if self.resultContent == 1 and tag == 'span':
			self.title = 1

		if tag == 'p':
			for name, value in attrs:
				if name == 'class' and value == 'address':
					self.address = 1	

		if tag == 'div':
			for name, value in attrs:
				if name == 'class' and value == 'phoneNum':
					self.phone = 1

		if tag == 'dl':
			self.info = 1

	def handle_endtag(self, tag):
		if tag == 'a' and self.name == 1:
			self.name = 0
			self.writeName = 0

		if tag == 'span' and self.title ==1:
			self.title = 0

		if tag == 'p' and self.address == 1: 	
			self.address = 0

		if tag == 'div' and self.phone == 1:
			self.phone = 0

		if tag == 'dl':
			self.info = 0

		if tag == 'div' and self.resultContent == 1:
			self.resultContent = 0;


	def handle_data(self, data):
		if self.writeName == 1:
			self.datadetail.append(('name', data.strip()))
		if self.title == 1:
			self.datadetail.append(('title', data.strip()))
		if self.address == 1:
			self.datadetail.append(('address', data.strip()))
		if self.phone == 1:
			self.datadetail.append(('phone', data.strip()))
		if self.info == 1:
			self.datadetail.append(('info', data.strip()))	

	def get_data(self):
		return self.datadetail

	def check_result(self):
		return self.hasresult

excel = codecs.open("./TreatmentAdaa.csv", "w", "latin-1")
excel.write('Name; Title; Address; Phone')

urls = ("http://treatment.adaa.org/finding-help/search-results/zipcode/90025/radius/100/?pg=1",
	"http://treatment.adaa.org/finding-help/search-results/zipcode/90025/radius/100/?pg=2",
	"http://treatment.adaa.org/finding-help/search-results/zipcode/90025/radius/100/?pg=3",
	"http://treatment.adaa.org/finding-help/search-results/zipcode/90025/radius/100/?pg=4",
	"http://treatment.adaa.org/finding-help/search-results/zipcode/90025/radius/100/?pg=5",
	"http://treatment.adaa.org/finding-help/search-results/zipcode/90025/radius/100/?pg=6",
	"http://treatment.adaa.org/finding-help/search-results/zipcode/90025/radius/100/?pg=7")
br = mechanize.Browser(factory=mechanize.RobustFactory())
br.set_handle_robots(False)   
br.set_handle_refresh(False)  
br.addheaders = [('User-agent', 'Firefox')]
for url in urls:
	response = br.open(url)
	html = response.read()
	parser = MyHTMLParser()
	parser.feed(html)
	data_info = parser.get_data()

	for title, value in data_info:
		if title == "name":
			excel.write('\n')
			excel.write(value)
		else:
			excel.write(' ;'+value)

	parser.close()













