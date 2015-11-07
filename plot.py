# coding:utf-8
from multi_process import draw_review_distance_multiprocess
import matplotlib.pyplot as plt
import collections
import file_util
import time 
import summary_plot


class Plot:

	def save_graph(self, dict, saveFilename, xlabel='Num Reviews', ylabel='Num Members', use_log=[True,True],log_base=[10,10], plot_type='rx', title=''):
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
		plt.plot(x_list, y_list, plot_type)
		plt.ylabel(ylabel)
		plt.xlabel(xlabel)
		plt.title(title)
		plt.axis([0, float(max(x_list))*1.2, 0, float(max(y_list))*1.2])
		plt.savefig(saveFilename)

	def multiprocess_putnum(self, test_dict, data_num):
		"""
		传入希望的总处理数据量，每次载入queue的数量量（dict形式）
		然后计算不同的queue数据量下处理的时间，最后画图
		"""
		for put_num in test_dict.keys():
			finish_time = draw_review_distance_multiprocess(list_num=data_num, put_num=put_num)
			print put_num, "with finish_time", finish_time
			test_dict[put_num] = finish_time
		# test_dict = collections.OrderedDict(sorted(test_dict.items()))
		print test_dict
		# self.save_graph(test_dict, 'graphs/multi_process1.png', xlabel='Queue Put Number', ylabel='Cost Time', use_log=[False, False], plot_type='ro-')

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
		line_single, line_multi = plt.plot(single_x_list, single_y_list, 'bx-', multi_x_list, multi_y_list, 'ro-')
		plt.legend([line_single, line_multi], ['Single', 'Multi'])
		plt.savefig('graphs/single_multi.png')

