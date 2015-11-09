# coding:utf-8
from multiprocessing import Pool, Process, Lock, Queue, cpu_count
import summary_plot
import file_util
import time
import ast
from os import walk, path, makedirs

def producer(q, l, name, to_process_list):
	reviewer_content_list = []
	count = 0
	for contents in to_process_list.values():
		if count % 100 == 0:
			l.acquire()
			q.put(reviewer_content_list)
			l.release()
			reviewer_content_list = []
		reviewer_content_list.append(contents)
		count += 1
	l.acquire()
	q.put(reviewer_content_list)
	l.release()
	print 'finish puting', name

def write_review_distance_to_file(q, l, name):
	"""
	多进程方法
	获取一个grams_pair的数组
	计算数组中每个元素的distance
	然后存入自己的dis_list中
	在任务完成之后，写入自己的进程对应的文件中
	"""
	print 'starting process %s' % name
	dis_list = []
	while True:
		l.acquire()
		if q.empty():
			l.release()
			# time.sleep(0.1)
			continue
		else:
			grams_pair_list = q.get()
			if grams_pair_list == 'STOP':
				print 'process', name, ' exit'
				l.release()
				break
			l.release()
			# print 'process', name, 'have got ', len(grams_pair_list), 'reviews'
			for grams in grams_pair_list:
				jaccard_distance = summary_plot.jaccard_distance(grams[0], grams[1])
				dis_list.append(jaccard_distance)
		# time.sleep(1)
	# print 'writing to file'
	if not path.exists('jaccard_distance/'):
		makedirs('jaccard_distance')
	with open('./jaccard_distance/jd.' + str(name), 'w') as fp:
		fp.write(str(dis_list))

def write_reviewer_similarity_to_file(q, l, name):
	print 'starting process %s' % name
	similarity_list = []
	while True:
		l.acquire()
		if q.empty():
			l.release()
			time.sleep(0.1)
			continue
		else:
			reviewer_content_dict = q.get()
			if reviewer_content_dict == 'STOP':
				print 'process', name, ' exit'
				l.release()
				break
			l.release()
			# print 'process', name, 'have got ', str(len(reviewer_content_dict.keys())), 'reviewers content'
			similarity_list += summary_plot.get_reviewer_similarity(reviewer_content_dict)
			# print 'process' , name,' have done ', str(len(similarity_list))
	print 'writing to file', name
	if not path.exists('reviewer_similarity/'):
		makedirs('reviewer_similarity')
	with open('./reviewer_similarity/rs.' + str(name), 'w') as fp:
		fp.write(str(similarity_list))

def draw_review_distance_multiprocess(list_num=-1, put_num=10000):
	q = Queue()
	l = Lock()
	fu = file_util.FileUtil()
	fu.open_file('../AmazonDataBackup/reviewsNew/reviewsNew.mP')
	fu.get_structure()
	content_list = fu.get_content_list()[0:list_num]
	content_list_2_grams = summary_plot.get_2_grams_list(content_list)
	# l.acquire()
	# with open('global_value.py', 'w') as fp:
	# 	fp.write('False')
	# l.release()
	start = time.time()
	process_list = []
	cpu_num = cpu_count()
	for i in range(0,cpu_num):
		p = Process(target=write_review_distance_to_file, args=(q, l, i))
		p.start()
		process_list.append(p)
	reviews_len = len(content_list_2_grams)
	print reviews_len
	count = 0
	grams_pair_list = []
	for i in range(0, reviews_len):
		for j in range(i + 1, reviews_len):
			if count != 0:
				if count % put_num == 0:
					q.put(grams_pair_list)
					grams_pair_list = []
				# if count % (put_num * 12) == 0 and not q.empty():
				# 	time.sleep(5)
			grams_pair = [content_list_2_grams[i], content_list_2_grams[j]]
			grams_pair_list.append(grams_pair)
			count += 1
	q.put(grams_pair_list)
	for i in range(0,cpu_num):
		q.put('STOP')
	# print 'finish puting with %s s' % (time.time() - start)
	# l.acquire()
	# with open('global_value.py', 'w') as fp:
	# 	fp.write('True')
	# l.release()
	# print 'start join process'
	for p in process_list:
		p.join()
	finish_time = time.time() - start
	print 'exit main with %s s' % finish_time	
	return finish_time

