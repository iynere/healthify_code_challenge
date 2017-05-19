# -*- coding: utf-8 -*-

# imports
import pytest
from enchant import tokenize
from utils import is_all_titlecased, filter_periods, is_all_caps, try_to_fix_case, is_sentence_leading, fix_sentence_titlecasing, make_suggested_case_corrections, find_split_idx, fix_sentence_smushes, create_output_path



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
  
def test_sentence_leader():
  '''test whether a word is a sentence-leader in a string'''
  string = test_data['sentence for leading test']
  # first word in string
  assert is_sentence_leading(list(tokenizer(string))[0], string) == True
  # first word after a period
  assert is_sentence_leading(list(tokenizer(string))[2], string) == True
  # not a sentence-leader
  assert is_sentence_leading(list(tokenizer(string))[1], string) == False
  
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
  # with periods
  assert word_tokens_after[7][0] == word_tokens_before[7][0]
  # or without
  assert word_tokens_after[19][0] == word_tokens_before[19][0]
  # sentence-leading words stay title-cased
  # at the beginning of the string
  assert word_tokens_after[0][0] == word_tokens_before[0][0]
  # or in a new sentence within the string
  assert word_tokens_after[13][0] == word_tokens_before[13][0]
  
def test_casing_corrections():
  '''make sure the case-correction function is working'''
  # fixes case, ignores words without a valid suggested correction, leaves valid words as they were
  assert make_suggested_case_corrections(test_data['wrong case']) == 'USA is the best but usal is an invalid word without a case-only suggestion'
  
def test_find_split_idx():
  '''see if split idx finder returns the right index'''
  assert find_split_idx(test_data['split idx exists']) == 7
  assert find_split_idx(test_data['no split exists']) == None
  
def test_sentence_smush_fixer():
  '''test adding spaces between smushed words within an entire sentence'''
  # unsmushes smushed sentence, ignores invalid words that can't be unsmushed
  assert fix_sentence_smushes(test_data['smushed sentence']) == 'hey there how goes it today lkjasdlkfjlkdjf'
  # leaves sentences alone if words are spelled right or can't be un-unsmushed
  assert fix_sentence_smushes(test_data['non-smushed sentence']) == test_data['non-smushed sentence']
  
def test_output_path():
  '''make sure output path gets created correctly'''
  assert create_output_path(test_data['input path']) == '/path/to/input/output.csv'
  