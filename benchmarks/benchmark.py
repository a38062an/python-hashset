#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import time
from bstree import bstree
from hashset import hashset
import config

def benchmark_insert(data_structure, words, name):
    start = time.time()
    for word in words:
        data_structure.insert(word)
    end = time.time()
    return end - start

def benchmark_find(data_structure, words, name):
    start = time.time()
    for word in words:
        data_structure.find(word)
    end = time.time()
    return end - start

def load_dictionary(filepath):
    words = []
    with open(filepath, 'r') as f:
        for line in f:
            for word in line.split():
                words.append(word.lower().strip())
    return words

def run_benchmarks():
    print("=" * 60)
    print("Data Structure Performance Benchmark")
    print("=" * 60)
    
    # Find a dictionary file
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    dict_files = []
    
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file == 'dict':
                dict_files.append(os.path.join(root, file))
    
    if not dict_files:
        print("No dictionary files found in data directory!")
        return
    
    # Use the first dictionary file found
    dict_file = dict_files[0]
    print("\nLoading dictionary: " + os.path.relpath(dict_file))
    words = load_dictionary(dict_file)
    print("Loaded " + str(len(words)) + " words\n")
    
    results = {}
    
    # Benchmark BSTree
    print("Benchmarking BSTree...")
    config.verbose = 0
    tree = bstree()
    insert_time = benchmark_insert(tree, words, "BSTree")
    find_time = benchmark_find(tree, words[:min(1000, len(words))], "BSTree")
    
    # Calculate metrics
    ops_per_sec = len(words) / insert_time
    avg_comparisons = tree.number_of_comparisons / tree.number_of_executions
    
    results['BSTree'] = {
        'insert': insert_time,
        'find': find_time,
        'size': tree.size(),
        'comparisons': tree.number_of_comparisons,
        'executions': tree.number_of_executions,
        'ops_per_sec': ops_per_sec,
        'avg_comparisons': avg_comparisons
    }
    print("  Insert time: " + str(round(insert_time, 6)) + "s")
    print("  Find time (1000 words): " + str(round(find_time, 6)) + "s")
    print("  Size: " + str(tree.size()))
    print("  Ops/sec: " + str(int(ops_per_sec)))
    print("  Avg comparisons: " + str(round(avg_comparisons, 2)))
    print()
    
    # Benchmark HashSet
    print("Benchmarking HashSet...")
    config.verbose = 0
    # Uses init_size from config.py
    hs = hashset()
    
    # Track collisions separately for insert and find
    insert_time = benchmark_insert(hs, words, "HashSet")
    collisions_after_insert = hs.number_of_collisions
    accesses_after_insert = hs.number_of_accesses
    
    find_time = benchmark_find(hs, words[:min(1000, len(words))], "HashSet")
    collisions_after_find = hs.number_of_collisions
    accesses_after_find = hs.number_of_accesses
    
    # Calculate metrics
    ops_per_sec = len(words) / insert_time
    load_factor = hs.number_of_values / hs.hash_table_size
    collisions_insert = collisions_after_insert
    collisions_find = collisions_after_find - collisions_after_insert
    avg_collisions_insert = collisions_insert / len(words)
    find_count = accesses_after_find - accesses_after_insert
    avg_collisions_find = collisions_find / float(find_count)
    avg_probe_length = hs.total_probe_length / float(hs.number_of_finds)
    
    results['HashSet'] = {
        'insert': insert_time,
        'find': find_time,
        'size': hs.number_of_values,
        'collisions': hs.number_of_collisions,
        'rehashes': hs.number_of_rehashes,
        'accesses': hs.number_of_accesses,
        'ops_per_sec': ops_per_sec,
        'load_factor': load_factor,
        'avg_coll_insert': avg_collisions_insert,
        'avg_coll_find': avg_collisions_find,
        'avg_probe_length': avg_probe_length
    }
    print("  Insert time: " + str(round(insert_time, 6)) + "s")
    print("  Find time (1000 words): " + str(round(find_time, 6)) + "s")
    print("  Size: " + str(hs.number_of_values))
    print("  Ops/sec: " + str(int(ops_per_sec)))
    print("  Collisions (insert): " + str(collisions_insert))
    print("  Collisions (find): " + str(collisions_find))
    print("  Avg collisions/insert: " + str(round(avg_collisions_insert, 2)))
    print("  Avg collisions/find: " + str(round(avg_collisions_find, 2)))
    print("  Avg probe length: " + str(round(avg_probe_length, 2)))
    print("  Rehashes: " + str(hs.number_of_rehashes))
    print("  Load factor: " + str(round(load_factor, 2)))
    print()
    
    # Summary
    print("=" * 60)
    print("Performance Summary")
    print("=" * 60)
    print("\nStructure            Insert (s)      Find (s)        Ops/sec")
    print("-" * 60)
    for name, data in results.items():
        insert_str = str(round(data['insert'], 6))
        find_str = str(round(data['find'], 6))
        ops_str = str(int(data['ops_per_sec']))
        print(name.ljust(20) + " " + insert_str.ljust(15) + " " + find_str.ljust(15) + " " + ops_str)
    
    # Calculate speedup
    bst_insert = results['BSTree']['insert']
    hash_insert = results['HashSet']['insert']
    bst_find = results['BSTree']['find']
    hash_find = results['HashSet']['find']
    insert_speedup = bst_insert / hash_insert
    find_speedup = bst_find / hash_find
    
    print("\n" + "=" * 60)
    print("HashSet vs BSTree:")
    print("  Insert speedup: " + str(round(insert_speedup, 2)) + "x faster")
    print("  Find speedup: " + str(round(find_speedup, 2)) + "x faster")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    run_benchmarks()
