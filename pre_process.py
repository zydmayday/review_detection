import os
import file_util


# FU = file_util.FileUtil('../AmazonDataBackup/README.txt')


def get_product_array(file_name):
	product_array = []
	with open(file_name) as fp:
		for line in fp:
			product_array.append(line.split('\t')[0])
	return product_array

def get_mP_reviews(file_name, product_array):
	reviews = ''
	with open(file_name) as fp:
		for line in fp:
			if line.split('\t')[1] in product_array:
				reviews += line
	fp2 = open(file_name + '.mp', 'w')
	print 'finish writing ' + file_name + '.mp'
	fp2.write(reviews)
	fp2.close()

def get_mP_products(file_name, product_array):
	mProducts = ''
	with open(file_name) as fp:
		for line in fp:
			if line.split('\t')[0] in product_array:
				mProducts += line
	fp2 = open(file_name + '.mp', 'w')
	print 'finish writing ' + file_name + '.mp'
	fp2.write(mProducts)
	fp2.close()

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
	product_array = get_product_array('../AmazonDataBackup/productInfoXML-reviewed-mProducts.copy')
	print len(mProduct_array)
	# mProduct_reviews = ''
	mProductinfo = ''
	for (dirname, dirs, files) in os.walk('../AmazonDataBackup/productinfo'):
		for file in files[0:1]:
			print file
			with open('../AmazonDataBackup/productinfo/' + file) as f:
				for line in f.readlines()[0:10]:
					print line.split('\t')[0]
					if line.split('\t')[0] in mProduct_array:
						mProductinfo += line
				# mProduct_reviews += f.read()
	with open('../AmazonDataBackup/productinfo/productinfo.copy', 'w') as fp:
		fp.write(mProductinfo)
	# get_mP_reviews('../AmazonDataBackup/reviewsNew.txt', product_array)
	# get_mP_products('../AmazonDataBackup/productinfo.txt', product_array)
	# with open('../AmazonDataBackup/productinfo.txt') as fp:
	# 	for line in fp.readlines()[0:5]:
	# 		print line
	# split_file('reviewsNew.txt', 100000)
	# split_file('../AmazonDataBackup/productinfo.txt', 100000)

	# mProduct_reviews = ''
	# for (dirname, dirs, files) in os.walk('./reviewsNew'):
	# 	for file in files:
	# 		print file
	# 		with open('./reviewsNew/' + file) as f:
	# 			mProduct_reviews += f.read()
	# with open('./reviewsNew/reviewsNew.copy', 'w') as fp:
	# 	fp.write(mProduct_reviews)