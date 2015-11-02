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
			with open('global_value.py') as fp:
				if fp.read() == 'True':
					print 'exit', name
					l.release()
					break
				else:
					l.release()
					continue
		else:
			grams_pair_list = q.get()
			l.release()
			for grams in grams_pair_list:
				jaccard_distance = summary_plot.jaccard_distance(grams[0], grams[1])
				dis_list.append(jaccard_distance)
		# time.sleep(1)
	print 'writing to file'
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
			with open('global_value.py') as fp:
				if fp.read() == 'True':
					print 'exit', name
					l.release()
					break
				else:
					l.release()
					continue
		else:
			reviewer_content_dict = q.get()
			l.release()
			print 'process', name, 'have got ', str(len(reviewer_content_dict.keys())), 'reviewers content'
			similarity_list += summary_plot.get_reviewer_similarity(reviewer_content_dict)
			# print 'process' , name,' have done ', str(len(similarity_list))
	print 'writing to file', name
	if not path.exists('reviewer_similarity/'):
		makedirs('reviewer_similarity')
	with open('./reviewer_similarity/rs.' + str(name), 'w') as fp:
		fp.write(str(similarity_list))

def draw_review_distance_multiprocess():
	q = Queue()
	l = Lock()
	start = time.time()
	fu = file_util.FileUtil()
	fu.open_file('../AmazonDataBackup/reviewsNew/reviewsNew.mP')

	fu.get_structure()

	content_list = fu.get_content_list()[0:100]
	content_list_2_grams = summary_plot.get_2_grams_list(content_list)
	l.acquire()
	with open('global_value.py', 'w') as fp:
		fp.write('False')
	l.release()
	process_list = []
	for i in range(0,cpu_count()):
		p = Process(target=write_review_distance_to_file, args=(q, l, i))
		p.start()
		process_list.append(p)
	reviews_len = len(content_list_2_grams)

	count = 0
	grams_pair_list = []
	for i in range(0, reviews_len):
		for j in range(i + 1, reviews_len):
			if count % 50000 == 0:
				q.put(grams_pair_list)
				grams_pair_list = []
			grams_pair = [content_list_2_grams[i], content_list_2_grams[j]]
			grams_pair_list.append(grams_pair)
			count += 1
	q.put(grams_pair_list)
	print 'finish puting with %s s' % (time.time() - start)
	print count
	l.acquire()
	with open('global_value.py', 'w') as fp:
		fp.write('True')
	l.release()
	# print 'start join process'
	for p in process_list:
		p.join()	
	print 'exit main with %s s' % (time.time() - start)

	jd_list = []
	for (dirpath, dirnames, filenames) in walk('jaccard_distance'):
		for filename in filenames:
			if not filename.startswith('.'):
				print filename
				with open('jaccard_distance/' + filename) as fp:
					sub_list = ast.literal_eval(fp.read())
					print len(sub_list)
					jd_list += sub_list
	summary_plot.save_graph(summary_plot.get_reviews_similarity_relation(jd_list), 'review_similarity.png', use_log=[False, True], plot_type='bo-')

def draw_reviewer_similarity_multiprocess():
	q = Queue()
	l = Lock()
	start = time.time()
	fu = file_util.FileUtil()
	fu.open_file('../AmazonDataBackup/reviewsNew/reviewsNew.mP')
	fu.get_structure()
	print 'finish get_structure() with %s s' % (time.time() - start)
	# reviewer_content_dict = fu.get_reviewer_content_dict()
	l.acquire()
	with open('global_value.py', 'w') as fp:
		fp.write('False')
	l.release()
	process_list = []
	# producer = Process(target=producer, args=(q, l, 'producer', reviewer_content_dict))
	# p.start()
	for i in range(0,cpu_count()):
		p = Process(target=write_reviewer_similarity_to_file, args=(q, l, i))
		p.start()
		process_list.append(p)

	count = 0
	reviewer_content_dict = {}
	for line in fu.structure[0:1000000]:
		reviewer = line[0]
		if not reviewer in reviewer_content_dict.keys():
			if count % 6000 == 0:
				q.put(reviewer_content_dict)
				reviewer_content_dict = {}
			reviewer_content_dict[reviewer] = []
			count += 1
		reviewer_content_dict[reviewer].append(line[-1])
	q.put(reviewer_content_dict)
	print 'finish puting with %s s' % (time.time() - start)
	l.acquire()
	with open('global_value.py', 'w') as fp:
		fp.write('True')
	l.release()
	for p in process_list:
		p.join()
	print 'exit main with %s s' % (time.time() - start)

	reviewer_similarity_list = []
	for (dirpath, dirnames, filenames) in walk('reviewer_similarity'):
		for filename in filenames:
			if not filename.startswith('.'):
				print filename
				with open('reviewer_similarity/' + filename) as fp:
					sub_list = ast.literal_eval(fp.read())
					print len(sub_list)
					reviewer_similarity_list += sub_list
	print len(reviewer_similarity_list)
	summary_plot.save_graph(summary_plot.get_reviews_similarity_relation(reviewer_similarity_list),'reviewer_similarity.png', xlabel='Maxinum Similarity Score', ylabel='Number of Reviewers', use_log=[False, True], plot_type='bo-')


if __name__ == '__main__':
	# draw_review_distance_multiprocess()
	draw_reviewer_similarity_multiprocess()
