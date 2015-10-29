import numpy as np
import operator
import matplotlib.pyplot as plt
import collections
from sets import Set
from collections import Counter
import re


def get_reviews_array(file_name):
	reviews_array = []
	with open(file_name) as fp:
		for line in fp:
			reviews_array.append(line.split('\t'))
	return reviews_array

reviews_array = get_reviews_array('./reviewsNew/reviewsNew.mP')
# reviews_array = get_reviews_array('reviewsNew.txt')
# reviews_array = get_reviews_array('./reviewsNew/reviews_test.mP')

def get_column_array(reviews_array, column=[0]):
	return_array = []
	for review in reviews_array:
		one_review = []
		for col in column:
			one_review.append(review[col])
		if len(one_review) == 1:
			return_array.append(one_review[0])
		else:
			return_array.append(one_review)
	return return_array

def get_reviews_content(reviews_array):
	return get_column_array(reviews_array, column=[-1])

def get_reviews_reviewers_relation(reviews_array):
	reviewers_array = get_column_array(reviews_array, column=[0])
	# for reviews in reviews_array:
	# 	reviewers_array.append(reviews[0])

	# count every reviewers' reviews number 
	c = Counter(e for e in reviewers_array)

	reviews_reviewers_dict = {}
	for x in c:
		num = c[x] 
		if not reviews_reviewers_dict.get(num):
			reviews_reviewers_dict[num] = 1
		else:
			reviews_reviewers_dict[num] += 1
	# count occurency of every reviews level
	return reviews_reviewers_dict

def get_reviews_products_relation(reviews_array):
	products_array = get_column_array(reviews_array, column=[1])
	# for reviews in reviews_array:
	# 	products_array.append(reviews[1])

	# count every products' reviews number 
	c = Counter(e for e in products_array)

	reviews_products_dict = {}
	for x in c:
		num = c[x] 
		if not reviews_products_dict.get(num):
			reviews_products_dict[num] = 1
		else:
			reviews_products_dict[num] += 1
	# count occurency of every reviews level
	return reviews_products_dict

def get_reviews_feedbacks_relation(reviews_array):
	feedbacks_array = []
	for reviews in reviews_array:
		if len(reviews):
			feedbacks_array.append(int(reviews[3]))

	# count every feedbacks' reviews number 
	c = Counter(e for e in feedbacks_array)
	# count occurency of every reviews level
	c = collections.OrderedDict(sorted(c.items()))
	return c

def get_reviews_rating_relation(reviews_array):
	rating_array = []
	for reviews in reviews_array:
		if len(reviews):
			rating_array.append(reviews[5])

	# count every rating' reviews number 
	c = Counter(e for e in rating_array)
	# count occurency of every reviews level
	c = collections.OrderedDict(sorted(c.items()))
	return c

def plot_relation(dict, xlabel='Num Reviews', ylabel='Num Members', use_log=True, plot_type='rx'):
	relation_x = []
	relation_y = []
	for i in dict.iterkeys():
		relation_x.append(float(i))
		relation_y.append(float(dict[i]))

	fig, ax =  plt.subplots()
	if use_log:
		ax.set_xscale('log', basex=10)
		ax.set_yscale('log', basey=10)
	plt.plot(relation_x, relation_y, plot_type)
	plt.ylabel(ylabel)
	plt.xlabel(xlabel)
	plt.axis([0, float(max(relation_x))*1.1, 0, float(max(relation_y))*1.1])
	plt.show()

def plot_percent(dict, xlabel='Rating', ylabel='Percent of Reviews'):
	relation_x = []
	relation_y = []
	for k, v in dict.iteritems():
		relation_x.append(k)
		relation_y.append(v)
	y_sum = sum(relation_y)
	for index, y in enumerate(relation_y):
		relation_y[index] = float(y) / y_sum
	fig, ax =  plt.subplots()
	# ax.set_xscale('log', basex=10)
	# ax.set_yscale('log', basey=10)
	plt.plot(relation_x, relation_y, 'r-')
	plt.ylabel(ylabel)
	plt.xlabel(xlabel)
	plt.axis([0, float(max(relation_x))*1.1, 0, float(max(relation_y))*1.1])
	plt.show()


def jaccard_distence(word1_set, words2_set):
	set_or = word1_set | words2_set
	set_and = word1_set & words2_set
	return float(len(set_and)) / len(set_or)

def get_2_grams(words=""):
	words_list = re.findall(r"[\w']+", words)
	# words_list_2 = [words_list[idx] + ' ' + words_list[idx+1] for idx, word in words_list]
	words_list_2 = []
	words_list_len = len(words_list)
	for idx, word in enumerate(words_list):
		if idx != words_list_len - 1:
			words_list_2.append(words_list[idx] + ' ' + words_list[idx + 1])
	return Set(words_list_2)

def get_js_list(reviews_array):
	reviews_content_list = get_reviews_content(reviews_array)
	content_2_grams = []
	for content in reviews_content_list:
		content_2_grams.append(get_2_grams(words=content))
	reviews_len = len(reviews_content_list)
	jd_list = []
	for i in range(0, reviews_len):
		for j in range(i + 1, reviews_len):
			jd_list.append(jaccard_distence(content_2_grams[i], content_2_grams[j]))

	return jd_list

def get_reviews_similarity_relation(jd_list):
	rs_relation_dict = {'0':0, '0.1':0, '0.2':0, '0.3':0, '0.4':0, '0.5':0, '0.6':0, '0.7':0, '0.8':0, '0.9':0, '1':0}
	for jd in jd_list:
		if jd >= 0 and jd < 0.1:
			rs_relation_dict['0'] += 1
		elif jd >= 0.1 and jd < 0.2:
			rs_relation_dict['0.1'] += 1
		elif jd >= 0.2 and jd < 0.3:
			rs_relation_dict['0.2'] += 1
		elif jd >= 0.3 and jd < 0.4:
			rs_relation_dict['0.3'] += 1
		elif jd >= 0.4 and jd < 0.5:
			rs_relation_dict['0.4'] += 1
		elif jd >= 0.5 and jd < 0.6:
			rs_relation_dict['0.5'] += 1
		elif jd >= 0.6 and jd < 0.7:
			rs_relation_dict['0.6'] += 1
		elif jd >= 0.7 and jd < 0.8:
			rs_relation_dict['0.7'] += 1
		elif jd >= 0.8 and jd < 0.9:
			rs_relation_dict['0.8'] += 1
		elif jd >= 0.9 and jd < 1:
			rs_relation_dict['0.9'] += 1
		elif jd ==1:
			rs_relation_dict['1'] += 1		

	return rs_relation_dict

# rs_relation_dict = get_reviews_similarity_relation(get_js_list(reviews_array))
# plot_relation(rs_relation_dict, use_log=False, plot_type='b-', xlabel='Similarity Score', ylabel='Num Pairs')

# print get_reviews_rating_relation(reviews_array)
# print get_reviews_feedbacks_relation(reviews_array)
# print get_reviews_products_relation(reviews_array)
# get_reviews_reviewers_relation(reviews_array)

# plot_relation(get_reviews_reviewers_relation(reviews_array))
# plot_relation(get_reviews_products_relation(reviews_array), xlabel='Num Reviews', ylabel='Num Products')
plot_relation(get_reviews_feedbacks_relation(reviews_array), xlabel='Num Reviews', ylabel='Num Feedbacks')
# plot_percent(get_reviews_rating_relation(reviews_array))

