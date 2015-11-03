# coding:utf-8
import operator
import matplotlib.pyplot as plt
import collections
from sets import Set
from collections import Counter
import re
import file_util
import ast
import time


def get_reviews_reviewers_relation(memberId_list):
	"""
	获取用户和其所发的review之间的关系
	并且统计，每个发送数量下的用户的数量
	例如，用户A，B，C发送了10条，最后统计出来的是发送10条的用户为3
	"""
	c = Counter(e for e in memberId_list)
	d = Counter(c.values())
	return d

def get_reviews_products_relation(productId_list):
	"""
	获取产品数和review数量之间的关系
	"""
	c = Counter(e for e in productId_list)
	d = Counter(c.values())
	return d

def get_reviews_feedbacks_relation(feedback_list):
	"""
	获取review和feedback之间的关系
	为了方便作图，这里进行了排序
	"""
	feedback_list = [float(feedback) for feedback in feedback_list]
	c = Counter(e for e in feedback_list)
	for key in c.keys():
		key = float(key)
	c = collections.OrderedDict(sorted(c.items()))
	return c

def get_reviews_rating_relation(rating_list):
	"""
	获取review和rating之间的关系
	为了方便作图，这里进行了排序
	同时，这里对Y轴的数值进行了调整
	"""
	c = Counter(e for e in rating_list)
	c = collections.OrderedDict(sorted(c.items()))
	values = c.values()
	values = [float(value) for value in values]
	sum_rating_num = sum(values)
	for value in c.values():
		value = value / sum_rating_num
	return c

def get_reviewer_similarity(reviewer_content_dict):
	similarity_list = []
	for reviewer, contents in reviewer_content_dict.iteritems():
		if len(contents) > 1:
			jd_list = get_jd_list(get_2_grams_list(contents))
			if len(jd_list) != 0:
				similarity_list.append(max(jd_list))
	return similarity_list

def save_graph(dict, saveFilename, xlabel='Num Reviews', ylabel='Num Members', use_log=[True,True], plot_type='rx'):
	"""
	作图
	给定的x_list和y_list作图，并根据一定的参数进行修饰
	"""

	x_list = dict.keys()
	y_list = dict.values()

	fig, ax =  plt.subplots()
	if use_log[0]:
		ax.set_xscale('log', basex=10)
	if use_log[1]:
		ax.set_yscale('log', basey=10)
	plt.plot(x_list, y_list, plot_type)
	plt.ylabel(ylabel)
	plt.xlabel(xlabel)
	plt.axis([0, float(max(x_list))*1.2, 0, float(max(y_list))*1.2])
	plt.savefig(saveFilename)

def jaccard_distance(word1_set, words2_set):
	"""
	计算Jaccard distance
	"""
	set_or = word1_set | words2_set
	set_and = word1_set & words2_set
	if len(set_or) == 0:
		return 2
	return float(len(set_and)) / len(set_or)

def get_2_grams(words=""):
	"""
	给定一个文本，将其分割成2-grams的格式
	"""
	words_list = re.findall(r"[\w']+", words)
	# words_list_2 = [words_list[idx] + ' ' + words_list[idx+1] for idx, word in words_list]
	words_list_2 = []
	words_list_len = len(words_list)
	for idx, word in enumerate(words_list):
		if idx != words_list_len - 1:
			words_list_2.append(words_list[idx] + ' ' + words_list[idx + 1])
	return Set(words_list_2)

def get_2_grams_list(content_list):
	return [get_2_grams(content) for content in content_list]

def get_jd_list(content_list_2_grams):
	"""
	对于分割成2-grams格式的文本list，计算两两之间的jaccard distance
	"""
	reviews_len = len(content_list_2_grams)
	jd_list = []
	for i in range(0, reviews_len):
		for j in range(i + 1, reviews_len):
			jd = jaccard_distance(content_list_2_grams[i], content_list_2_grams[j])
			if jd <= 1:
				jd_list.append(jd)

	return jd_list

def get_reviews_similarity_relation(jd_list):
	"""
	判断每个similarity区间内的数量
	"""
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
	rs_relation_dict = collections.OrderedDict(sorted(rs_relation_dict.items()))
	return rs_relation_dict


# rs_relation_dict = get_reviews_similarity_relation(get_jd_list(reviews_array))
# plot_relation(rs_relation_dict, use_log=False, plot_type='b-', xlabel='Similarity Score', ylabel='Num Pairs')

# save_graph(get_reviews_feedbacks_relation(fu.get_feedback_list()), 'reviews_feedbacks.png', xlabel='Num Reviews', ylabel='Num Feedbacks')
# save_graph(get_reviews_rating_relation(fu.get_rating_list()), 'reviews_rating.png', plot_type='b-', use_log=[False, False],  xlabel='Percent of Reviews', ylabel='Rating')
# save_graph(get_reviews_similarity_relation(get_jd_list(fu.get_content_list()[3000:8000])), 'review_similarity.png', use_log=[False, True], plot_type='bo-')

if __name__ == '__main__':
	fu = file_util.FileUtil()
	fu.open_file('../AmazonDataBackup/reviewsNew.txt')
	fu.get_structure()
	save_graph(get_reviews_products_relation(fu.get_productId_list()), 'reviews_products.png', xlabel='Num Reviews', ylabel='Num Products')
	# save_graph(get_reviews_reviewers_relation(fu.get_memberId_list()), 'reviews_reviewers.png')
	# with open("reviewer_similarity_relation_1") as fp:
	# 	line = fp.readline()
	# 	save_graph(collections.OrderedDict(sorted(ast.literal_eval(line).items())), 'reviewer_similarity_relation_1.png', use_log=[False, True], plot_type='ro-')

	# start = time.time()
	# print 'finish get_structure() %s' % (time.time() - start)
	# # start =time.time()
	# content_list = fu.get_content_list()[0:1000]
	# print 'finish get content_list() %s' % (time.time() - start)
	# # start = time.time()
	# content_list_2_grams = get_2_grams_list(content_list)
	# print 'finish get get_2_grams_list() %s' % (time.time() - start)
	# # start = time.time()
	# jd_list = get_jd_list(content_list_2_grams)
	# print len(jd_list)
	# print 'finish get get_jd_list() %s' % (time.time() - start)
	# # start = time.time(1)
	# get_reviews_similarity_relation(jd_list)
	# print 'finish get get_reviews_similarity_relation() %s' % (time.time() - start)
	# reviewer_content_dict = fu.get_reviewer_content_dict()
	# print 'finish get_reviewer_content_dict() %s' % (time.time() - start)
	# reviewer_similarity_list = get_reviewer_similarity(reviewer_content_dict)
	# print 'finish get_reviewer_similarity() %s' % (time.time() - start)
	# reviewer_similarity_relation = get_reviews_similarity_relation(reviewer_similarity_list)
	# with open("reviewer_similarity_relation", "w") as fp:
	# 	fp.write(str(reviewer_similarity_relation))
	# save_graph(get_reviews_similarity_relation(reviewer_similarity_list), 'reviewer_similarity.png', use_log=[False, True], plot_type='bo-')

	# fu.close()