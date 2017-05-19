# -*- coding: utf-8 -*-

# imports
import re
from enchant import Dict, tokenize

# spellchecking
dictionary = Dict('en_US')
tokenizer = tokenize.get_tokenizer('en_US')

def is_all_titlecased(string):
  '''checks if each word in a string is titlecased'''
  # enchant's tokenizer breaks a string into tokens of its constituent words, organized as tuples of the form (word, start_index)
  # we check only the first character because all-caps strings are not considered title-cased
  return all(token[0][0].istitle() for token in list(tokenizer(string)))

def filter_periods(word):
  '''filter out periods in acronyms/all-caps words'''
  return re.sub(r'\.', '', word)

def is_all_caps(word):
  '''checks if a word is all-caps'''
  # filter out '.' in case word is an acronym of the form 'U.S.A.' rather than 'USA'
  return all(char.istitle() for char in list(filter_periods(word)))
  
def try_to_fix_case(word):
  '''return top suggestion if it differs from word only in case, otherwise return original word '''
  suggestions = dictionary.suggest(word)
  
  if suggestions:
    if suggestions[0].lower() == word.lower():
      return suggestions[0]
  return word
  
def fix_sentence_titlecasing(string):
  '''de-title-cases all non-all-caps, non-sentence-leading words in a completely title-cased string; otherwise returns the original string'''
  if is_all_titlecased(string):
    chars = list(string)
    
    # if word isn't all-caps and isn't a sentence-leader, lowercase it
    for token in list(tokenizer(string)):
      if not is_all_caps(token[0]) and not is_sentence_leading(token, string):
        chars[token[1]] = chars[token[1]].lower()
        
    return ''.join(chars)
  return string

def is_sentence_leading(token, string):
  '''checks if a word is at the beginning of a sentence within a given string'''
  # either it's the string's first word , or there is a '.' at its start index - 2
  return token[1] == 0 or  string[token[1] - 2] == '.'
  
def is_valid(word):
  '''checks if word exists in dictionary'''
  return dictionary.check(word)
  
def find_split_idx(smushed_words):
  '''returns index where word can be split into 2 valid words, or else None'''
  for index in range(1, len(smushed_words)):
    if is_valid(smushed_words[0:index]) and is_valid(smushed_words[index:]):
      return index
  return None
  
def create_output_path(input_path):
  '''creates output file in same directory as input file'''
  return '/'.join(input_path.split('/')[0:-1]) + '/output.csv'
  