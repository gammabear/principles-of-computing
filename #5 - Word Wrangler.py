"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import math

WORDFILE = "assets_scrabble_words3.txt"

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    result = []
    
    prev_word = ""
    for idx in range(len(list1)):
        curr_word = list1[idx]

        if curr_word != prev_word:
            result.append(curr_word)
        elif curr_word == prev_word:
            pass
        prev_word = curr_word    
    return result

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    result = []
    list1 = remove_duplicates(list1)
    list2 = remove_duplicates(list2)
    result = [val for val in list1 if val in list2]
    return result

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in both list1 and list2.

    This function can be iterative.
    """   
    result = []
    list1_copy = []
    list2_copy = []
    for idx in range(len(list1)):
        list1_copy.append(list1[idx])
    for idy in range(len(list2)):
        list2_copy.append(list2[idy])

    while list1_copy and list2_copy:
        if list1_copy[0] < list2_copy[0]:
            result.append(list1_copy.pop(0))
        else:
            result.append(list2_copy.pop(0))
    
    return result + list1_copy + list2_copy
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if (len(list1) == 1 or len(list1) == 0):
        return list1
    
    length = len(list1)
    mid = int(math.floor(length/2))
    first = []
    second = []
    for idx in range(mid):
        first.append(list1[idx])
    for idy in range(mid, length):
        second.append(list1[idy])

    sorted_first = merge_sort(first)
    sorted_second = merge_sort(second)
    result = merge(sorted_first, sorted_second) 
    return result

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    result = []
    if word == "":
        return [word]
    
    first = word[0]
    rest_word = word[1:]
    rest_strings = []
    rest_strings = gen_all_strings(rest_word)
    
    for string in rest_strings:
        if string == "":
            new_string = first
            result.append(new_string)
        else:
            for idx in range(len(string)+1):
                front = string[0:idx]
                back = string[idx:]
                new_string = front + first + back
                result.append(new_string)
    return result + rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    
    data = []
    for line in netfile.readlines():
        word = line.strip()
        data.append(word)
    return data

def run():
    """
    Run game.
    """
    #list1 = ["aye", "bye", "bye", "hi", "hi", "oh"]
    #list1 = ["aye"]
    #list2 = ["cya", "bye", "aye"]
    
    #sortedlist = merge_sort(list2)
    #print "merge_sorted", sortedlist
    
    #list3 = ["bye", "oh", "hi", "hi"]
    
    
    #list2 = remove_duplicates(list1)
    #inter = intersect(list1, list3)
    
    #merged = merge(list1, list2)
    #print "merged", merged
    
    #print "remove_dupes", list2
    
    #print "intersect", inter
    
    #all_strings = gen_all_strings("bar")
    #print "all strings", all_strings
    
    words = load_words(WORDFILE)
    
    
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                    gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()