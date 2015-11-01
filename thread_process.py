# coding:utf-8

import threading
import summary_plot
import time

file_end_flag = False
gram_end_flag = False

content_list = []
grams_list = []
gram_pair_list = []

file_lock = threading.Lock()
gram_lock = threading.Lock()
distance_lock = threading.Lock()


class FileReader(threading.Thread):
	def __init__(self, filename):
		threading.Thread.__init__(self)
		self.fp = open(filename)

	def run(self):
		global content_list
		global file_end_flag
		print 'start FileReader'
		for line in self.fp:
			file_lock.acquire()
			content_list.append(line.split('\t')[-1])
			print '\t append one line into content_list'
			file_lock.release()
			time.sleep(1)
		file_end_flag = True
		print 'end FileReader'


class GramConverter(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		print 'start GramConverter'
		global content_list
		global grams_list
		global file_end_flag
		global gram_end_flag
		while not (file_end_flag and len(content_list) == 0):
			file_lock.acquire()
			if content_list:
				content = content_list.pop()
				grams = summary_plot.get_2_grams(content)
				gram_lock.acquire()
				grams_list.append(grams)
				print '\t\t append one grams into grams_list'
				gram_lock.release()
			file_lock.release()
			time.sleep(1)
		gram_end_flag = True
		print 'end GramConverter'

class GramPairDistributor(threading.Thread):
	"""
	存储所有的gram数组
	每当有一个新的gram Set进来时，就将其与之前所有的gram Set做成pair
	然后派发给JaccardDistanceComputer进行计算
	"""
	def __init__(self):
		threading.Thread.__init__(self)
		self.grams_list = []

	def run(self):
		print 'start GramPairDistributor'
		global file_end_flag
		global gram_end_flag
		global grams_list
		global gram_pair_list
		while not ( gram_end_flag and len(grams_list) == 0):
			gram_lock.acquire()
			grams = None
			if grams_list:
				print '\t\t\t try to get grams from grams_list - with ' + str(len(grams_list)) + ' grams'
				grams = grams_list.pop()
				print '\t\t\t get grams : ' + str(grams)
			gram_lock.release()
			if grams:
				distance_lock.acquire()
				for old_grams in self.grams_list:
					gram_pair_list.append([grams, old_grams])
				print '\t\t\t\t append gram_pairs into gram_pair_list'
				distance_lock.release()
				grams_list.append(grams)
			time.sleep(1)
		print 'end GramPairDistributor'

def main():
	t1 = FileReader('../AmazonDataBackup/reviewsNew/reviews_test.mP')
	t2 = GramConverter()
	t3 = GramPairDistributor()
	t1.start()
	t2.start()
	t3.start()
	t1.join()
	t2.join()
	t3.join()

	print gram_pair_list

if __name__ == '__main__':
	main()
