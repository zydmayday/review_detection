import numpy as np
import sqlite3

conn = sqlite3.connect('features.db')

conn.execute('''
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
	);''')