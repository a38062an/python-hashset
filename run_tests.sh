#!/bin/bash
# Quick test script to verify everything works

echo "Running all tests..."
echo ""

echo "=== Testing BSTree ==="
cd tests && python3 test_bstree.py
echo ""

echo "=== Testing HashSet ==="
python3 test_hashset.py
echo ""

echo "=== Running Spell Checker (HashSet) ==="
cd ../src && python3 speller_hashset.py -d ../data/simple/1/dict ../data/simple/1/infile
echo ""

echo "=== Running Spell Checker (BSTree) ==="
python3 speller_bstree.py -d ../data/simple/1/dict ../data/simple/1/infile
echo ""

echo "All tests completed!"
