#!/usr/bin/env python

import sys
import argparse
from setutils import *

parser = argparse.ArgumentParser(description = 'This is a utility to find the longest "word path" where each successive word differs from the last word by only one letter; added, removed, changed.  A starting word and word list must be provided.  The word list must consist of one word per line.')
parser.add_argument('-w', '--word', help = 'Starting word', required = True)
parser.add_argument('-f', '--wordfile', help = 'File contaning the words', required = True)
parser.add_argument('-o', '--outfile', help = 'Output file to store the full word path.  Argument is optional and the full word path will be printed to the console if not provided', required = False)

args = parser.parse_args()

# uncomment to print supplied arguments
DEBUG = False
if DEBUG:
    print("Starting word: %s" % args.word)
    print("File containing the words: %s" % args.wordfile)
    print("Output file: %s" % args.outfile)

start_word = args.word

# read all words into a list
with open(args.wordfile) as wf:
    word_corpus = wf.readlines()

# remove all whitespace characters from the word list
word_corpus = [w.strip().lower() for w in word_corpus]

iSets = [] # empty list to contain all ordered/indexed sets
iset_count = 0

def create_set(word, merge_iset=None):
    if merge_iset:
        newset = merge_iset.union([])
        newset.add(word)
    else:
        newset = IndexedSet([word])
    return newset

def add_to_set(aset):
    global iSets
    new_start_word = aset[-1].lower()
    for w in word_corpus:
        if DEBUG:
            print("Word = %s, iSet value = %s" % (w,new_start_word))
        if w in aset:
            continue
        if abs(len(new_start_word) - len(w)) == 1: #words within one letter length
            if DEBUG:
                print "words within one letter difference"
            if new_start_word == w[:-1]: # if either is equal add
                nset = create_set(w, aset)
                if DEBUG:
                    print("sw %s == word-1 %s" % (new_start_word,w[:-1]))
                    print nset
                if nset not in iSets:
                    iSets.append(nset)
                    return process_sets(iSets)
            elif new_start_word[:-1] == w: # if either is equal add
                nset = create_set(w, aset)
                if DEBUG:
                    print("sw-1 %s == word %s" % (new_start_word[:-1],w))
                    print nset
                if nset not in iSets:
                    iSets.append(nset)
                    return process_sets(iSets)
        elif abs(len(new_start_word) - len(w)) == 0:
            if DEBUG:
                print "words same length"
            if len(new_start_word) >= 2:
                if new_start_word[:-1] == w[:-1]:
                    nset = create_set(w, aset)
                    if DEBUG:
                        print("sw %s == word %s" % (new_start_word,w))
                        print nset
                    if nset not in iSets:
                        iSets.append(nset)
                        return process_sets(iSets)
        elif len(new_start_word) == 1:
            continue
        else:
            continue

def process_sets(mySets):
    global iSets
    if len(mySets) == 0:
        iSets.append(create_set(start_word))
        return process_sets(iSets)
    else:
        #numsets = len(mySets)
        for s in mySets:
            add_to_set(s)

process_sets(iSets)
l = len(iSets[-1])
while len(iSets[-1]) == l:
    longest_set = iSets.pop()
    print("The longest path(s) are %d words long" % len(longest_set))
    print longest_set


# for n in range(len(iSets)):
#     print("Values in iSet %d are: " % n)
#     print iSets[n]
#     print("length of iSet %d is %d: " % (n, len(iSets[n])))
