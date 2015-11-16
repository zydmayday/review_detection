import sqlite3

class Database:
	def __init__(self, name):
		self.conn = sqlite3.connect('features.db')

	def create_feature_table():
		self.conn.execute('''
			CREATE TABLE `features` (
			`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			`review_id`	INTEGER NOT NULL,
			`fb_num`	INTEGER NOT NULL,
			`help_fb_num`	INTEGER NOT NULL,
			`pc_help_fb`	REAL NOT NULL,
			`r_title_len`	INTEGER NOT NULL,
			`r_body_len`	INTEGER NOT NULL,
			`data_order_asc`	INTEGER NOT NULL,
			`data_order_desc`	INTEGER NOT NULL,
			`is_first`	INTEGER NOT NULL,
			`is_only`	INTEGER NOT NULL,
			`pc_pos_words`	REAL NOT NULL,
			`pc_neg_words`	REAL NOT NULL,
			`sim_with_prod`	REAL NOT NULL,
			`pc_times_brand`	REAL NOT NULL,
			`pc_num`	REAL NOT NULL,
			`pc_cap`	REAL NOT NULL,
			`pc_cap_word`	REAL NOT NULL,
			`rating`	REAL NOT NULL,
			`dev_rating`	REAL NOT NULL,
			`fea_indic`	INT NOT NULL,
			`bad_after_first_good`	INT NOT NULL,
			`good_after_first_bad`	INT NOT NULL,
			`r_first_review`	INT NOT NULL,
			`r_only_review`	INT NOT NULL,
			`avg_rating`	INT NOT NULL,
			`std_dev`	INT NOT NULL,
			`alw_one_rating`	INT NOT NULL,
			`both_good_bad`	INT NOT NULL,
			`both_good_avg`	INT NOT NULL,
			`both_bad_avg`	INT NOT NULL,
			`all_three`	INT NOT NULL,
			`f31`	REAL NOT NULL,
			`f32`	REAL NOT NULL,
			`price`	REAL NOT NULL,
			`sales_rank`	INT NOT NULL,
			`prod_avg_rating`	REAL NOT NULL,
			`std_dev_rating`	REAL NOT NULL);''')

	def close():
		self.conn.close()