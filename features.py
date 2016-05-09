# import numpy as np
from file_util import FileUtil
import datetime
import operator
from dateutil.parser import parse
import re, math
from collections import Counter
from summary_plot import jaccard_distance, get_2_grams

def rank_dict(dict, reverse):
	# dict = {'product1': {0: 'March 13, 2004', 2: 'September 23, 2002', 5: 'September 23, 2008'}, 'product2': {1: 'September 21, 2004', 4: 'November 13, 2004', 3: 'November 13, 2002'}}
	# for product, date_list in dict.iteritems():
	# 	for idx, date in date_list.iteritems():
	# 		date_list[idx] = parse(date)
	# print collections.OrderedDict(sorted(dict['product1'].items()))
	rank_list = {}
	for product, date_list in dict.iteritems():
		date_list = sorted(date_list.items(), key=operator.itemgetter(1), reverse=reverse)
		try:
			rank_list[product]
		except:
			rank_list[product] = {}
		for idx, date in enumerate(date_list):
			rank_list[product][date[0]] = idx

	return rank_list

WORD = re.compile(r'\w+')

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

def text_to_vector(text, format=r'\w+'):
	# words = text.split(' ')
	word_format = re.compile(format)
	words = word_format.findall(text)
	return Counter(words)

def product_brand_dict(file_name):
	product_brand_dict = {}
	with open(file_name) as fp:
		for line in fp.readlines():
			product_info = line.split('\t')
			product_brand_dict[product_info[0]] = product_info[2]
	return product_brand_dict

def product_price_dict(file_name):
	product_price_dict = {}
	with open(file_name) as fp:
		for line in fp.readlines():
			product_info = line.split('\t')
			product_price_dict[product_info[0]] = product_info[3]
	return product_price_dict

def product_rank_dict(file_name):
	product_rank_dict = {}
	with open(file_name) as fp:
		for line in fp.readlines():
			product_info = line.split('\t')
			product_rank_dict[product_info[0]] = product_info[1]
	return product_rank_dict

def product_avg_rating(product_rating_list):
	dict = {}
	dict_2 = {}
	for item in product_rating_list:
		product_id = item[0]
		rating = item[1]
		try:
			dict[product_id] += 1
			dict_2[product_id] += float(rating)
		except:
			dict[product_id] = 1
			dict_2[product_id] = float(rating)
			
	for key in dict.keys():
		dict_2[key] = dict_2[key] / dict[key]
	return dict_2

