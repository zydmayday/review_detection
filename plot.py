# coding:utf-8
from multi_process import draw_review_distance_multiprocess
import matplotlib.pyplot as plt
import collections
import file_util
import time 
import summary_plot

class Plot:

	def save_graph(self, dict, saveFilename, xlabel='Num Reviews', ylabel='Num Members', use_log=[True,True], plot_type='rx'):
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

	def multiprocess_putnum(self, test_dict, data_num):
		"""
		传入希望的总处理数据量，每次载入queue的数量量（dict形式）
		然后计算不同的queue数据量下处理的时间，最后画图
		"""
		for put_num in test_dict.keys():
			finish_time = draw_review_distance_multiprocess(list_num=data_num, put_num=put_num)
			test_dict[put_num] = finish_time
		test_dict = collections.OrderedDict(sorted(test_dict.items()))
		print test_dict
		self.save_graph(test_dict, 'graphs/multi_process1.png', xlabel='Queue Put Number', ylabel='Cost Time', use_log=[False, False], plot_type='ro-')

	def singleprocess_datanum(self, test_dict):
		fu = file_util.FileUtil('../AmazonDataBackup/reviewsNew/reviewsNew.mP')
		fu.get_structure()
		for data_num in test_dict.keys():
			print data_num
			content_list = fu.get_content_list()[0:data_num]
			content_list_2_grams = summary_plot.get_2_grams_list(content_list)
			start = time.time()
			jd_list = summary_plot.get_jd_list(content_list_2_grams)
			summary_plot.get_reviews_similarity_relation(jd_list)
			finish_time = time.time() - start
			print 'finish get relation with %s s' % finish_time
			test_dict[data_num] = finish_time
		test_dict = collections.OrderedDict(sorted(test_dict.items()))
		return test_dict
		# self.save_graph(test_dict, 'graphs/single_distance_different_datanum', xlabel='Total Data Number', ylabel='Cost Time', use_log=[False, False], plot_type='bo-')

	def multiprocess_datanum(self, test_dict, put_num):
		for data_num in test_dict.keys():
			print data_num
			finish_time = draw_review_distance_multiprocess(list_num=data_num, put_num=put_num)
			test_dict[data_num] = finish_time
		test_dict = collections.OrderedDict(sorted(test_dict.items()))
		return test_dict
		# self.save_graph(test_dict, 'graphs/multi_process1.png', xlabel='Total Data Number', ylabel='Cost Time', use_log=[False, False], plot_type='ro-')

	def multi_single_datanum(self, min_num, max_num, step, put_num):
		# plot = Plot()
		test_dict = {}
		for x in xrange(min_num, max_num, step):
			test_dict[x] = 0
		# plot.multiprocess_putnum(test_dict, 2000)
		single_dict = self.singleprocess_datanum(test_dict)
		single_x_list = single_dict.keys()
		single_y_list = single_dict.values()
		multi_dict = self.multiprocess_datanum(test_dict, put_num)
		multi_x_list = multi_dict.keys()
		multi_y_list = multi_dict.values()
		plt.ylabel('Cost Time')
		plt.xlabel('Total Data Num')		
		line1, line2 = plt.plot(single_x_list, single_y_list, 'bx-', multi_x_list, multi_y_list, 'ro-')
		plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
		plt.savefig('graphs/single_multi.png')

if __name__ == '__main__':
	plot = Plot()
	plot.multi_single_datanum(10, 50, 10, 10)
	



