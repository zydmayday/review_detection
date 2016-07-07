import pandas as pd
from pandas import DataFrame
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import ast
import unicodedata
import datetime
import numpy as np
from math import *
from scipy.misc import imread
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# import matplotlib.pyplot as plt


# NEED_POS = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN']
NEED_POS = ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN']

def remove_extra_tags(tags_list):
	return_tags_list = []
	for t in tags_list:
		if t[1] in NEED_POS:
			return_tags_list.append(t)
	return return_tags_list

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

# def calculate_time(start):
# 	now = datetime.datetime.now()
# 	print now, 'has run', (now - start)

def pos_tag(file_name, suffix='_POStagged', fast=False, sep=','):
	# start = datetime.datetime.now()
	print "start pos_tag"
	# file_name = '/home/data/amazon/testReviews.csv'
	file_name = file_name
	reviews = pd.read_csv(file_name, sep=sep)
	def w(x):
		pw = nltk.pos_tag([w.lower() for w in RegexpTokenizer(r'\w+').tokenize(str(x)) if w.lower() not in stopwords.words('english')])
		print pw
		return pw
	# calculate_time(start)
	if fast:
		reviews['postagged_body'] = reviews['Body'].map(lambda x: w(x))
		# reviews['postagged_body'] = reviews['Body'].map(lambda x: nltk.pos_tag(nltk.tokenize(str(x))))
	else:
		reviews['postagged_body'] = reviews['Body'].map(lambda x: TextBlob(str(x), pos_tagger=PerceptronTagger()).tags)

	# calculate_time(start)
	reviews['postagged_body_cleaned'] = reviews['postagged_body'].map(lambda x: remove_extra_tags(x))
	# calculate_time(start)
	reviews.to_csv(file_name.split('.')[0] + suffix + '.' + file_name.split('.')[1], sep='\t')
	# reviews.to_csv('/home/data/amazon/testReviewsPOStagged.csv', sep='\t')
	# calculate_time(start)

def lemmatize(file_name, suffix='_lemmatized', sep='\t'):
	print "start lemmatize"
	def l(tags_list):
		tags_list = ast.literal_eval(tags_list)
		lmtzr = WordNetLemmatizer()
		return_tags_list = []
		for t in list(tags_list):
			return_tags_list.append(lmtzr.lemmatize(t[0],get_wordnet_pos(t[1]))) 
		return return_tags_list

	reviews = pd.read_csv(file_name, error_bad_lines=False, sep=sep)
	reviews['lemmatized_body'] = reviews['postagged_body_cleaned'].map(lambda x: l(x))
	reviews.to_csv(file_name.split('.')[0] + suffix + '.' + file_name.split('.')[1], sep='\t')

def word_freq(file_name, suffix='_wordfreq', sep='\t', threshold=.5):
	print "start word_freq"
	# start = datetime.datetime.now()
	# print start
	reviews = pd.read_csv(file_name, error_bad_lines=False, sep=sep)
	cb = reviews['lemmatized_body']
	rate = reviews['Rating']
	# label all words with the rating
	cb_temp = []
	for i, c in enumerate(cb):
		cb_temp.append([(w, rate[i]) for w in ast.literal_eval(c)])
	reviews['lemmatized_body'] = cb_temp
	# calculate_time(start)
	# get the corpus of all reviews, lists of all words with label
	'''--------------------------------------------------------'''
	cop_wl = []
	for b in cb_temp:
		# change the unicode data to the raw string
		# cop_wl += [(unicodedata.normalize('NFKD', w[0]).encode('utf-8','replace'), w[1]) for w in b if type(w[0])==unicode]
		cop_wl += b
	'''--------------------------------------------------------'''
	# calculate_time(start)
	# word frequency of the corpus with label
	wfq = nltk.FreqDist(cop_wl)
	# calculate_time(start)
	# get the word list of all reviews without label
	cop = [w[0] for w in cop_wl]
	cop = set(cop)
	cop_len = len(cop)
	# calculate_time(start)
	# get freq of all words in one list
	wfq_l = []
	for w in cop:
		for i in range(1, 6):
			wfq_l.append(wfq[(w, i)])

	# calculate_time(start)
	# reshape the list to a matrix
	wfq_mx = DataFrame(np.array(wfq_l).reshape((cop_len,5)), index=pd.Index(cop), columns=pd.Index([1,2,3,4,5]))
	# calculate_time(start)
	# calculate the prob of each rating
	w_s = []
	w_sum = []
	for i, r in wfq_mx.iterrows():
		word_sum = wfq_mx.ix[i].sum()
		# wfq_mx.ix[i] = wfq_mx.ix[i]/word_sum
		w_s.append(word_useful_score(list(wfq_mx.ix[i])))
		w_sum.append(word_sum)

	wfq_mx['score'] = w_s
	wfq_mx['sum'] = w_sum
	wfq_mx = wfq_mx.sort(columns='sum').ix[-int(len(w_s) * threshold):,:]
	print wfq_mx
	wfq_mx.to_csv(file_name.split('.')[0] + suffix + '.' + file_name.split('.')[1], sep='\t')
	# calculate_time(start)

