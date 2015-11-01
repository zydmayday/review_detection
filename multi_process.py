from multiprocessing import Pool, Process, Lock, Queue, cpu_count
import summary_plot
import file_util

def write_distance_to file(q, l, name):
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
			grams_list = []
			for x in xrange(1,10000):
				grams_list.append(q.get())
				if q.empty():
					break
			l.release()
			for grams in grams_list:
				jaccard_distance = summary_plot.jaccard_distance(grams[0], grams[1])
				dis_list.append(jaccard_distance)
		# time.sleep(1)
	print 'writing to file'
	# with open('./jaccard_distance/jd.' + str(name), 'w') as fp:
	# 	fp.write(str(dis_list))


if __name__ == '__main__':
	fu = file_util.FileUtil()

	fu.open_file('../AmazonDataBackup/reviewsNew/reviewsNew.mP')

	fu.get_structure()

	content_list = fu.get_content_list()[0:1000]
	content_list_2_grams = summary_plot.get_2_grams_list(content_list)

	with open('global_value.py', 'w') as fp:
		fp.write('False')
	q = Queue()
	l = Lock()
	process_list = []
	cpu_count = cpu_count()
	for i in range(0,cpu_count):
		p = Process(target=write_distance_to file, args=(q, l, i))
		p.start()
		process_list.append(p)
	reviews_len = len(content_list_2_grams)
	for i in range(0, reviews_len):
		for j in range(i + 1, reviews_len):
			q.put([content_list_2_grams[i], content_list_2_grams[j]])
	with open('global_value.py', 'w') as fp:
		fp.write('True')
	for p in process_list:
		p.join()	
	print 'exit main'