def draw_graph(dirname, title, xlabel, ylabel):
	jd_list = []
	for (dirpath, dirnames, filenames) in walk(dirname):
		for filename in filenames:
			if not filename.startswith('.'):
				print filename
				with open(dirname + '/' + filename) as fp:
					sub_list = ast.literal_eval(fp.read())
					jd_list += sub_list
	print len(jd_list)
	summary_plot.save_graph(summary_plot.get_reviews_similarity_relation(jd_list), 'graphs/' + dirname + '.png', use_log=[False, True], plot_type='bo-', xlabel=xlabel, ylabel=ylabel, title=title)


def draw_reviewer_similarity_multiprocess():
	q = Queue()
	l = Lock()
	start = time.time()
	fu = file_util.FileUtil()
	fu.open_file('../AmazonDataBackup/reviewsNew/reviewsNew.mP')
	fu.get_structure()
	print 'finish get_structure() with %s s' % (time.time() - start)
	# reviewer_content_dict = fu.get_reviewer_content_dict()
	# l.acquire()
	# with open('global_value.py', 'w') as fp:
	# 	fp.write('False')
	# l.release()
	process_list = []
	# producer = Process(target=producer, args=(q, l, 'producer', reviewer_content_dict))
	# p.start()
	for i in range(0,cpu_count()):
		p = Process(target=write_reviewer_similarity_to_file, args=(q, l, i))
		p.start()
		process_list.append(p)

	count = 0
	reviewer_content_dict = {}
	for line in fu.structure:
		reviewer = line[0]
		if not reviewer in reviewer_content_dict.keys():
			if count % 2000 == 0:
				q.put(reviewer_content_dict)
				reviewer_content_dict = {}
			reviewer_content_dict[reviewer] = []
			count += 1
		reviewer_content_dict[reviewer].append(line[-1])
	q.put(reviewer_content_dict)
	for i in range(0,cpu_count()):
		q.put('STOP')
	print 'finish puting with %s s' % (time.time() - start)
	# l.acquire()
	# with open('global_value.py', 'w') as fp:
	# 	fp.write('True')
	# l.release()
	for p in process_list:
		p.join()
	finish_time = time.time() - start
	print 'exit main with %s s' % finish_time
	# return finish_time

	# reviewer_similarity_list = []
	# for (dirpath, dirnames, filenames) in walk('reviewer_similarity'):
	# 	for filename in filenames:
	# 		if not filename.startswith('.'):
	# 			print filename
	# 			with open('reviewer_similarity/' + filename) as fp:
	# 				sub_list = ast.literal_eval(fp.read())
	# 				print len(sub_list)
	# 				reviewer_similarity_list += sub_list
	# print len(reviewer_similarity_list)
	# with open("reviewer_similarity_relation_all", "w") as fp:
	# 	fp.write(str(summary_plot.get_reviews_similarity_relation(reviewer_similarity_list)))
	# summary_plot.save_graph(summary_plot.get_reviews_similarity_relation(reviewer_similarity_list),'reviewer_similarity.png', xlabel='Maxinum Similarity Score', ylabel='Number of Reviewers', use_log=[False, True], plot_type='bo-')

if __name__ == '__main__':
	# time_dict = {10000:0, 50000:0}
	# for put_num in [100,500,1000,5000,10000,20000,50000]:
	# for put_num in time_dict.keys():
	# 	finish_time = draw_review_distance_multiprocess(list_num=1000, put_num=put_num)
	# 	time_dict[put_num] = finish_time
	# print time_dict
	draw_graph('jaccard_distance', xlabel='Similarity Score', ylabel='Num Pairs', title='')

	# draw_review_distance_multiprocess(put_num=2000, list_num=50000)
