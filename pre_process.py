import os
import file_util


# def get_file_line(file_name):

# 	non_blank_count = 0

# 	with open(file_name) as infp:
# 		for line in infp.readlines():
# 			# if line.startswith(' ') or 'BREAK-REVIEWED' in line:
# 			non_blank_count += 1

# 	return non_blank_count

FU = file_util.FileUtil('../AmazonDataBackup/README.txt')
# get the number of all reviews
# 5838923
# print get_file_line('reviewsNew.txt')

def get_product_array(file_name):
	product_array = []
	with open(file_name) as fp:
		for line in fp:
			product_array.append(line.split('\t')[0])
	return product_array

# 36255    36246
# product_array = get_product_array('productinfoXML-reviewed-mProducts.copy')

# def get_reviewer_array(file_name):
# 	reviewer_array = []
# 	with open(file_name) as fp:
# 		for line in fp:
# 			reviewer_array.append(line.split('\t')[0])
# 	return set(reviewer_array)

# 164524
# print len(get_reviewer_array('./reviewsNew/reviewsNew.copy'))

def get_mP_reviews(file_name, product_array):
	reviews = ''
	with open(file_name) as fp:
		for line in fp:
			if line.split('\t')[1] in product_array:
				reviews += line
	fp2 = open(file_name + '.copy', 'w')
	print 'finish writing ' + file_name + '.copy'
	fp2.write(reviews)
	fp2.close()



# mp reviews num : 226764
# get the mProduct reviews from file
# for (dirname, dirs, files) in os.walk('./reviewsNew'):
# 	for file in files:
# 		get_mP_reviews('./reviewsNew/' + file, product_array)


def write_txt_to_file(f, newfile, line_num):
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

def split_file(file_name, line_num):
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

# split_file('reviewsNew.txt', 100000)

# mProduct_reviews = ''
# for (dirname, dirs, files) in os.walk('./reviewsNew'):
# 	for file in files:
# 		print file
# 		with open('./reviewsNew/' + file) as f:
# 			mProduct_reviews += f.read()
# with open('./reviewsNew/reviewsNew.copy', 'w') as fp:
# 	fp.write(mProduct_reviews)





