from bs4 import BeautifulSoup as Soup
import re, pandas as pd
from selenium import webdriver
import sys, os
import json
import matplotlib.pyplot as plt
import numpy as np

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
		pl_tags = data["programming-languages"]
		pl_dict = {}
		for tag in pl_tags:
			pl_dict[tag] = 0
		fw_tags = data["frameworks"]
		fw_dict= {}
		for tag in fw_tags:
			fw_dict[tag] = 0
		aca_tags = data["academia"]
		aca_dict = {}
		for tag in aca_tags:
			aca_dict[tag] = 0
		misc_tags = data["misc"]
		misc_dict = {}
		for tag in misc_tags:
			misc_dict[tag] = 0
		return [pl_dict, fw_dict, aca_dict, misc_dict]

	def __updateFreqCountFromPage(self, _url):
		try:
			url = self.indeed_url + _url
			soup = self.__getSoupObj(url)
			for script in soup(["script", "style"]):
				script.extract()
			text = soup.get_text()
			text = re.sub("[^a-zA-Z.+3#]", " ", text)
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
			text = self.__updateFreqCountFromPage(url)
			for dictionary in freqDict:
				for word in text:
					if word in dictionary:
						dictionary[word] += 1
			count += 1
			print(count)
		return freqDict

	def plot(self):
		freqcounts = self.__getFreqCounts()
		for updated_dict in freqcounts:
			ranked_tuples = reversed(sorted(updated_dict.items(), key=lambda x: x[1]))
			labels = []
			scores = []
			for i in ranked_tuples:
				labels.append(i[0])
				scores.append(i[1])
			y_pos = np.arange(len(labels))
			plt.barh(y_pos, list(reversed(scores)), align='center', alpha=0.5)
			plt.yticks(y_pos, list(reversed(labels)))
			plt.xlabel('Count')
			plt.title('Word Frequencies in Machine Learning Job Postings')
			plt.show()


indeed = IndeedJobFrequency("search_tags.json", "machine+learning", 100)
indeed.plot()


#

