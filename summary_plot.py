# coding:utf-8
import operator
# import matplotlib.pyplot as plt
import collections
from sets import Set
from collections import Counter
import re
import file_util
import ast
import time
import math


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
	# c = collections.OrderedDict(sorted(c.items()))
	# values = c.values()
	# values = [float(value) for value in values]
	# sum_rating_num = sum(values)
	# for value in c.values():
	# 	value = value / sum_rating_num
	return c

def get_reviewer_similarity(reviewer_content_dict):
	similarity_list = []
	for reviewer, contents in reviewer_content_dict.iteritems():
		if len(contents) > 1:
			jd_list = get_jd_list(get_2_grams_list(contents))
			if len(jd_list) != 0:
				similarity_list.append(max(jd_list))
	return similarity_list

def save_graph(dict, saveFilename, xlabel='Num Reviews', ylabel='Num Members', use_log=[True,True], log_base=[10, 10], plot_type='rx', title='', color='red', lw=1):
	"""
	作图
	给定的x_list和y_list作图，并根据一定的参数进行修饰
	"""

	x_list = dict.keys()
	y_list = dict.values()

	fig, ax =  plt.subplots()
	if use_log[0]:
		ax.set_xscale('log', basex=log_base[0])
	if use_log[1]:
		ax.set_yscale('log', basey=log_base[1])
	plt.plot(x_list, y_list, plot_type, linewidth=lw)
	plt.ylabel(ylabel)
	plt.xlabel(xlabel)
	plt.title(title)
	# plt.set_linewidth(lw)
	# plt.axhline(y=10, color='black', alpha=0.5)
	# plt.axhline(y=100, color='black', alpha=0.5)
	# plt.axhline(y=1000, color='black', alpha=0.5)
	# plt.axhline(y=10000, color='black', alpha=0.5)
	# plt.axhline(y=100000, color='black', alpha=0.5)
	# plt.axhline(y=1, color='black', alpha=0.5)
	plt.axis([0, float(max(x_list))*1.1, 1, float(max(y_list))*10])
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
	# rs_relation_dict = {'0.0':0, '0.1':0, '0.2':0, '0.3':0, '0.4':0, '0.5':0, '0.6':0, '0.7':0, '0.8':0, '0.9':0, '1.0':0}
	rs_relation_dict = {}
	for jd in jd_list:
		key = str(math.floor(jd / 0.1) / 10)
		if key not in rs_relation_dict.keys():
			rs_relation_dict[key] = 0
		rs_relation_dict[key] += 1
	rs_relation_dict = collections.OrderedDict(sorted(rs_relation_dict.items()))
	return rs_relation_dict


# rs_relation_dict = get_reviews_similarity_relation(get_jd_list(reviews_array))
# plot_relation(rs_relation_dict, use_log=False, plot_type='b-', xlabel='Similarity Score', ylabel='Num Pairs')

# save_graph(get_reviews_feedbacks_relation(fu.get_feedback_list()), 'reviews_feedbacks.png', xlabel='Num Reviews', ylabel='Num Feedbacks')
# save_graph(get_reviews_similarity_relation(get_jd_list(fu.get_content_list()[3000:8000])), 'review_similarity.png', use_log=[False, True], plot_type='bo-')

