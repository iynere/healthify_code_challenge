# -*- coding: utf-8 -*-

import csv, os, re, string, sys, petl

input = petl.fromcsv('data.csv')

def row_mapper(row):
	row_id = str(row[0])
	description = str(row[1])
	if all(word[0].capitalize() == word[0] for word in description.split(' ')):
		return [row_id, description.lower().capitalize()]
	else:
		return row

petl.rowmap(input, row_mapper, ['id', 'description'], failonerror=True).tocsv('output.csv')


# lambda row: [re.sub(r'\D\g', 'x', row)], ['id', 'description']

# output.tocsv('huh2.csv')


# conv = lambda v: prog.sub(repl, v, count=count)
#    return convert(table, field, conv)
# # def test_row_map(row):
# 	return 'lololololol'

# table2 = etl.rowmap(table1, test_row_map, header=['id','description'])

# table2.tocsv('output.csv')

'''
overall strategy:
program that takes 2 arguments:

1. data csv filepath (absolute or relative)
2. transform function (in this case, a function i'll write, which fixes the title-case issue identified in the instructions)
3. optional filepath for output; will default to same directory)
'''

