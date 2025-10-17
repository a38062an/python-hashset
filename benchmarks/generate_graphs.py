#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import matplotlib.pyplot as plt
import time
from bstree import bstree
from hashset import hashset
import config

def benchmark_varying_sizes():
    """Benchmark data structures with varying input sizes"""
    sizes = [10, 50, 100, 500, 1000, 2000]
    
    bstree_insert_times = []
    hashset_insert_times = []
    bstree_find_times = []
    hashset_find_times = []
    
    for size in sizes:
        words = [f"word{i}" for i in range(size)]
        
        # BSTree insert
        config.verbose = 0
        tree = bstree()
        start = time.time()
        for word in words:
            tree.insert(word)
        bstree_insert_times.append(time.time() - start)
        
        # BSTree find
        start = time.time()
        for word in words[:min(100, len(words))]:
            tree.find(word)
        bstree_find_times.append(time.time() - start)
        
        # HashSet insert
        config.verbose = 0
        config.init_size = 509
        hs = hashset()
        start = time.time()
        for word in words:
            hs.insert(word)
        hashset_insert_times.append(time.time() - start)
        
        # HashSet find
        start = time.time()
        for word in words[:min(100, len(words))]:
            hs.find(word)
        hashset_find_times.append(time.time() - start)
    
    return sizes, bstree_insert_times, hashset_insert_times, bstree_find_times, hashset_find_times

def generate_performance_graphs():
    """Generate performance comparison graphs"""
    print("Generating performance graphs...")
    
    sizes, bst_insert, hs_insert, bst_find, hs_find = benchmark_varying_sizes()
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'graphs')
    os.makedirs(output_dir, exist_ok=True)
    
    # Insert time comparison
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bst_insert, marker='o', label='BSTree', linewidth=2)
    plt.plot(sizes, hs_insert, marker='s', label='HashSet', linewidth=2)
    plt.xlabel('Number of Elements', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.title('Insert Performance Comparison', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    insert_path = os.path.join(output_dir, 'insert_performance.png')
    plt.savefig(insert_path, dpi=300)
    print(f"Saved: {insert_path}")
    plt.close()
    
    # Find time comparison
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bst_find, marker='o', label='BSTree', linewidth=2)
    plt.plot(sizes, hs_find, marker='s', label='HashSet', linewidth=2)
    plt.xlabel('Dataset Size', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.title('Find Performance Comparison (100 lookups)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    find_path = os.path.join(output_dir, 'find_performance.png')
    plt.savefig(find_path, dpi=300)
    print(f"Saved: {find_path}")
    plt.close()
    
    # Combined comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.plot(sizes, bst_insert, marker='o', label='BSTree', linewidth=2)
    ax1.plot(sizes, hs_insert, marker='s', label='HashSet', linewidth=2)
    ax1.set_xlabel('Number of Elements', fontsize=11)
    ax1.set_ylabel('Time (seconds)', fontsize=11)
    ax1.set_title('Insert Performance', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(sizes, bst_find, marker='o', label='BSTree', linewidth=2)
    ax2.plot(sizes, hs_find, marker='s', label='HashSet', linewidth=2)
    ax2.set_xlabel('Dataset Size', fontsize=11)
    ax2.set_ylabel('Time (seconds)', fontsize=11)
    ax2.set_title('Find Performance (100 lookups)', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    combined_path = os.path.join(output_dir, 'combined_performance.png')
    plt.savefig(combined_path, dpi=300)
    print(f"Saved: {combined_path}")
    plt.close()
    
    print(f"\nAll graphs saved to: {output_dir}")

if __name__ == "__main__":
    try:
        import matplotlib
        generate_performance_graphs()
    except ImportError:
        print("Error: matplotlib is not installed.")
        print("Install it with: pip install matplotlib")
        sys.exit(1)
