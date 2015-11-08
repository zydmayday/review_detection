# coding:utf-8

class FileUtil:

	def __init__(self, file_name='', open_type='r', **attrs):
		if file_name:
			self.fp = open(file_name, open_type)
		self.structure = []

	def open_file(self, file_name, open_type='r'):
		self.fp = open(file_name, open_type)

	def get_file_line(self):
		"""
		获取文件的行数
		"""
		non_blank_count = 0

		for line in self.fp:
			# if line.startswith(' ') or 'BREAK-REVIEWED' in line:
			non_blank_count += 1

		return non_blank_count

	def close(self):
		self.fp.close()

	def get_structure(self, split_type='\t'):
		"""
		将文本分割成一个二维数组，并存储
		和下面一个方法不同的是，这个直接把数组二维化
		"""
		self.structure = [line.split(split_type) for line in self.fp]
		return self.structure

	def get_line_list(self):
		"""
		用来获取文件中的每一行，同时做成一个数组
		"""
		return [line for line in self.fp]

	def get_column_list(self, columns=[0], split_type='\t'):
		"""
		私有方法
		获取每一行的特定列，同时组成数组
		"""
		col_len = len(columns)
		if col_len == 1:
			list = []
			for line in self.structure:
				try:
					list.append(line[columns[0]])
				except:
					continue
			return list
			# return [line[col] for col in columns for line in self.structure]
		else:
			return [[line[col] for col in columns] for line in self.structure]

	def get_memberId_list(self):
		"""
		具体的方法，用来获取文本中所有用户Id的list
		"""
		return self.get_column_list()

	def get_productId_list(self):
		"""
		这里的文本格式仅限制在reviewsNew.txt中
		获取文本中所有产品Id的list
		"""
		return self.get_column_list(columns=[1])

	def get_feedback_list(self):
		"""
		获取feedback的list，这个是helpful的数量
		"""
		return self.get_column_list(columns=[3])

	def get_rating_list(self):
		"""
		获取rating的list
		"""
		return self.get_column_list(columns=[5])

	def get_content_list(self):
		"""
		获取所有的review的内容
		"""
		return self.get_column_list(columns=[-1])

	def get_reviewer_content_dict(self):
		reviewer_content_dict = {}
		self.structure = self.structure[0:10000]
		for line in self.structure:
			reviewer = line[0]
			if not reviewer in reviewer_content_dict.keys():
				reviewer_content_dict[reviewer] = []
			reviewer_content_dict[reviewer].append(line[-1])
		# to_pop_reviewers = []
		# for reviewer, contents in reviewer_content_dict.iteritems():
		# 	if len(contents) == 1:
		# 		to_pop_reviewers.append(reviewer)
		# for reviewer in to_pop_reviewers:
		# 	reviewer_content_dict.pop(reviewer, None)
		return reviewer_content_dict
		
if __name__ == '__main__':
	fu = FileUtil('../AmazonDataBackup/reviewsNew.txt')
	fu.get_structure()
	print fu.get_file_line()
