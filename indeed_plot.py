import numpy as np
import seaborn as sns
import json
import matplotlib.pyplot as plt
import math
sns.set(style="dark")

def getX_Y(filename, query):
	with open(filename) as data_file:
		data = json.load(data_file)
	ranked_tuples = reversed(sorted(data[query].items(), key=lambda x: x[1]))
	labels = []
	scores = []
	for i in ranked_tuples:
		labels.append(i[0])
		scores.append(int(i[1]))
	return labels, scores

def plot(X,Y,title):
	y_pos = np.arange(len(X))
	plt.barh(y_pos, list(reversed(Y)), align='center', alpha=0.8)
	plt.yticks(y_pos, list(reversed(X)))
	plt.xlabel('Count')
	plt.title(title)
	plt.show()


filenames = ["programming-languages","academia","misc","frameworks"]
categories = ["data+engineer","data+scientist","machine+learning","data+analytics"]

for i in filenames:
	for j in categories:
		filename = '{}_results.json'.format(i)
		labels, counts = getX_Y(filename, j)
		job_role = j.split('+')
		title = 'Query: {} {}'.format(job_role[0],job_role[1])
		plot(labels, counts, title)
