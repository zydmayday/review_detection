import os
import numpy as ntpath
from pandas import Series, DataFrame
import pandas as pd
import nltk
import operator
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

class PreProcessWithPandas():
	def __init__(self, file_name=None):
		if file_name:
			self.data = self.load_file(file_name)
			# self.data = self.data.apply(lambda row: nltk.word_tokenize(row['Body']), axis=1)

	def load_file(self, file_name):
		return pd.read_csv(file_name, nrows=5)

	def word_count(self, by='Body'):
		# bodies = self.data.apply(lambda row: nltk.word_tokenize(row[by]), axis=1)
		# def lower_zyd(row):
		# 	return [x.lower() for x in row]
		# bodies = bodies.apply(lower_zyd)
		corpus = []
		for b in self.data[by]:
			corpus.append(b)
		corpus = [''.join(corpus)]
		# corpus = ''.join(corpus)
		# counts = Counter(corpus)
		# print counts
		tf = CountVectorizer(analyzer='word', min_df=0, stop_words='english')
		counts = tf.fit_transform(corpus)
		feature_names = tf.get_feature_names()
		matrix = dict(zip(feature_names, counts.toarray()[0]))
		sorted_x = sorted(matrix.items(), key=operator.itemgetter(1), reverse=True)
		print sorted_x

	def tf_idf(self, by='Body'):
		corpus = []
		for body in self.data[by]:
			corpus.append(body)
		corpus = [''.join(corpus)]
		print corpus
		tf = TfidfVectorizer(analyzer='word', min_df=0, stop_words='english')
		tfidf_matrix = tf.fit_transform(corpus)
		feature_names = tf.get_feature_names()
		# tf_idf = self.data.apply(lambda row: nltk.word_tokenize(row[by]), axis=1)
		return tfidf_matrix, feature_names

	def test(self):
		corpus = []
		a = 'The game of life is a game of everlasting learning'
		b = 'The unexamined life is not worth living'
		c = 'Never stop learning'
		corpus.append(a)
		corpus.append(b)
		corpus.append(c)
		# tf = TfidfVectorizer(analyzer='word', min_df=0, stop_words='english')
		tf = CountVectorizer(analyzer='word', min_df=0, stop_words='english')
		tfidf_matrix = tf.fit_transform(corpus)
		feature_names = tf.get_feature_names()
		return tfidf_matrix, feature_names
class PreProcessForTxt():

	def get_file_line(self, file_name):

		non_blank_count = 0

		with open(file_name) as infp:
			for line in infp.readlines():
				# if line.startswith(' ') or 'BREAK-REVIEWED' in line:
				non_blank_count += 1

		return non_blank_count

	def get_pure_file(self, file_name, to_file):
		file_txt = ''
		with open(file_name) as fp:
			for line in fp:
				if 'BREAK-REVIEWED' in line:
					pass
				else:
					file_txt += line
		with open(to_file, 'w') as tf:
			tf.write(file_txt)

	def get_product_features_file(self, file_name, to_file):
		file_txt = ''
		with open(file_name) as fp:
			for idx, line in enumerate(fp):
				contents = line.split('\t')
				if idx % 2:
					for content in contents:
						if 'Feature' in content and '->' in content:
							file_txt += content.split('->')[1].lower() + ' '
					file_txt += '\n'
				else:
					file_txt += contents[0] + '\t'

		with open(to_file, 'w') as fp:
			fp.write(file_txt)

	def get_mp_file(self, file_name, to_file):
		file_txt = ''
		with open(file_name) as fp:
			for line in fp:
				productinfo = line.split('\t')
				if len(productinfo) < 2:
					continue
				type = productinfo[2]
				product_id = productinfo[0]
				if not ("Books" in type or "Music" in type or "DVD" in type):
	 				if product_id.startswith(' '):
						file_txt += line
		with open(to_file, 'w') as tf:
			tf.write(file_txt)

	def get_product_array(self, file_name):
		product_array = []
		with open(file_name) as fp:
			for line in fp:
				product_array.append(line.split('\t')[0])
		return product_array

	def get_reviewer_array(self, file_name):
		reviewer_array = []
		with open(file_name) as fp:
			for line in fp:
				reviewer_array.append(line.split('\t')[0])
		return set(reviewer_array)

	def get_mP_reviews(self, file_name, product_array):
		reviews = ''
		with open(file_name) as fp:
			for line in fp:
				if line.split('\t')[1] in product_array:
					reviews += line
		fp2 = open(file_name + '.mP', 'w')
		print 'finish writing ' + file_name + '.copy'
		fp2.write(reviews)
		fp2.close()


	def write_txt_to_file(self, f, newfile, line_num):
		file_txt = ''
		flag = 1
		for i in xrange(0,line_num):
			line = f.readline()
			if line:
				file_txt += line
			else:
				flag = -1
		with open(newfile, 'w') as nf:
			print nf.name
			nf.write(file_txt)
		return flag

	def split_file(self, file_name, line_num):
		dir_name = file_name.split('.')[0]
		if not os.path.exists(dir_name):
			os.mkdir(dir_name)
		count = 1
		with open(file_name) as f:
			while True:
				status = write_txt_to_file(f, dir_name + '/' + dir_name + str(count), line_num)
				if status == -1:
					break
				else:
					count += 1

if __name__ == '__main__':
	data_process = PreProcessWithPandas('../AmazonDataBackup/MProductReviewsLatest.csv')
	data_process.word_count()	