if __name__ == '__main__':
	# fu = file_util.FileUtil()
	# final_dict = {}
	# for x in xrange(1,2):
	# 	fu.open_file('../AmazonDataBackup/reviewsNew/reviewsNew' + str(x))
	# 	fu.get_structure()
	# 	count_dict = get_reviews_feedbacks_relation(fu.get_feedback_list())
	# 	for feedback, num in count_dict.iteritems():
	# 		if feedback not in final_dict.keys():
	# 			final_dict[feedback] = 0
	# 		final_dict[feedback] += num

	# print final_dict
	# final_dict = {'5.0': 3360942, '2.0': 316981, '1.0': 482862, '4.0': 1170336, '3.0': 507449}
	# c = collections.OrderedDict(sorted(.items()))
	# c = collections.OrderedDict(sorted(final_dict.items()))
	# values = c.values()
	# values = [float(value) for value in values]
	# sum_rating_num = sum(values)
	# for key in c.keys():
	# 	c[key] = c[key] / sum_rating_num
	# print c
	# c = {}
	# for key, num in {'0.48': 28, '0.49': 18, '0.46': 17, '0.47': 13, '0.44': 16, '0.45': 28, '0.42': 21, '0.43': 21, '0.41': 27, '0.59': 14, '0.58': 31, '0.51': 17, '0.53': 18, '0.52': 14, '0.55': 372, '0.54': 67, '0.57': 121, '0.56': 567, '0.28': 25, '0.29': 23, '0.24': 46, '0.25': 57, '0.26': 177, '0.27': 56, '0.21': 49, '0.22': 37, '0.23': 42, '0.39': 14, '0.38': 12, '0.37': 19, '0.36': 18, '0.35': 32, '0.34': 21, '0.33': 43, '0.32': 31, '0.31': 22, '0.08': 14603, '0.09': 5912, '0.02': 221177775, '0.03': 20649473, '0.01': 1445067969, '0.06': 104486, '0.07': 33403, '0.04': 2269251, '0.05': 408805, '0.82': 1367, '0.83': 527, '0.81': 2634, '0.86': 52, '0.87': 54, '0.84': 148, '0.85': 56, '0.88': 63, '0.89': 117, '0.15': 328, '0.14': 318, '0.17': 122, '0.16': 216, '0.11': 1684, '0.13': 595, '0.12': 998, '0.19': 53, '0.18': 110, '0.99': 80, '0.98': 126, '0.95': 405, '0.94': 962, '0.97': 229, '0.96': 189, '0.91': 383, '0.93': 990, '0.92': 738, '0.9': 213, '0.8': 2002, '1.0': 3852, '0.1': 3511, '0.0': 4360185542, '0.3': 28, '0.2': 85, '0.5': 17, '0.4': 23, '0.7': 44, '0.6': 34, '0.61': 25, '0.62': 37, '0.63': 35, '0.64': 34, '0.65': 25, '0.66': 38, '0.67': 36, '0.68': 37, '0.69': 30, '0.73': 52, '0.72': 43, '0.71': 17, '0.77': 153, '0.76': 31, '0.75': 37, '0.74': 18, '0.79': 1149, '0.78': 442}.iteritems():
	# 	key = float(key)
	# 	key = str(math.floor(key / 0.1) / 10)
	# 	if key not in c.keys():
	# 		c[key] = 0
	# 	c[key] += num
	c = collections.OrderedDict(sorted({'0.9': 4315, '0.8': 7020, '1.0': 3852, '0.1': 7935, '0.0': 6049917219, '0.3': 236, '0.2': 601, '0.5': 1239, '0.4': 212, '0.7': 1986, '0.6': 330}.items()))
	save_graph(c, 'graphs/reviewer_similarity_110000_2.png', use_log=[False, True],  xlabel='Maximum Similarity Score', ylabel='Number of Reviewers', plot_type='k,-')
	# print str(math.floor(0.348473 / 0.1) / 10)
	# print get_reviews_similarity_relation([0.4232,0.123123, 0.986, 0.9999, 0.0])


	# fu = file_util.FileUtil()
	# fu.open_file('../AmazonDataBackup/reviewsNew.txt')
	# fu.get_structure()
	# save_graph(get_reviews_products_relation(fu.get_productId_list()), 'reviews_products.png', xlabel='Num Reviews', ylabel='Num Products')
	# save_graph(get_reviews_rating_relation(fu.get_rating_list()), 'reviews_rating.png', xlabel='Rating', ylabel='NPercent of Reviews')
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