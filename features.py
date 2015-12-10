import numpy as np
from file_util import FileUtil
import datetime
import operator
from dateutil.parser import parse
import re, math
from collections import Counter

def rank_dict(dict, reverse):
	# dict = {'product1': {0: 'March 13, 2004', 2: 'September 23, 2002', 5: 'September 23, 2008'}, 'product2': {1: 'September 21, 2004', 4: 'November 13, 2004', 3: 'November 13, 2002'}}
	# for product, date_list in dict.iteritems():
	# 	for idx, date in date_list.iteritems():
	# 		date_list[idx] = parse(date)
	# print collections.OrderedDict(sorted(dict['product1'].items()))
	rank_list = {}
	for product, date_list in dict.iteritems():
		date_list = sorted(date_list.items(), key=operator.itemgetter(1), reverse=reverse)
		for idx, date in enumerate(date_list):
			rank_list[date[0]] = idx
		# date_list = [ (date[0], idx) for idx, date in enumerate(date_list)]
		# rank_list += date_list


	return rank_list

# WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])

	sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)

	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator

def text_to_vector(text):
	words = text.split(' ')
	# words = WORD.findall(text)
	return Counter(words)


class Feature:
	def __init__(self, old_file, new_file, filename=""):
		if filename:
			self.fu = FileUtil(filename)
			self.fu.get_structure()
		self.old_file = old_file
		self.new_file = new_file
		# self.db = Database(dbname)

	def save_reviewerid(self):
		reviewIds = self.fu.get_memberId_list()
		with open(self.old_file, 'a') as fp:
			review_txt = ""
			for review_id in reviewIds:
				review_txt += review_id + '\n'
			fp.write(review_txt)
		# for review_id  in reviewIds:
			# self.db.insert_into_features({'review_id': review_id})

	def save_f1(self):
		features = self.fu.get_feedback_list()
		review_txt = ""
		with open(self.old_file) as fp:
			for index, line in enumerate(fp.readlines()):
				review_txt += line.replace('\n', '') + '\t' + features[index] + '\n'
		with open(self.new_file + '1', 'w') as fp:
			fp.write(review_txt) 

	def save_f2(self):
		help_features = self.fu.get_help_feedback_list()
		review_txt = ""
		with open(self.old_file + '1') as fp:
			for index, line in enumerate(fp.readlines()):
				review_txt += line.replace('\n', '') + '\t' + help_features[index] + '\n'
		with open(self.new_file + '2', 'w') as fp:
			fp.write(review_txt) 

	def save_f3(self):
		review_txt = ""
		with open(self.old_file + '2') as fp:
			for line in fp.readlines():
				features = line.split('\t')
				if float(features[1]) == 0:
					review_txt += line.replace('\n', '') + '\t' + '0.0\n'
				else:
					review_txt += line.replace('\n', '') + '\t' + str(float(features[2])/float(features[1])) + '\n'
		with open(self.new_file + '3', 'w') as fp:
			fp.write(review_txt) 

	def save_f4(self):
		title_list = self.fu.get_title_list()
		review_txt = ""
		with open(self.old_file + '3') as fp:
			for index, line in enumerate(fp.readlines()):
				review_txt += line.replace('\n', '') + '\t' + str(len(title_list[index].split(' '))) + '\n'
		with open(self.new_file + '4', 'w') as fp:
			fp.write(review_txt) 

	def save_f5(self):
		content_list = self.fu.get_content_list()
		review_txt = ""
		with open(self.old_file + '4') as fp:
			for index, line in enumerate(fp.readlines()):
				review_txt += line.replace('\n', '') + '\t' + str(len(content_list[index].split(' '))) + '\n'
		with open(self.new_file + '5', 'w') as fp:
			fp.write(review_txt) 

	def save_f6(self):
		reviewer_product_date_list = self.fu.get_column_list([1,2])
		review_txt = ""
		dict = {}
		for idx, reviewer_product_date in enumerate(reviewer_product_date_list):
			product = reviewer_product_date[0]
			date = reviewer_product_date[1]
			if product not in dict:
				dict[product] = {}
			try:
				dict[product][idx] = parse(date)
			except:
				print date
		rank_list = rank_dict(dict, False)
		with open(self.old_file + '5') as fp:
			for index, line in enumerate(fp.readlines()):
				review_txt += line.replace('\n', '') + '\t' + str(rank_list[index] + 1) + '\n'
		with open(self.new_file + '6', 'w') as fp:
			fp.write(review_txt) 

	def save_f7(self):
		reviewer_product_date_list = self.fu.get_column_list([1,2])
		review_txt = ""
		dict = {}
		for idx, reviewer_product_date in enumerate(reviewer_product_date_list):
			product = reviewer_product_date[0]
			date = reviewer_product_date[1]
			if product not in dict:
				dict[product] = {}
			try:
				dict[product][idx] = parse(date)
			except:
				print date
		rank_list = rank_dict(dict, True)
		# with open('review_product_rank', 'w') as fp:
		# 	fp.write(str(dict))
		with open(self.old_file + '6') as fp:
			for index, line in enumerate(fp.readlines()):
				review_txt += line.replace('\n', '') + '\t' + str(rank_list[index] + 1) + '\n'
		with open(self.new_file + '7', 'w') as fp:
			fp.write(review_txt) 

	def save_f8(self):
		review_txt = ""
		with open(self.old_file + '7') as fp:
			for index, line in enumerate(fp.readlines()):
				if line.split('\t')[6] == '1': 
					review_txt += line.replace('\n', '') + '\t' + '1\n'
				else:
					review_txt += line.replace('\n', '') + '\t' + '0\n'
		with open(self.new_file + '8', 'w') as fp:
			fp.write(review_txt) 

	def save_f9(self):
		review_txt = ""
		with open(self.old_file + '8') as fp:
			for index, line in enumerate(fp.readlines()):
				if line.split('\t')[6] == '1' and line.split('\t')[7] == '1': 
					review_txt += line.replace('\n', '') + '\t' + '1\n'
				else:
					review_txt += line.replace('\n', '') + '\t' + '0\n'
		with open(self.new_file + '9', 'w') as fp:
			fp.write(review_txt)

	def save_f10(self):
		review_txt = ""
		content_list = self.fu.get_content_list()
		positive_words = []
		with open('../opinion-lexicon-English/positive-words.txt') as fp:
			positive_words = [word for word in fp.readlines()]
		with open(self.old_file + '9') as fp:
			for index, line in enumerate(fp.readlines()):
				content = content_list[index].split(' ')
				content_len = len(content)
				positive_len = 0.0
				for word in content:
					if word.lower() in positive_words:
						positive_len += 1
						print positive_len
				review_txt += line.replace('\n', '') + '\t' + str(positive_len / content_len) +'\n'
		with open(self.new_file + '10', 'w') as fp:
			fp.write(review_txt)

	def save_f11(self):
		review_txt = ""
		content_list = self.fu.get_content_list()
		negative_words = []
		with open('../opinion-lexicon-English/negative-words.txt') as fp:
			negative_words = [word for word in fp.readlines()]
		print len(negative_words)
		with open(self.old_file + '10') as fp:
			for index, line in enumerate(fp.readlines()):
				content = content_list[index].split(' ')
				content_len = len(content)
				negative_len = 0.0
				for word in content:
					if word.lower() in negative_words:
						negative_len += 1
						print negative_len
				review_txt += line.replace('\n', '') + '\t' + str(negative_len / content_len) +'\n'
		with open(self.new_file + '11', 'w') as fp:
			fp.write(review_txt)

	def save_f12(self):
		review_txt = ""
		product_content_list = self.fu.get_column_list([1,7])
		product_feature_list = {}
		with open('../AmazonDataBackup/productInfoXML-reviewed-mProducts.features') as fp:
			for line in fp:
				product_id = line.split('\t')[0]
				product_feature = line.split('\t')[1]
				product_feature_list[product_id] = product_feature
		with open(self.old_file + '11') as fp:
			for index, line in enumerate(fp.readlines()):
				product_id = product_content_list[index][0]
				content = product_content_list[index][1].lower()
				product_feature = product_feature_list[product_id]
				cos_sim = get_cosine(text_to_vector(content), text_to_vector(product_feature))
				review_txt += line.replace('\n', '') + '\t' + str(cos_sim) +'\n'
		with open(self.new_file + '12', 'w') as fp:
			fp.write(review_txt)

if __name__ == "__main__":
	fea = Feature('../AmazonDataBackup/reviewsNew/reviews.features', '../AmazonDataBackup/reviewsNew/reviews.features' ,filename='../AmazonDataBackup/reviewsNew/reviewsNew.mp')
	# fea.save_reviewerid()
	# fea.save_f1()
	# fea.save_f2()
	# fea.save_f3()
	# fea.save_f4()
	# fea.save_f5()
	# fea.save_f6()
	# fea.save_f7()
	# fea.save_f8()
	# fea.save_f9()
	# fea.save_f10()
	# fea.save_f11()
	fea.save_f12()


	