if __name__ == '__main__':
	plot = Plot()
	# test_dict = {}
	# for x in xrange(1000, 200000, 1000):
	# 	test_dict[x] = 0
	# print str(test_dict)
	# plot.multiprocess_putnum(test_dict, 2000)
	# plot.multi_single_datanum(10, 50, 10, 10)

	plot.save_graph(collections.OrderedDict(sorted({64000: 14.918230056762695, 96000: 15.744375944137573, 197000: 19.829822778701782, 85000: 15.994122982025146, 139000: 20.036482095718384, 42000: 15.09686803817749, 7000: 27.16706609725952, 110000: 15.831425905227661, 194000: 19.258142948150635, 63000: 14.682793140411377, 165000: 17.73047685623169, 20000: 17.920326948165894, 14000: 20.43348503112793, 107000: 15.52566409111023, 191000: 19.242440938949585, 41000: 15.102224111557007, 162000: 17.511078119277954, 134000: 16.996234893798828, 156000: 17.412498950958252, 62000: 15.627978801727295, 21000: 18.001748085021973, 133000: 16.631924152374268, 19000: 18.528390169143677, 188000: 19.1599280834198, 167000: 18.11474919319153, 159000: 21.29122805595398, 40000: 14.950007915496826, 92000: 15.98358702659607, 130000: 16.522154808044434, 61000: 15.211261987686157, 101000: 16.629250049591064, 185000: 18.54332685470581, 178000: 18.857381105422974, 82000: 15.144268035888672, 3000: 48.3637969493866, 127000: 17.625098943710327, 39000: 15.108372926712036, 98000: 15.999804019927979, 182000: 18.686457872390747, 60000: 15.043747901916504, 74000: 15.116554975509644, 153000: 17.371186017990112, 81000: 15.520318984985352, 124000: 18.9638991355896, 179000: 18.560935020446777, 38000: 14.806413888931274, 17000: 18.7116858959198, 113000: 18.151208877563477, 150000: 17.349174976348877, 59000: 14.380456924438477, 121000: 16.156711101531982, 16000: 19.90347719192505, 88000: 15.395801067352295, 176000: 18.709563970565796, 147000: 16.72798490524292, 37000: 15.161941051483154, 118000: 17.466742992401123, 58000: 15.186264991760254, 95000: 16.11911416053772, 135000: 19.816465854644775, 15000: 20.175090074539185, 144000: 20.101855993270874, 115000: 15.937544107437134, 36000: 15.119109153747559, 6000: 31.63468599319458, 170000: 20.851011037826538, 146000: 19.911347150802612, 57000: 14.930532932281494, 141000: 21.05031418800354, 78000: 17.307641983032227, 13000: 22.59499216079712, 112000: 15.29670000076294, 196000: 19.671149969100952, 35000: 16.236346006393433, 157000: 19.124186038970947, 138000: 17.162599086761475, 56000: 15.727712154388428, 84000: 14.522046089172363, 109000: 15.92066502571106, 193000: 19.255282878875732, 77000: 15.214536905288696, 164000: 20.746891975402832, 168000: 18.123740911483765, 34000: 15.136823177337646, 91000: 15.680315971374512, 106000: 15.070641994476318, 190000: 19.17009210586548, 55000: 14.853172063827515, 161000: 21.992069005966187, 76000: 16.81409215927124, 2000: 66.36966300010681, 132000: 16.69684410095215, 33000: 15.118573904037476, 187000: 18.664016008377075, 103000: 16.932559967041016, 158000: 17.653738975524902, 54000: 14.707251071929932, 73000: 15.4998939037323, 129000: 16.338701963424683, 11000: 24.236300945281982, 100000: 15.649889945983887, 184000: 19.0886070728302, 32000: 15.250720024108887, 80000: 15.245896100997925, 114000: 16.546409130096436, 126000: 16.05789804458618, 53000: 14.961920022964478, 97000: 15.811627864837646, 181000: 19.96997904777527, 10000: 24.293741941452026, 87000: 15.448606014251709, 125000: 16.5158588886261, 152000: 20.121020078659058, 31000: 15.459984064102173, 123000: 16.37104105949402, 52000: 14.618037939071655, 94000: 17.786370992660522, 136000: 18.259411096572876, 149000: 17.054018020629883, 9000: 25.049793004989624, 120000: 15.94108510017395, 30000: 16.03421401977539, 5000: 34.715928077697754, 175000: 18.13328504562378, 51000: 14.917027950286865, 117000: 16.08367609977722, 8000: 26.413170099258423, 12000: 22.15650510787964, 172000: 18.106805086135864, 29000: 15.842013835906982, 143000: 19.855108976364136, 199000: 19.6211519241333, 50000: 15.152168035507202, 83000: 15.376329183578491, 169000: 17.78787398338318, 71000: 14.912647008895874, 140000: 18.594067811965942, 28000: 15.694918155670166, 90000: 15.690378904342651, 111000: 17.00503921508789, 195000: 19.24498987197876, 49000: 15.14981198310852, 166000: 18.51816201210022, 137000: 16.61916208267212, 70000: 14.89110016822815, 65000: 14.657104969024658, 108000: 15.75787901878357, 192000: 19.509616136550903, 27000: 16.45912194252014, 163000: 17.72785711288452, 104000: 15.998986005783081, 48000: 14.603538036346436, 72000: 14.888283014297485, 105000: 17.021487951278687, 69000: 14.564287900924683, 173000: 18.304534912109375, 160000: 21.469449043273926, 26000: 16.34509301185608, 79000: 15.283149003982544, 131000: 16.797734022140503, 47000: 14.586381912231445, 102000: 15.778518915176392, 186000: 18.840651988983154, 155000: 17.707167863845825, 68000: 14.783122062683105, 86000: 16.405131101608276, 198000: 20.394216060638428, 128000: 16.56391406059265, 25000: 16.41101598739624, 99000: 16.040529012680054, 183000: 18.2150239944458, 46000: 15.179689884185791, 93000: 15.941359996795654, 154000: 19.332723140716553, 67000: 15.086982011795044, 180000: 21.71414589881897, 24000: 16.67489194869995, 4000: 39.802417039871216, 177000: 19.580168962478638, 151000: 18.512964963912964, 45000: 14.799952030181885, 122000: 17.075910091400146, 66000: 15.176244020462036, 75000: 14.961277961730957, 148000: 19.777824878692627, 23000: 16.991419076919556, 119000: 16.118332862854004, 44000: 15.079751968383789, 18000: 18.84535789489746, 174000: 20.461286067962646, 1000: 81.70069408416748, 145000: 16.670475006103516, 189000: 19.31572389602661, 116000: 16.58310580253601, 22000: 17.334073066711426, 89000: 15.937705039978027, 171000: 18.16211199760437, 43000: 14.970747947692871, 142000: 16.917114973068237}.items())), 'graphs/multi_putnum2000_costTime.png', plot_type='rx-', use_log=[False, False], log_base=[2, 10], title='2000 reviews with different queue put num', xlabel='Queue Put Number', ylabel='Cost Time')
	



