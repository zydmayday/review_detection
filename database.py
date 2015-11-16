import sqlite3

class Database:
	def __init__(self, name):
		self.conn = sqlite3.connect(name)

	def create_feature_table(self):
		self.conn.execute("drop table if exists features")
		self.conn.execute('''
			CREATE TABLE `features` (
			`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			`review_id`	INTEGER NOT NULL,
			`fb_num`	INTEGER ,
			`help_fb_num`	INTEGER ,
			`pc_help_fb`	REAL ,
			`r_title_len`	INTEGER ,
			`r_body_len`	INTEGER ,
			`data_order_asc`	INTEGER ,
			`data_order_desc`	INTEGER ,
			`is_first`	INTEGER ,
			`is_only`	INTEGER ,
			`pc_pos_words`	REAL ,
			`pc_neg_words`	REAL ,
			`sim_with_prod`	REAL ,
			`pc_times_brand`	REAL ,
			`pc_num`	REAL ,
			`pc_cap`	REAL ,
			`pc_cap_word`	REAL ,
			`rating`	REAL ,
			`dev_rating`	REAL ,
			`fea_indic`	INT ,
			`bad_after_first_good`	INT ,
			`good_after_first_bad`	INT ,
			`r_first_review`	INT ,
			`r_only_review`	INT ,
			`avg_rating`	INT ,
			`std_dev`	INT ,
			`alw_one_rating`	INT ,
			`both_good_bad`	INT ,
			`both_good_avg`	INT ,
			`both_bad_avg`	INT ,
			`all_three`	INT ,
			`f31`	REAL ,
			`f32`	REAL ,
			`price`	REAL ,
			`sales_rank`	INT ,
			`prod_avg_rating`	REAL ,
			`std_dev_rating`	REAL );''')

	def close(self):
		self.conn.close()

	def insert_into_features(self, keywords={}):
		sql_start = "INSERT INTO FEATURES ("
		sql_end = ") VALUES ("
		for key, word in keywords.iteritems():
			sql_start += str(key) + ','
			sql_end += "\'" + str(word) + '\','
		sql_end = sql_end[0:-1]
		sql_end += ');'
		print sql_start[:-1] + sql_end
		with self.conn:
			cur = self.conn.cursor()
			cur.execute(sql_start[:-1] + sql_end)

	def delete_feature(self, where, value):
		sql = "DELETE from FEATURES where " + str(where) + "=" + str(value) + ";"
		print sql
		with self.conn:
			cur = self.conn.cursor()
			cur.execute(sql)

if __name__ == "__main__":
	db = Database('reviews.db')
	db.create_feature_table()
	# db.insert_into_features({'review_id': 2})
	# db.delete_feature('review_id', 3)
	