def word_useful_score(l, alpha=0.5):
	def sigmoid(x):
		print x
		if float(x) is float('nan'):
			return 0.5
		if abs(x) > 700:
			return 0
		return 1 / (1 + exp(-x))
	max_indexs = [i for i, j in enumerate(l) if j == max(l)]
	score = 0.0
	for m_i in max_indexs:
		m = l[m_i]
		# print score, '+=',m
		score += m
		for i, s in enumerate(l):
			# print score, '-= abs(', i, '-', m_i, ') *', s, '*', alpha 
			score -= abs(i - m_i) * s * alpha
	score = score / len(max_indexs)
	return sigmoid(score) - 0.5

def cloud_word_for_words(file_name):
	wd = pd.read_csv(file_name, sep='\t')
	words = []
	for i, w in wd.iterrows():
		for j in range(int(w['score'])):
			words.append(w['name'])
	words = ' '.join([str(w) for w in words])
	wordcloud = WordCloud(background_color='white', max_words=200,  
						  width=1800, height=1000, relative_scaling=.5,
						  max_font_size=200, stopwords=STOPWORDS).generate(words)
	plt.figure()
	plt.imshow(wordcloud)
	plt.axis("off")
	# plt.show()
	plt.savefig(file_name.split('.')[0] + '.png')

def cloud_word_with_mask(file_name):
	text = open(file_name).read()
	# read the mask / color image
	# amazon_coloring = imread('amazon-logo_grey.png')

	wc = WordCloud(background_color="white", max_words=200, #mask=amazon_coloring,
	               stopwords=STOPWORDS.add("said"),
	               max_font_size=200, random_state=42, width=1800, height=1000)
	# generate word cloud
	wc.generate(text)

	# create coloring from image
	# image_colors = ImageColorGenerator(amazon_coloring)

	# recolor wordcloud and show
	# we could also give color_func=image_colors directly in the constructor
	# plt.imshow(wc.recolor(color_func=image_colors))
	plt.figure()
	plt.imshow(wc)
	plt.axis("off")
	# plt.show()
	plt.savefig(file_name.split('.')[0] + '.png')

def collect_text_for_cw(file_name='data_5w_POStagged_lemmatized_score.csv', type='low'):
	rd = pd.read_csv(file_name, sep='\t')
	rd = rd.sort(columns='score', ascending=True).reset_index()
	with open(type+'.txt', 'w') as fw:
		if type=='low':
			fw.write(''.join([w for w in list(rd['Body'].ix[:])[:1000] if str(w) != 'nan']))
		elif type=='high':
			fw.write(''.join([w for w in list(rd['Body'].ix[:])[-1000:] if str(w) != 'nan']))

def review_score(file_name, wd_file_name, suffix='_score'):
	rd = pd.read_csv(file_name, sep='\t')
	wd = pd.read_csv(wd_file_name, sep='\t')
	wd.columns = ['name', 1,2,3,4,5, 'score', 'sum']
	words = list(wd['name'])
	# rd['lemmatized_body'] = rd['lemmatized_body'].map(lambda x: ast.literal_eval(x))
	def s(wd, l):
		# print [w for w in l]
		nume = sum([float(wd.ix[wd['name']==w, 'score']) for w in ast.literal_eval(l) if w in words])
		deno = len(str(rd.ix[rd['lemmatized_body'] == l, 'Body'].values[0]).split())
		score = nume / deno
		print l, score
		# print [float(wd.ix[wd['name']==w, 'score']) for w in l], score
		return score
	rd['score'] = rd['lemmatized_body'].map(lambda x: s(wd, x))
	rd.to_csv(file_name.split('.')[0] + suffix + '.' + file_name.split('.')[1], sep='\t')

if __name__ == '__main__':
	# list = [0.2,0.2,0.2,0.2,0.2]
	# print word_useful_score(list, 1)
	# pos_tag('data_5w.csv', fast=True)
	# pos_tag('test.csv', fast=True)
	# pos_tag('test_100.csv', fast=True, sep='\t')
	# pos_tag('/home/data/amazon/zyd/data_100.csv', fast=True)
	# pos_tag('/home/data/amazon/zyd/MProductReviewsLatest_10.csv', fast=True)
	# lemmatize('data_5w_POStagged.csv', sep='\t')
	# lemmatize('/home/data/amazon/zyd/data_100_POStagged.csv', sep='\t')
	# lemmatize('test_POStagged.csv', sep='\t')
	word_freq('data_5w_POStagged_lemmatized.csv')
	# word_freq('test_POStagged_lemmatized.csv')
	# cloud_word_for_words('high_words.csv')
	# review_score('test.csv', 'test_POStagged_lemmatized_wordfreq.csv')
	review_score('data_5w_POStagged_lemmatized.csv', 'data_5w_POStagged_lemmatized_wordfreq.csv')
	# lemmatize('test_100_POStagged.csv', sep='\t')
	# word_freq('/home/data/amazon/zyd/data_5w_POStagged_lemmatized.csv')
	# word_freq('test_100_POStagged_lemmatized.csv')
	# cloud_word_with_mask('high.txt')
	# review_score(file_name='test_100_POStagged_lemmatized.csv', wd_file_name='test_100_POStagged_lemmatized_wordfreq.csv')
	# collect_text_for_cw(type='high')
