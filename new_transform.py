# -*- coding: utf-8 -*-

# imports
import enchant
import petl
import re
import sys
from enchant.tokenize import get_tokenizer

# spellchecking
dictionary = enchant.Dict('en_US')
tokenizer = get_tokenizer('en_US')

# load csv file
# worth noting that petl knows to ignore the explicit "" around some descriptions and simply format each description as a string without its own internal quotation marks
input = petl.fromcsv(sys.argv[1])


def is_all_titlecased(string):
  '''checks if each word in a string is titlecased'''
  # enchant's tokenizer breaks a string into tokens of its constituent words, organized as tuples of the form (word, start_index)
  return all(token[0].istitle() for token in list(tokenizer(string)))


def is_all_caps(word):
  '''checks if a word is all-caps'''
  # filter out '.' in case word is an acronym of the form 'U.S.A.' rather than 'USA'
  return all(char.istitle() for char in list(re.sub(r'\.', '', word)))

def is_sentence_leading(token, string):
  '''checks if a word is at the beginning of a sentence within a given string'''
  # either it's the string's first word , or there is a '.' at its start index - 2
  return token[1] == 0 or  string[token[1] - 2] == '.'


def fix_titlecasing(string):
  '''de-title-cases all non-all-caps, non-sentence-leading words in a completely title-cased string; otherwise returns the original string'''
  if is_all_titlecased(string):
    chars = list(string)
    
    # if word isn't all-caps and isn't a sentence-leader, lowercase it
    for token in list(tokenizer(string)):
      if not is_all_caps(token[0]) and not is_sentence_leading(token, string):
        chars[token[1]] = chars[token[1]].lower()
        
    return ''.join(chars)
  return string

def is_valid(word):
  '''checks if word exists in dictionary'''
  return dictionary.check(word)

def try_to_fix_case(word):
  '''return top suggestion if it differs from word only in case, otherwise return original word '''
  suggestions = dictionary.suggest(word)
  
  if suggestions:
    if suggestions[0].lower() == word.lower():
      return suggestions[0]
      
  return word
  
def split_idx_exists(smushed_words):
  '''returns index where word can be split into 2 valid words, or else None'''
  for index in range(len(smushed_words)):
    if is_valid(smushed_words[0:index]) and is_valid(smushed_words[index:]):
      return index
      
  return None
  
def split(word, idx):
  '''call this if a valid split idx exists—inserts a space between the 2 words and returns the string'''
  return word[0:idx] + ' ' + word[idx:]

def make_corrections(string):
  '''
  1. replace invalid words with suggested case corrections if they exist
  2. try to separate words if they might actually be 2 words missing a space between them
  '''
  # make string into list for manipulating words/chars
  chars = list(string)
  
  # iterate through list of word/idx tokens
  for token in list(tokenizer(string)):
    if not is_valid(token[0]):
      start = token[1]
      end = start + len(token[0])
      chars[start:end] = list(try_to_fix_case(token[0]))
      
  return ''.join(chars)

def row_mapper(row):
  row_id = str(row[0])
  description = make_corrections(fix_titlecasing(str(row[1])))

  return [row_id, description]

petl.rowmap(input, row_mapper, ['id', 'description'], failonerror=True).tocsv('output.csv')

# notes: integrate word splitter
# add note about testing
# refactor