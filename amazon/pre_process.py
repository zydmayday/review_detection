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


NEED_PO	 = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN']

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

def pos_tag(file_name, suffix='_POStagged', fast=False):
	# start = datetime.datetime.now()
	# print start
	# file_name = '/home/data/amazon/testReviews.csv'
	file_name = file_name
	reviews = pd.read_csv(file_name)
	# calculate_time(start)
	if fast:
		reviews['postagged_body'] = reviews['Body'].map(lambda x: nltk.pos_tag([w for w in RegexpTokenizer(r'\w+').tokenize(str(x)) if w not in stopwords.words('english')]))
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
	# start = datetime.datetime.now()
	# print start
	reviews = pd.read_csv(file_name, error_bad_lines=False, sep=sep)
	cb = reviews['lemmatized_body']
	rate = reviews['Rating']
	# label all words with the rating
	for i, c in enumerate(cb):
		cb[i] = [(w, rate[i]) for w in c]
	# calculate_time(start)
	# get the corpus of all reviews, lists of all words with label
	cop_wl = []
	for b in cb:
		# change the unicode data to the raw string
		for i, w in enumerate(b):
			if type(w) == unicode:
				b[i] = unicodedata.normalize('NFKD', w).encode('utf-8','ignore')
		cop_wl += b
	# calculate_time(start)
	# word frequency of the corpus with label
	wfq = nltk.FreqDist(cop_wl)
	calculate_time(start)
	# get the word list of all reviews without label
	cop = [w[0] for w in cop_wl]
	cop = set(cop)
	cop_len = len(cop)
	calculate_time(start)
	# get freq of all words in one list
	wfq_l = []
	for i in range(1, 6):
		for w in cop:
			wfq_l.append(wfq[(w, i)])
	calculate_time(start)
	# reshape the list to a matrix
	wfq_mx = DataFrame(np.array(wfq_l).reshape((cop_len,5)), index=pd.Index(cop), columns=pd.Index([1,2,3,4,5]))
	calculate_time(start)
	# calculate the prob of each rating
	for i, r in wfq_mx.iterrows():
		wfq_mx.ix[i] = wfq_mx.ix[i]/wfq_mx.ix[i].sum()  
	reviews.to_csv(file_name.split('.')[0] + suffix + '.' + file_name.split('.')[1], sep='\t')
	calculate_time(start)

def get_max_indexs(list):
	m = max(list)
	return [i for i, j in enumerate(list) if j == m]

def word_useful_score(list, max_indexs, alpha=0.5):
	score = 0.0
	for m_i in max_indexs:
		m = list[m_i]
		# print score, '+=',m
		score += m
		for i, s in enumerate(list):
			# print score, '-= abs(', i, '-', m_i, ') *', s, '*', alpha 
			score -= abs(i - m_i) * s * alpha
	return score / len(max_indexs)

if __name__ == '__main__':
	# list = [0.45,0.45,0.05,0.03,0.02]
	# max_indexs = get_max_indexs(list)
	# print word_useful_score(list, max_indexs)
	# pos_tag('/home/data/amazon/zyd/data_5w.csv', fast=True)
	pos_tag('/home/data/amazon/zyd/data_100.csv', fast=True)
	# pos_tag('/home/data/amazon/zyd/MProductReviewsLatest_10.csv', fast=True)
	# lemmatize('/home/data/amazon/unicode_reviews_POStagged.csv', sep='\t')
	# word_freq('/home/data/amazon/zyd/unicode_reviews_POStagged_lemmatized.csv')

