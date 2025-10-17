#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bstree import bstree
import config

def test_bstree_insert():
    config.verbose = 0
    tree = bstree()
    
    # Test basic insertion
    if not tree.insert("hello"):
        print("Error: failed to insert hello")
    if not tree.insert("world"):
        print("Error: failed to insert world")
    # Test duplicate insertion
    if tree.insert("hello"):
        print("Error: duplicate insertion should return False")
    if not tree.find("hello"):
        print("Error: hello should be found")
    if not tree.find("world"):
        print("Error: world should be found")

def test_bstree_find():
    config.verbose = 0
    tree = bstree()
    
    tree.insert("apple")
    tree.insert("banana")
    tree.insert("cherry")
    
    if not tree.find("banana"):
        print("Error: banana should be found")
    if tree.find("grape"):
        print("Error: grape should not be found")

def test_bstree_size():
    config.verbose = 0
    tree = bstree()
    
    tree.insert("one")
    tree.insert("two")
    tree.insert("three")
    if not tree.find("one"):
        print("Error: one should be found")
    if not tree.find("two"):
        print("Error: two should be found")
    if not tree.find("three"):
        print("Error: three should be found")

def test_bstree_empty():
    config.verbose = 0
    tree = bstree()
    
    if tree.find("anything"):
        print("Error: should not find anything in empty tree")

if __name__ == "__main__":
    test_bstree_insert()
    test_bstree_find()
    test_bstree_size()
    test_bstree_empty()
    print("All bstree tests passed!")
