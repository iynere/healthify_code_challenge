# -*- coding: utf-8 -*-

# imports
import petl
import re
import sys
from enchant import Dict, tokenize
from utils import is_all_titlecased, is_all_caps, try_to_fix_case, fix_sentence_titlecasing, is_sentence_leading, is_valid, find_split_idx, create_output_path

# spellchecking
dictionary = Dict('en_US')
tokenizer = tokenize.get_tokenizer('en_US')

# load csv file
# worth noting that petl knows to ignore the explicit "" around some descriptions and simply format each description as a string without its own internal quotation marks
input_path = sys.argv[1]
data = petl.fromcsv(input_path)

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
  description = make_corrections(fix_sentence_titlecasing(str(row[1])))

  return [row_id, description]

petl.rowmap(data, row_mapper, ['id', 'description'], failonerror=True).tocsv(create_output_path(input_path))

# notes: integrate word splitter
# add note about testing
# refactor