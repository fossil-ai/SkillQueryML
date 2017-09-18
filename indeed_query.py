from bs4 import BeautifulSoup as Soup
import re, pandas as pd
from selenium import webdriver
import sys, os
import json

class IndeedJobFrequency:

	def __init__(self, json_file, query, numOfPages,):
		self.indeed_url = "https://www.indeed.com/"
		self.json_file = json_file
		self.numOfPages = numOfPages
		self.query = query
		self.driver = webdriver.Chrome(os.getcwd() + "/chromedriver.exe")
		self.urls = []
		self.tag_list = []

	def getURLs(self):
		for i in range(self.numOfPages):
			append_num = (i + 1) * 10
			base_url = '{}jobs?q={}&start={}'.format(self.indeed_url,self.query,append_num)
			soup = self.__getSoupObj(base_url)
			for link in soup.find_all('h2', {'class': 'jobtitle'}):
				job_tag = link.a.get('href')
				if 'pagead' not in job_tag:
					self.urls.append(job_tag)
		print("Added {} URLs Job Postings...".format(len(self.urls)))
		return self.urls

	def __getSoupObj(self, url):
		self.driver.get(url)
		html = self.driver.page_source
		soup = Soup(html, 'html.parser')
		return soup

	def __getTagDicts(self):
		with open(self.json_file) as data_file:
			data = json.load(data_file)
		dict_list = []
		self.keys = list(data.keys())
		for i in range(len(data)):
			temp_dict = {}
			for tag in data[self.keys[i]]:
				temp_dict[tag] = 0
			dict_list.append(temp_dict)
		return dict_list

	def __getTextFromPage(self, _url):
		try:
			url = self.indeed_url + _url
			soup = self.__getSoupObj(url)
			for script in soup(["script", "style"]):
				script.extract()
			text = soup.get_text()
			text = re.sub("[^a-zA-Z.+3#&]", " ", text)
			text = text.lower().split()
			return text
		except:
			return "Error"

	def __getFreqCounts(self):
		urls = self.getURLs()
		freqDict = self.__getTagDicts()
		count = 0
		for url in urls:
			print(url)
			text = self.__getTextFromPage(url)
			for dictionary in freqDict:
				for word in text:
					if word in dictionary:
						dictionary[word] += 1
			count += 1
			print(count)
		return freqDict


	def run(self):
		freqcount_dicts = self.__getFreqCounts()
		for i in range(len(self.keys)):
			filename = '{}_results.json'.format(self.keys[i])
			with open(filename,"r") as data_file:
				data = json.load(data_file)
			data[self.query] = freqcount_dicts[i]
			with open(filename, "w") as json_file:
				json.dump(data, json_file)


indeed = IndeedJobFrequency("search_tags.json", "data+analytics", 100)
indeed.run()
