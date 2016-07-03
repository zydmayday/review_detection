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
from wordcloud import WordCloud
import matplotlib.pyplot as plt


NEED_POS = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN']

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
	# calculate_time(start)
	if fast:
		reviews['postagged_body'] = reviews['Body'].map(lambda x: nltk.pos_tag([w for w in RegexpTokenizer(r'\w+').tokenize(str(x)) if w.lower() not in stopwords.words('english')]))
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

def word_freq(file_name, suffix='_wordfreq', sep='\t'):
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
		# cb[i] = [(w, rate[i]) for w in c]
	# calculate_time(start)
	# get the corpus of all reviews, lists of all words with label
	cop_wl = []
	for b in cb:
		# change the unicode data to the raw string
		for i, w in enumerate(b):
			if type(w) == unicode:
				b[i] = unicodedata.normalize('NFKD', w).encode('utf-8','replace')
		cop_wl += b
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
		w_s.append(word_useful_score(list(wfq_mx.ix[i]), word_sum))
		w_sum.append(word_sum)

	wfq_mx['score'] = w_s
	wfq_mx['sum'] = w_sum

	wfq_mx.to_csv(file_name.split('.')[0] + suffix + '.' + file_name.split('.')[1], sep='\t')
	# calculate_time(start)

def word_useful_score(l, sum, alpha=0.5):
	max_indexs = [i for i, j in enumerate(l) if j == max(l)]
	score = 0.0
	for m_i in max_indexs:
		m = l[m_i]
		# print score, '+=',m
		score += m
		for i, s in enumerate(l):
			# print score, '-= abs(', i, '-', m_i, ') *', s, '*', alpha 
			score -= abs(i - m_i) * s * alpha
	return score / len(max_indexs) / log(sum+1)

def cloud_word(file_name):
	wd = pd.read_csv(file_name, sep='\t')
	wd_sort = wd.sort(['score'], False).ix[:, 0]
	words = ' '.join(list(wd_sort))
	wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(words)
	plt.figure()
	plt.imshow(wordcloud)
	plt.axis("off")
	# plt.show()
	plt.savefig(file_name.split['.'][0] + 'png')

if __name__ == '__main__':
	# list = [0.45,0.45,0.05,0.03,0.02]
	# print word_useful_score(list, max_indexs)
	# pos_tag('/home/data/amazon/zyd/data_5w.csv', fast=True)
	# pos_tag('test.csv', fast=True, sep='\t')
	# pos_tag('/home/data/amazon/zyd/data_100.csv', fast=True)
	# pos_tag('/home/data/amazon/zyd/MProductReviewsLatest_10.csv', fast=True)
	# lemmatize('/home/data/amazon/zyd/data_5w_POStagged.csv', sep='\t')
	# lemmatize('/home/data/amazon/zyd/data_100_POStagged.csv', sep='\t')
	# lemmatize('test_POStagged.csv', sep='\t')
	# word_freq('/home/data/amazon/zyd/data_5w_POStagged_lemmatized.csv')
	# word_freq('test_POStagged_lemmatized.csv')
	cloud_word('test_POStagged_lemmatized_wordfreq.csv')


