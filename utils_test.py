# -*- coding: utf-8 -*-

# imports
import pytest
from enchant import tokenize
from utils import is_all_titlecased, is_all_caps, filter_periods, try_to_fix_case, fix_sentence_titlecasing, is_sentence_leading, find_split_idx, create_output_path
from test_data import test_data

# spellchecking
tokenizer = tokenize.get_tokenizer('en_US')

def test_titlecased():
	'''test if a string is title-cased'''
	assert is_all_titlecased(test_data['titlecased']) == True
	assert is_all_titlecased(test_data['not titlecased']) == False
	
def test_filter_periods():
	'''test whether filter_periods removes periods from a string'''
	assert filter_periods(test_data['acronym with periods']) == 'ACRONYM'  

def test_allcaps():
	'''test if a string is all-caps'''
	# with periods
	assert is_all_caps(test_data['acronym with periods']) == True
	# or without
	assert is_all_caps(test_data['allcaps string']) == True
	assert is_all_caps(test_data['lowercased string']) == False
	
def test_word_case_fixer():
	'''test case-fixing function'''
	# should return the word itself if no suggestions exist
	assert try_to_fix_case(test_data['no suggestions']) == test_data['no suggestions']
	# should return the word itself if the top suggestion is not simply a differently cased version of the word
	assert try_to_fix_case(test_data['different word']) == test_data['different word']
	# replaces word with top suggestion if it is different only in casing
	assert try_to_fix_case(test_data['only miscased']) == 'USA'
	
def test_sentence_case_fixer():
	'''test case-fixing functions applied to an entire sentence'''
	# returns original string unless all words are title-cased
	assert fix_sentence_titlecasing(test_data['regular sentence']) == test_data['regular sentence']
	# process a title-cased sentence
	word_tokens_before = list(tokenizer(test_data['titlecased sentence']))
	word_tokens_after = list(tokenizer(fix_sentence_titlecasing(test_data['titlecased sentence'])))
	
	# non-sentence-leading, non-allcaps words get lowercased
	assert word_tokens_after[1][0] == word_tokens_before[1][0].lower()
	assert word_tokens_after[11][0]  == word_tokens_before[11][0].lower()
	# all-caps words stay all-caps
	assert word_tokens_after[8][0] == word_tokens_before[8][0]
	assert word_tokens_after[20][0] == word_tokens_before[20][0]
	# sentence-leading words stay title-cased
	assert word_tokens_after[0][0] == word_tokens_before[0][0]
	assert word_tokens_after[14][0] == word_tokens_before[14][0]
	
def test_sentence_leader():
	'''test whether a word is a sentence-leader in a string'''
	string = test_data['sentence for leading test']
	# first word in string
	assert is_sentence_leading(list(tokenizer(string))[0], string) == True
	# first word after a period
	assert is_sentence_leading(list(tokenizer(string))[2], string) == True
	# not a sentence-leader
	assert is_sentence_leading(list(tokenizer(string))[1], string) == False
	
def test_find_split_idx():
	'''see if split idx finder returns the right index'''
	assert find_split_idx(test_data['split idx exists']) == 7
	assert find_split_idx(test_data['no split exists']) == None
	
def test_output_path():
	'''make sure output path gets created correctly'''
	assert create_output_path(test_data['input path']) == '/path/to/input/output.csv'