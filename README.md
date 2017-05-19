Clean a 20,000-row .csv file.

## Usage

This program is written for Python 2.
Required dependencies are [petl](http://petl.readthedocs.io) and [pyenchant](https://pythonhosted.org/pyenchant):

```
pip install petl
pip install pyenchant
```

To run the tests: `pytest -v`

To run the program: navigate to the `healthify_code_challenge` directory and run `python transform.py /path/to/input/file.csv`

The cleaned data is outputted as `output.csv`, in the same directory as the input file.

## Overview

Data have two fields: id (integer) and description (string). There are a couple of different issues with the description data:

* some descriptions are entirely title-cased
* some words are misspelled
* some words are mis-cased
* there are spaces missing between some words

## Describing the corpus

We will be working entirely within the description field data. Here are some of its characteristics:

* there are no hyphens
* there are no semicolons
* there are no #, $, %, &, (), +, or = characters
* there are no internal quotation marks—only  external opening and closing "" around some (not all) of the descriptions
* there are numbers in some of the descriptions
* all sentences end in periods (no question or exclamation marks)
* there are no commas that are not followed by a space

## Initial approach: de-title-casing

On its face, correcting the entirely title-cased descriptions is the simplest part of this task: split each description into its constituent words, and if each word in a particular description is title-cased, then we know it needs to be corrected.

However, if we un-title-case all but the first word in each sentence of these descriptions, then we risk losing some appropriately title-cased words, i.e., proper nouns, acronyms, etc. We can easily check if a word consists entirely of capital letters, in which case we can leave it as it is (making the hopefully fairly reasonable assumption that it was written that way for a legitimate reason). Checking if a word is a actually a proper noun is more difficult:

* natural language parsers tend to treat title-cased words as proper nouns simply on the basis that they are title-cased
* any dictionary we use to look up proper nouns will have a limited corpus, and many of the proper nouns in these descriptions—for example, the name of a small community organization in some random city—will most likely not be in the dictionary

Thus, it probably makes the most sense to de-title-case all non-all-caps, non-sentence-leading words in these all-title-cased descriptions, and attempt to re-title-case some of them afterwards by checking against the limited proper nouns available in various dictionaries.

It's possible that we could train an AI to use some combination of dictionary look-ups and web scraping to determine if, for example, a series of title-cased words correspond to the name of a real organization; however, that is beyond the scope of this code challenge.

## Dictionaries

Checking each word in a 20,000-row file is very time-intensive. One way to speed up the process could be to use memoization—storing an internal list of words to check each subsequent word against before turning to a dictionary API, which is slower. However, we cannot assume that the words in these descriptions are spelled correctly—in fact, we know that many of them are *not*.

We could also use memoization to track words that should be title-cased; however, just because words are title-cased in one place (i.e., 'Neighborly Care Network') doesn't mean that they should be title-cased throughout the corpus.

Furthermore, while we could attempt to use some kind of auto-correct library on words that seem to be misspelled, there is no guarantee that this would be helpful:

* a) there are correct nouns in the corpus that would fail dictionary checks (names of people, organizations, etc.)
* b) some words are missing spaces between them and so would certainly not be autocorrected to anything of value

Thus, autocorrect, applied blindly without the assistance of some kind of AI trained on the corpus, will without a doubt result in the loss of potentially correct information; this scenario seems less preferable than its alternative: information that is source-accurate but may have typos, mistakes, syntax errors, etc.

## Optimizations

Are there any subsets of the techniques described above that might be beneficial in ways that don't compromise the integrity of the data?

One possibility w.r.t title-casing: if a lower-cased word doesn't exist in the dictionary (for example, 'america' or 'usa') and the word is equal to a lower-cased version of one of its dictionary suggestions (in this case, 'America' or 'USA'), then it is probably a proper noun which has simply been mis-cased. In these cases, we can replace the word with this dictionary suggestion with relative confidence that we are choosing correctly.

Another possibility w.r.t words with spaces missing between them: simply iterate over the characters, at each index checking if both the left-slice and right-slice are words. If we reach this point, we can reasonably assume that this is where the space is meant to go, and slice the string in two on that index. This will certainly not be 100% effective—there are probably many sets of two words that, when smushed together, have multiple ways of dividing them into two correct words—but it seems like a reasonable assumption for this corpus.

## Implementation

I have written a Python program to clean this data. I use the [petl](http://petl.readthedocs.io) module to structure the ETL pipeline and the [pyenchant](https://pythonhosted.org/pyenchant) module for string parsing and spellchecking.

## Further thoughts

With more time, I would have written tests for the output file (it should have the same number of rows—it does), added a command-line progress bar (since the function takes some time to run), and looked into American place name dictionaries (it shouldn't be too hard to find one to check names of towns, counties, etc., against).

I believe machine learning, web scraping, and more complex parsing/transformation algorithms could also help provide more comprehensive data cleaning with only a small loss to source-accuracy. Some examples and texts that seem instructive/promising:

* ["Multi-Level Feature Extraction for Spelling Correction,"](http://research.ihost.com/and2007/cd/Proceedings_files/p79.pdf) by Johannes Schaback and Fang Li, *[IJCAI-2007 Workshop on Analytics for Noisy Unstructured Text Data](http://research.ihost.com/and2007)*
* [Transform Data by Example - Microsoft Research](https://microsoft.com/en-us/research/project/transform-data-by-example)
* ["tRuEcasIng,"](https://cs.cmu.edu/~llita/papers/lita.truecasing-acl2003.pdf) by Lucian Vlad Lita, Abe Ittycheriah, Salim Roukos, and Nanda Kambhatla, *[41st Annual Meeting of the Association for Computational Linguistics (ACL 2003)](https://aclweb.org/mirror/acl2003)*