def all_same(items):
    return all(x == items[0] for x in items)

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
				review_txt += line.replace('\n', '') + '\t' + str(rank_list[product][index] + 1) + '\n'
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
				review_txt += line.replace('\n', '') + '\t' + str(rank_list[product][index] + 1) + '\n'
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
		product_content_list = self.fu.get_column_list([1,-1])
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

	def save_f13(self):
		review_txt = ""
		product_content_list = self.fu.get_column_list([1,-1])
		p_b_dict = product_brand_dict('../AmazonDataBackup/productInfoXML-reviewed-mProducts.copy')
		
		with open(self.old_file + '12') as fp:
			for index, line in enumerate(fp.readlines()):
				product_id = product_content_list[index][0]
				content = product_content_list[index][1].lower()
				content = WORD.findall(content)
				counted_content = Counter(content)
				brand = p_b_dict[product_id]
				try:
					brand_num = counted_content[brand]
					review_txt += line.replace('\n', '') + '\t' + str(float(brand_num) / len(content)) +'\n'
				except:
					brand_num = 0
					review_txt += line.replace('\n', '') + '\t' + '0\n'
				
		with open(self.new_file + '13', 'w') as fp:
			fp.write(review_txt)

	def save_f14(self):
		review_txt = ""
		content_list = self.fu.get_content_list()
		format = re.compile(r'\d+')
		with open(self.old_file + '13') as fp:
			for index, line in enumerate(fp.readlines()):
				content = content_list[index]
				number = len(format.findall(content))
				content = re.compile(r'\w+').findall(content)
				if len(content):
					review_txt += line.replace('\n', '') + '\t' + str(float(number) / len(content)) +'\n'
				else:
					review_txt += line.replace('\n', '') + '\t' + '0\n'
				
		with open(self.new_file + '14', 'w') as fp:
			fp.write(review_txt)

	def save_f15(self):
		review_txt = ""
		content_list = self.fu.get_content_list()
		with open(self.old_file + '14') as fp:
			for index, line in enumerate(fp.readlines()):
				content = content_list[index]
				capital_num = sum(1 for c in content if c.isupper())
				content = re.compile(r'\w+').findall(content)
				if len(content):
					review_txt += line.replace('\n', '') + '\t' + str(float(capital_num) / len(content)) +'\n'
				else:
					review_txt += line.replace('\n', '') + '\t' + '0\n'
				
		with open(self.new_file + '15', 'w') as fp:
			fp.write(review_txt)

	def save_f16(self):
		review_txt = ""
		content_list = self.fu.get_content_list()
		with open(self.old_file + '15') as fp:
			for index, line in enumerate(fp.readlines()):
				content = re.compile(r'\w+').findall(content_list[index])
				capital_num = sum(1 for c in content if c.isupper())
				# content = re.compile(r'\w+').findall(content)
				if len(content):
					review_txt += line.replace('\n', '') + '\t' + str(float(capital_num) / len(content)) +'\n'
				else:
					review_txt += line.replace('\n', '') + '\t' + '0\n'
				
		with open(self.new_file + '16', 'w') as fp:
			fp.write(review_txt)

	def save_f17(self):
		review_txt = ""
		rating_list = self.fu.get_rating_list()
		with open(self.old_file + '16') as fp:
			for index, line in enumerate(fp.readlines()):
				review_txt += line.replace('\n', '') + '\t' + str(rating_list[index]) +'\n'
				
		with open(self.new_file + '17', 'w') as fp:
			fp.write(review_txt)

	def save_f18(self):
		review_txt = ""
		product_rating_list = self.fu.get_column_list([1, 5])
		product_avg_rating_dict = product_avg_rating(product_rating_list)
		with open(self.old_file + '17') as fp:
			for index, line in enumerate(fp.readlines()):
				product_id = product_rating_list[index][0]
				rating = product_rating_list[index][1]
				review_txt += line.replace('\n', '') + '\t' + str(float(rating) - product_avg_rating_dict[product_id]) +'\n'
				
		with open(self.new_file + '18', 'w') as fp:
			fp.write(review_txt)

	def save_f19(self):
		review_txt = ""
		rating_list = self.fu.get_rating_list()
		with open(self.old_file + '18') as fp:
			for index, line in enumerate(fp.readlines()):
				try:
					rating = float(rating_list[index])
					if rating >= 4:
						review_txt += line.replace('\n', '') + '\t' + '1\n'
					elif rating <= 2.5:
						review_txt += line.replace('\n', '') + '\t' + '-1\n'
					else:
						review_txt += line.replace('\n', '') + '\t' + '0\n'
				except:
					print index
				
		with open(self.new_file + '19', 'w') as fp:
			fp.write(review_txt)

	def save_f20(self):
		review_txt = ""
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
		with open(self.old_file + '19') as fp:
			features = fp.readlines()
			for index, line in enumerate(features):
				product_id = reviewer_product_date_list[index][0]
				rank = rank_list[product_id][index]
				rating_type = int(line.split('\t')[19])
				if rank == 1 and rating_type == -1:
					# print rank_list[product_id]
					# print rank_list[product_id]
					# print index
					first_review_index = 0
					for review in rank_list[product_id].keys():
						if rank_list[product_id][review] == 0:
							first_review_index = review
					if int(features[first_review_index].split('\t')[19]) == 1:
						print index, first_review_index
						review_txt += line.replace('\n', '') + '\t' + '1\n'
					else:
						review_txt += line.replace('\n', '') + '\t' + '0\n'
				else:
					review_txt += line.replace('\n', '') + '\t' + '0\n'

				
		with open(self.new_file + '20', 'w') as fp:
			fp.write(review_txt)

	def save_f21(self):
		review_txt = ""
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
		with open(self.old_file + '20') as fp:
			features = fp.readlines()
			for index, line in enumerate(features):
				product_id = reviewer_product_date_list[index][0]
				rank = rank_list[product_id][index]
				rating_type = int(line.split('\t')[19])
				if rank == 1 and rating_type == 1:
					# print rank_list[product_id]
					# print rank_list[product_id]
					# print index
					first_review_index = 0
					for review in rank_list[product_id].keys():
						if rank_list[product_id][review] == 0:
							first_review_index = review
					if int(features[first_review_index].split('\t')[19]) == -1:
						print index, first_review_index
						review_txt += line.replace('\n', '') + '\t' + '1\n'
					else:
						review_txt += line.replace('\n', '') + '\t' + '0\n'
				else:
					review_txt += line.replace('\n', '') + '\t' + '0\n'

				
		with open(self.new_file + '21', 'w') as fp:
			fp.write(review_txt)

	def save_f22(self):
		review_txt = ""
		
		with open(self.old_file + '21') as fp:
			reviewers = {}
			lines = fp.readlines()
			for line in lines:
				features = line.split('\t')
				if not reviewers.has_key(features[0]):
					reviewers[features[0]] = {'review_num': 0, 'first_review_num': 0.0}
				if int(features[8]) == 1:
					reviewers[features[0]]['first_review_num'] += 1
				reviewers[features[0]]['review_num'] += 1
			# features = [line.split('\t') for line in lines]
			print 'finish features'
			for index, line in enumerate(lines):
				features = line.split('\t')
				review_id = features[0]
				review_num = reviewers[review_id]['review_num']
				first_review_num = reviewers[review_id]['first_review_num']
				if first_review_num > 0 and first_review_num != review_num:
					print index, first_review_num
				review_txt += lines[index].replace('\n', '') + '\t' + str(first_review_num / review_num) +'\n'

				
		with open(self.new_file + '22', 'w') as fp:
			fp.write(review_txt)

	def save_f23(self):
		review_txt = ""
		
		with open(self.old_file + '22') as fp:
			reviewers = {}
			lines = fp.readlines()
			for line in lines:
				features = line.split('\t')
				if not reviewers.has_key(features[0]):
					reviewers[features[0]] = {'review_num': 0, 'only_review_num': 0.0}
				if int(features[9]) == 1:
					reviewers[features[0]]['only_review_num'] += 1
				reviewers[features[0]]['review_num'] += 1
			# features = [line.split('\t') for line in lines]
			print 'finish features'
			for index, line in enumerate(lines):
				features = line.split('\t')
				review_id = features[0]
				review_num = reviewers[review_id]['review_num']
				only_review_num = reviewers[review_id]['only_review_num']
				if only_review_num > 0 and only_review_num != review_num:
					print index, only_review_num
				review_txt += lines[index].replace('\n', '') + '\t' + str(only_review_num / review_num) +'\n'

				
		with open(self.new_file + '23', 'w') as fp:
			fp.write(review_txt)

	def save_f24(self):
		review_txt = ""
		reviewer_rating_list = self.fu.get_column_list([0,5])
		reviewers = {}
		for reviewer_rating in reviewer_rating_list:
			reviewer_id = reviewer_rating[0]
			rating = reviewer_rating[1]
			if not reviewers.has_key(reviewer_id):
				reviewers[reviewer_id] = {'ratings': [], 'avg_rating': 0.0}
			reviewers[reviewer_id]['ratings'].append(float(rating))

		for reviewer_id in reviewers.keys():
			ratings = reviewers[reviewer_id]['ratings']
			reviewers[reviewer_id]['avg_rating'] = sum(ratings) / len(ratings)

		with open(self.old_file + '23') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				features = line.split('\t')
				reviewer_id = features[0]
				review_txt += lines[index].replace('\n', '') + '\t' + str(reviewers[reviewer_id]['avg_rating']) +'\n'

				
		with open(self.new_file + '24', 'w') as fp:
			fp.write(review_txt)

	def save_f25(self):
		review_txt = ""
		reviewer_rating_list = self.fu.get_column_list([0,5])
		reviewers = {}
		for reviewer_rating in reviewer_rating_list:
			reviewer_id = reviewer_rating[0]
			rating = reviewer_rating[1]
			if not reviewers.has_key(reviewer_id):
				reviewers[reviewer_id] = {'ratings': [], 'avg_rating': 0.0, 'std_rating': 0.0}
			reviewers[reviewer_id]['ratings'].append(float(rating))

		for reviewer_id in reviewers.keys():
			ratings = reviewers[reviewer_id]['ratings']
			reviewers[reviewer_id]['avg_rating'] = sum(ratings) / len(ratings)
			

		for reviewer_id in reviewers.keys():
			ratings = reviewers[reviewer_id]['ratings']
			avg_rating = reviewers[reviewer_id]['avg_rating']
			std_rating = math.sqrt(sum([ (rating - avg_rating)**2 for rating in ratings ]))
			reviewers[reviewer_id]['std_rating'] = std_rating

		with open(self.old_file + '24') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				features = line.split('\t')
				reviewer_id = features[0]
				review_txt += lines[index].replace('\n', '') + '\t' + str(reviewers[reviewer_id]['std_rating']) +'\n'

				
		with open(self.new_file + '25', 'w') as fp:
			fp.write(review_txt)

	def save_f26(self):
		review_txt = ""
		reviewer_rating_list = self.fu.get_column_list([0,5])
		reviewers = {}
		for reviewer_rating in reviewer_rating_list:
			reviewer_id = reviewer_rating[0]
			rating = float(reviewer_rating[1])
			if not reviewers.has_key(reviewer_id):
				reviewers[reviewer_id] = []
			rating_flag = 1
			if rating >= 4:
				rating_flag = 1
			elif rating < 2.5:
				rating_flag = -1
			else:
				rating_flag = 0
			reviewers[reviewer_id].append(rating_flag)

		with open(self.old_file + '25') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				features = line.split('\t')
				reviewer_id = features[0]
				if all_same(reviewers[reviewer_id]):
					review_txt += lines[index].replace('\n', '') + '\t' +'1\n'
				else:
					review_txt += lines[index].replace('\n', '') + '\t' +'0\n'

				
		with open(self.new_file + '26', 'w') as fp:
			fp.write(review_txt)

	def save_f27(self):
		review_txt = ""
		reviewer_rating_list = self.fu.get_column_list([0,5])
		reviewers = {}
		for reviewer_rating in reviewer_rating_list:
			reviewer_id = reviewer_rating[0]
			rating = float(reviewer_rating[1])
			if not reviewers.has_key(reviewer_id):
				reviewers[reviewer_id] = {'good': False, 'avg': False, 'bad': False}
			if rating >= 4:
				reviewers[reviewer_id]['good'] = True
			elif rating < 2.5:
				reviewers[reviewer_id]['bad'] = True
			else:
				reviewers[reviewer_id]['avg'] = True
			

		with open(self.old_file + '26') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				features = line.split('\t')
				reviewer_id = features[0]
				if reviewers[reviewer_id]['good'] and reviewers[reviewer_id]['bad'] and not reviewers[reviewer_id]['avg']:
					print index
					review_txt += lines[index].replace('\n', '') + '\t' +'1\n'
				else:
					review_txt += lines[index].replace('\n', '') + '\t' +'0\n'

				
		with open(self.new_file + '27', 'w') as fp:
			fp.write(review_txt)

	def save_f28(self):
		review_txt = ""
		reviewer_rating_list = self.fu.get_column_list([0,5])
		reviewers = {}
		for reviewer_rating in reviewer_rating_list:
			reviewer_id = reviewer_rating[0]
			rating = float(reviewer_rating[1])
			if not reviewers.has_key(reviewer_id):
				reviewers[reviewer_id] = {'good': False, 'avg': False, 'bad': False}
			if rating >= 4:
				reviewers[reviewer_id]['good'] = True
			elif rating < 2.5:
				reviewers[reviewer_id]['bad'] = True
			else:
				reviewers[reviewer_id]['avg'] = True
			

		with open(self.old_file + '27') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				features = line.split('\t')
				reviewer_id = features[0]
				if reviewers[reviewer_id]['good'] and reviewers[reviewer_id]['avg'] and not reviewers[reviewer_id]['bad']:
					print index
					review_txt += lines[index].replace('\n', '') + '\t' +'1\n'
				else:
					review_txt += lines[index].replace('\n', '') + '\t' +'0\n'

				
		with open(self.new_file + '28', 'w') as fp:
			fp.write(review_txt)

	def save_f29(self):
		review_txt = ""
		reviewer_rating_list = self.fu.get_column_list([0,5])
		reviewers = {}
		for reviewer_rating in reviewer_rating_list:
			reviewer_id = reviewer_rating[0]
			rating = float(reviewer_rating[1])
			if not reviewers.has_key(reviewer_id):
				reviewers[reviewer_id] = {'good': False, 'avg': False, 'bad': False}
			if rating >= 4:
				reviewers[reviewer_id]['good'] = True
			elif rating < 2.5:
				reviewers[reviewer_id]['bad'] = True
			else:
				reviewers[reviewer_id]['avg'] = True
			

		with open(self.old_file + '28') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				features = line.split('\t')
				reviewer_id = features[0]
				if reviewers[reviewer_id]['bad'] and reviewers[reviewer_id]['avg'] and not reviewers[reviewer_id]['good']:
					print index
					review_txt += lines[index].replace('\n', '') + '\t' +'1\n'
				else:
					review_txt += lines[index].replace('\n', '') + '\t' +'0\n'

				
		with open(self.new_file + '29', 'w') as fp:
			fp.write(review_txt)

	def save_f30(self):
		review_txt = ""
		reviewer_rating_list = self.fu.get_column_list([0,5])
		reviewers = {}
		for reviewer_rating in reviewer_rating_list:
			reviewer_id = reviewer_rating[0]
			rating = float(reviewer_rating[1])
			if not reviewers.has_key(reviewer_id):
				reviewers[reviewer_id] = {'good': False, 'avg': False, 'bad': False}
			if rating >= 4:
				reviewers[reviewer_id]['good'] = True
			elif rating < 2.5:
				reviewers[reviewer_id]['bad'] = True
			else:
				reviewers[reviewer_id]['avg'] = True
			

		with open(self.old_file + '29') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				features = line.split('\t')
				reviewer_id = features[0]
				if reviewers[reviewer_id]['bad'] and reviewers[reviewer_id]['avg'] and reviewers[reviewer_id]['good']:
					print index
					review_txt += lines[index].replace('\n', '') + '\t' +'1\n'
				else:
					review_txt += lines[index].replace('\n', '') + '\t' +'0\n'

				
		with open(self.new_file + '30', 'w') as fp:
			fp.write(review_txt)

	def save_f31(self):
		review_txt = ""
		reviewers = {}
		with open(self.old_file + '30') as fp:
			for features in fp.readlines():
				features = features.split('\t')
				reviewer_id = features[0]
				if not reviewers.has_key(reviewer_id):
					reviewers[reviewer_id] = {'total': 0.0, 'first': 0.0}
				reviewers[reviewer_id]['total'] += 1
				if int(features[20]):
					reviewers[reviewer_id]['first'] += 1


		with open(self.old_file + '30') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				features = line.split('\t')
				reviewer_id = features[0]
				review_txt += lines[index].replace('\n', '') + '\t' + str(reviewers[reviewer_id]['first'] / reviewers[reviewer_id]['total']) +'\n'
				if reviewers[reviewer_id]['first'] and reviewers[reviewer_id]['first'] != 1:
					print index 
				
		with open(self.new_file + '31', 'w') as fp:
			fp.write(review_txt)

	def save_f32(self):
		review_txt = ""
		reviewers = {}
		with open(self.old_file + '31') as fp:
			for features in fp.readlines():
				features = features.split('\t')
				reviewer_id = features[0]
				if not reviewers.has_key(reviewer_id):
					reviewers[reviewer_id] = {'total': 0.0, 'first': 0.0}
				reviewers[reviewer_id]['total'] += 1
				if int(features[21]):
					reviewers[reviewer_id]['first'] += 1


		with open(self.old_file + '31') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				features = line.split('\t')
				reviewer_id = features[0]
				review_txt += lines[index].replace('\n', '') + '\t' + str(reviewers[reviewer_id]['first'] / reviewers[reviewer_id]['total']) +'\n'
				if reviewers[reviewer_id]['first'] and reviewers[reviewer_id]['first'] != 1:
					print index 
				
		with open(self.new_file + '32', 'w') as fp:
			fp.write(review_txt)

	def save_f33(self):
		review_txt = ""
		product_price = product_price_dict('../AmazonDataBackup/productInfoXML-reviewed-mProducts.copy')
		product_list = self.fu.get_productId_list()
		with open(self.old_file + '32') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				product_id = product_list[index]
				review_txt += lines[index].replace('\n', '') + '\t' + str(product_price[product_id]) +'\n'
				
		with open(self.new_file + '33', 'w') as fp:
			fp.write(review_txt)

	def save_f34(self):
		review_txt = ""
		product_rank = product_rank_dict('../AmazonDataBackup/productInfoXML-reviewed-mProducts.copy')
		product_list = self.fu.get_productId_list()
		with open(self.old_file + '33') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				product_id = product_list[index]
				review_txt += lines[index].replace('\n', '') + '\t' + str(product_rank[product_id]) +'\n'
				
		with open(self.new_file + '34', 'w') as fp:
			fp.write(review_txt)

	def save_f35(self):
		review_txt = ""
		product_list = self.fu.get_productId_list()
		product_rank = product_rank_dict('../AmazonDataBackup/productInfoXML-reviewed-mProducts.copy')
		product_rating_list = self.fu.get_column_list([1, 5])
		products = {}
		for product_rating in product_rating_list:
			product_id = product_rating[0]
			rating = float(product_rating[1])
			if not products.has_key(product_id):
				products[product_id] = {'ratings': [], 'avg': 0.0}
			products[product_id]['ratings'].append(rating)

		for product_id in products.keys():
			products[product_id]['avg'] = sum(products[product_id]['ratings']) / len(products[product_id]['ratings'])

		with open(self.old_file + '34') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				product_id = product_list[index]
				review_txt += lines[index].replace('\n', '') + '\t' + str(products[product_id]['avg']) +'\n'

				if index == 0:
					print products[product_id]
				
		with open(self.new_file + '35', 'w') as fp:
			fp.write(review_txt)

	def save_f36(self):
		review_txt = ""
		product_list = self.fu.get_productId_list()
		product_rank = product_rank_dict('../AmazonDataBackup/productInfoXML-reviewed-mProducts.copy')
		product_rating_list = self.fu.get_column_list([1, 5])
		products = {}
		for product_rating in product_rating_list:
			product_id = product_rating[0]
			rating = float(product_rating[1])
			if not products.has_key(product_id):
				products[product_id] = {'ratings': [], 'avg': 0.0, 'std': 0.0}
			products[product_id]['ratings'].append(rating)

		for product_id in products.keys():
			products[product_id]['avg'] = sum(products[product_id]['ratings']) / len(products[product_id]['ratings'])

		for product_id in products.keys():
			avg = products[product_id]['avg']
			std = math.sqrt(sum([(rating - avg)**2 for rating in products[product_id]['ratings']]))
			products[product_id]['std'] = std

		with open(self.old_file + '35') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				product_id = product_list[index]
				review_txt += lines[index].replace('\n', '') + '\t' + str(products[product_id]['std']) +'\n'

				if index == 0:
					print products[product_id]
				
		with open(self.new_file + '36', 'w') as fp:
			fp.write(review_txt)

	def save_labels(self):
		review_txt = ""
		content_list = self.fu.get_content_list()
		print 'get content list'
		grams_list = []
		for content in content_list:
			grams_list.append(get_2_grams(content))
		print 'get grams list'
		label_list = []
		content_len = len(content_list)
		for x in xrange(0,content_len):
			label_list.append(0)
		print 'start labeling'
		for i in xrange(0,content_len):
			grams_a = grams_list[i]
			for j in xrange(i+1,content_len):
				grams_b = grams_list[j]
				sim = jaccard_distance(grams_a, grams_b)
				if sim >= 0.9:
					print "sim is : " , sim
					label_list[i] = 1
					label_list[j] = 1
		with open(self.old_file + '36') as fp:
			lines = fp.readlines()
			for index, line in enumerate(lines):
				product_id = product_list[index]
				review_txt += lines[index].replace('\n', '') + '\t' + str(label_list[index]) +'\n'
				
		with open(self.new_file + '37', 'w') as fp:
			fp.write(review_txt)

if __name__ == "__main__":
	fea = Feature('../AmazonDataBackup/reviewsNew/reviews.features', '../AmazonDataBackup/reviewsNew/reviews.features', filename='../AmazonDataBackup/reviewsNew/reviewsNew.mp')
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
	# fea.save_f12()
	# fea.save_f13()
	# fea.save_f14()
	# fea.save_f15()
	# fea.save_f16()
	# fea.save_f17()
	# fea.save_f18()
	# fea.save_f19()
	# fea.save_f20()
	# fea.save_f21()
	# fea.save_f22()
	# fea.save_f23()
	# fea.save_f24()
	# fea.save_f25()
	# fea.save_f26()
	# fea.save_f27()
	# fea.save_f28()
	# fea.save_f29()
	# fea.save_f30()
	# fea.save_f31()
	# fea.save_f32()
	# fea.save_f33()
	# fea.save_f34()
	# fea.save_f35()
	# fea.save_f36()
	# fea.save_labels()
