# -*- coding: utf-8 -*-

import re

'''
RULES
-there are no hyphens
-there are no semicolons
-there's no #, $, %, &, (), +-=
-there are no internal quotation marks besides the single opening & closing ""
-there are sometimes numbers in the corpus
-all sentences end in periods (no question marks or exclamation marks)
-there are no commas that are not followed by a space
-there are mispelled and miscapitalized/mislowercased words
-there are words that are missing spaces between them
'''

def add_spaces_before(punctuation, string):
  '''adds leading spaces to any marks in a given set of punctuation'''
  return ''.join(map(lambda char: ' ' + char if char in punctuation else char, list(string)))
  # 'hello, there.' -> 'hello , there .'
  
def remove_spaces_before(punctuation, string):
  '''removes leading spaces from any marks in a given set of punctuation'''
  return ''.join(map(lambda (idx, char): '' if char == ' ' and str[idx+1] in punctuation else char, enumerate(list(str))))
  # 'hello , there .' -> 'hello, there.'

def words_list_from(string):
  '''turns a string of words into a list of the words'''
  # we need to separate words from their punctuation (just , & .)
  # but we need to preserve the punctuation, so we can use nlp to determine to if, for example, a word is the first in a new sentence & should be title-cased.
  # so we really need a completely parsed string, ie,
  # "The Organization objective is to provide food to families and individuals in need. In addition, we provide clothing, limited financial assistance, and help coordinate other social services."
  # to
  # [The, Organization, Objective, is, to, provide, food, to, the, families, and, individuals, in, need, ., in, addition, ,, we, provide, clothing ,, limited, financial, assistance, ,, and, help, coordinate, other, social, services, .]
  # because we also need to be able to correctly join the sentence back together, ie, we can't lose punctuation for good
  # we could use an actual nlp parser
  # but for now, simple solution:
  # can't really use an actual regex, since we need to preserve what the character is
  # we know it's just commas and periods
  # 1. why not split('') then map & if char = . || , add a leading space, then rejoin('')
  # 2. then split again on ' ' to do dictionary stuff
  # 3. then join again
  # 4. then map & reverse . / , stuff
  # 5. there must be a better way ??????
  