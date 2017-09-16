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
		self.search_tags = ["programming-languages", "frameworks", "academia", "misc"]

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
		for i in range(len(data)):
			temp_dict = {}
			for tag in data[self.search_tags[i]]:
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
		for i in range(len(self.search_tags)):
			filename = '{}_results.json'.format(self.search_tags[i])
			with open(filename, 'w') as fp:
				json.dump(freqcount_dicts[i], fp)

	def plot(self, filename):
		try:
			with open(filename) as data_file:
				data = json.load(data_file)
		except:
			print("Filename doesn't exist")
			return
		print(data)
		ranked_tuples = reversed(sorted(data.items(), key=lambda x: x[1]))
		labels = []
		scores = []
		for i in ranked_tuples:
			labels.append(i[0])
			scores.append(i[1])
		y_pos = np.arange(len(labels))
		plt.barh(y_pos, list(reversed(scores)), align='center', alpha=0.5)
		plt.yticks(y_pos, list(reversed(labels)))
		plt.xlabel('Count')
		plt.title('Word Frequencies in Queried Job Postings')
		plt.show()


indeed = IndeedJobFrequency("search_tags.json", "data+scientist", 1)
indeed.run()
indeed.plot("academia_results.json")

#

