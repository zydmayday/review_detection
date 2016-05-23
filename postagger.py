import pandas as pd
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

NEED_POS = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN']

def remove_extra_tags(tags_list):
	return_tags_list = []
	for t in tags_list:
		if t[1] in NEED_POS:
			return_tags_list.append(t)
	return return_tags_list

if __name__ == '__main__':
	# file_name = '../../testReviews.csv'
	file_name = '../../MProductReviewsLatest.csv'
	reviews = pd.read_csv(file_name)
	reviews['postagged_body'] = reviews['Body'].map(lambda x: TextBlob(x, pos_tagger=PerceptronTagger()).tags)
	reviews['postagged_body'] = reviews['postagged_body'].map(lambda x: remove_extra_tags(x))
	reviews.to_csv('../../MProductReviewsLatestPOStagged.csv', sep='\t')