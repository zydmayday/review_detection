import os
import numpy as ntpath
from pandas import Series, DataFrame
import pandas as pd
import nltk

class PreProcessWithPandas():
	def __init__(self, file_name=None):
		if file_name:
			self.data = self.load_file(file_name)

	def load_file(self, file_name):
		return pd.read_csv(file_name)

	def tf_idf(self, by='Body'):
		col = self.data[by]
		

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
	data_process = PreProcessWithPandas('test_data.csv')
	data = data_process.data
	print data.index
