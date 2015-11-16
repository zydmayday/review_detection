import numpy as np
from database import Database
from file_util import FileUtil

class Feature:
	def __init__(self, new_file, filename=""):
		if filename:
			self.fu = FileUtil(filename)
			self.fu.get_structure()
		self.new_file = new_file
		# self.db = Database(dbname)

	def save_reviewid(self):
		reviewIds = self.fu.get_memberId_list()
		with open(self.new_file, 'a') as fp:
			review_txt = ""
			for review_id in reviewIds:
				review_txt += review_id + '\n'
			fp.write(review_txt)
		# for review_id  in reviewIds:
			# self.db.insert_into_features({'review_id': review_id})

	def save_f1(self):
		features = self.fu.get_feedback_list()
		review_txt = ""
		with open(self.new_file) as fp:
			for index, line in enumerate(fp.readlines()):
				review_txt += line.replace('\n', '') + '\t' + features[index] + '\n'
		with open(self.new_file, 'w') as fp:
			fp.write(review_txt) 

	def save_f2(self):
		help_features = self.fu.get_help_feedback_list()
		review_txt = ""
		with open(self.new_file) as fp:
			for index, line in enumerate(fp.readlines()):
				review_txt += line.replace('\n', '') + '\t' + help_features[index] + '\n'
		with open(self.new_file, 'w') as fp:
			fp.write(review_txt) 

	def save_f3(self):
		review_txt = ""
		with open(self.new_file) as fp:
			for line in fp.readlines():
				features = line.split('\t')
				if float(features[1]) == 0:
					review_txt += line.replace('\n', '') + '\t' + '0.0\n'
				else:
					review_txt += line.replace('\n', '') + '\t' + str(float(features[2])/float(features[1])) + '\n'
		with open(self.new_file, 'w') as fp:
			fp.write(review_txt) 

	def save_f4(self):
		title_list = self.fu.get_title_list()
		review_txt = ""
		with open(self.new_file) as fp:
			for index, line in enumerate(fp.readlines()):
				review_txt += line.replace('\n', '') + '\t' + str(len(title_list[index])) + '\n'
		with open(self.new_file, 'w') as fp:
			fp.write(review_txt) 

if __name__ == "__main__":
	fea = Feature('../AmazonDataBackup/reviewsNew/reviews.features',filename='../AmazonDataBackup/reviewsNew/reviewsNew.mp')
	# fea.save_reviewid()
	# fea.save_f1()
	# fea.save_f2()
	# fea.save_f3()
	fea.save_f4()
