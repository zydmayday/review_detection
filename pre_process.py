import os
def get_file_line(file_name):

	non_blank_count = 0

	with open(file_name) as infp:
		for line in infp.readlines():
			# if line.startswith(' ') or 'BREAK-REVIEWED' in line:
			non_blank_count += 1

	return non_blank_count

# get the number of all reviews
# 5838923
# print get_file_line('reviewsNew.txt')

def get_pure_file(file_name, to_file):
	file_txt = ''
	with open(file_name) as fp:
		for line in fp:
			if 'BREAK-REVIEWED' in line:
				pass
			else:
				file_txt += line
	with open(to_file, 'w') as tf:
		tf.write(file_txt)

def get_product_features_file(file_name, to_file):
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

def get_mp_file(file_name, to_file):
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

# get_pure_file('productInfoXML-reviewed-mProducts.txt', 'productInfoXML-reviewed-mProducts.copy')

def get_product_array(file_name):
	product_array = []
	with open(file_name) as fp:
		for line in fp:
			product_array.append(line.split('\t')[0])
	return product_array

# 36255
# product_array = get_product_array('productinfoXML-reviewed-mProducts.copy')

def get_reviewer_array(file_name):
	reviewer_array = []
	with open(file_name) as fp:
		for line in fp:
			reviewer_array.append(line.split('\t')[0])
	return set(reviewer_array)

# 164524
# print len(get_reviewer_array('./reviewsNew/reviewsNew.copy'))

def get_mP_reviews(file_name, product_array):
	reviews = ''
	with open(file_name) as fp:
		for line in fp:
			if line.split('\t')[1] in product_array:
				reviews += line
	fp2 = open(file_name + '.mP', 'w')
	print 'finish writing ' + file_name + '.copy'
	fp2.write(reviews)
	fp2.close()

# mp reviews num : 226764
# get the mProduct reviews from file
# for (dirname, dirs, files) in os.walk('./reviewsNew'):
# 	for file in files:
# 		print file
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

if __name__ == '__main__':
	get_product_features_file('productInfoXML-reviewed-mProducts.pure', 'productInfoXML-reviewed-mProducts.features')
	# get_pure_file('productInfoXML-reviewed-mProducts.txt', 'productInfoXML-reviewed-mProducts.pure')
	# split_file('productinfo.txt', 1000000)
	# product_array = get_product_array('productinfoXML-reviewed-mProducts.copy')
	# mp_product = ""
	# with open('productinfo.txt') as fp:
	# 	for line in fp:
	# 		if line.split('\t')[0] in product_array:
	# 			mp_product += line
	# with open('productinfo.mp','w') as fp:
	# 	fp.write(mp_product)
	# for (dirname, dirs, files) in os.walk('./productinfo'):
	# 	for file in files:
	# 		if file.startswith('p'):
	# 			print file
	# 			mProduct_reviews = ''
	# 			get_mp_file('./productinfo/' + file, './productinfo/' + file + '.mp')
				# with open('./productinfo/' + file) as fp:
				# 	for line in fp.readlines():
				# 		if line.split("\t")[0] in product_array:
	# 						mProduct_reviews += line	
	# 			# get_pure_file('./productinfo/' + file, './productinfo/' + file + '.pure')
	# 			with open('./productinfo/' + file.split('.')[0] + '.mp', 'w') as fp:
	# 				fp.write(mProduct_reviews)
	# for (dirname, dirs, files) in os.walk('./productinfo'):
	# 	for file in files:
	# 		if file.endswith('mp'):
	# 			print file
	# 			mProduct_reviews = ''
	# 			with open('./productinfo/' + file) as fp:
	# 				mProduct_reviews += fp.read()
	# 	with open('./productinfo/productinfo.mp', 'w') as fp:
	# 		fp.write(mProduct_reviews)
