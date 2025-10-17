#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hashset import hashset
import config

def test_hashset_insert():
    config.verbose = 0
    config.init_size = 509
    hs = hashset()
    
    # Test basic insertion
    if not hs.insert("hello"):
        print("Error: failed to insert hello")
    if not hs.insert("world"):
        print("Error: failed to insert world")
    # Test duplicate insertion
    if hs.insert("hello"):
        print("Error: duplicate insertion should return False")
    if hs.number_of_values != 2:
        print("Error: should have 2 values")

def test_hashset_find():
    config.verbose = 0
    config.init_size = 509
    hs = hashset()
    
    hs.insert("apple")
    hs.insert("banana")
    hs.insert("cherry")
    
    if not hs.find("banana"):
        print("Error: banana should be found")
    if hs.find("grape"):
        print("Error: grape should not be found")

def test_hashset_collision():
    config.verbose = 0
    config.init_size = 509
    hs = hashset()
    
    # Insert many words
    for i in range(100):
        word = "word" + str(i)
        hs.insert(word)
    
    if hs.number_of_values != 100:
        print("Error: should have 100 values")
    if not hs.find("word50"):
        print("Error: word50 should be found")
    if not hs.find("word99"):
        print("Error: word99 should be found")

def test_hashset_rehash():
    config.verbose = 0
    config.init_size = 11
    hs = hashset()
    
    # Insert enough items to trigger rehash
    for i in range(20):
        word = "item" + str(i)
        hs.insert(word)
    
    if hs.number_of_rehashes <= 0:
        print("Error: should have triggered rehash")
    if hs.number_of_values != 20:
        print("Error: should have 20 values")

def test_hashset_empty():
    config.verbose = 0
    config.init_size = 509
    hs = hashset()
    
    if hs.find("anything"):
        print("Error: should not find anything in empty hashset")
    if hs.number_of_values != 0:
        print("Error: empty hashset should have 0 values")

if __name__ == "__main__":
    test_hashset_insert()
    test_hashset_find()
    test_hashset_collision()
    test_hashset_rehash()
    test_hashset_empty()
    print("All hashset tests passed!")
