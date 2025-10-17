# python-hashset

Efficient implementations of Binary Search Trees and Hash Sets in Python with collision handling and performance benchmarking.

## Documentation-hashset python-hashset

Efficient hash set implementation in Python. Includes custom hash functions, collision resolution, and benchmarking against other data structures.”

Efficient implementations of Binary Search Trees and Hash Sets in Python with collision handling and performance benchmarking.

## Documentation

**For detailed technical documentation** including system architecture, code flows, and how all components work together, see:

[docs/TECHNICAL_DOCUMENTATION.md](docs/TECHNICAL_DOCUMENTATION.md)

This includes:

- Complete code flow explanations
- How the spell checker works
- Data structure implementation details
- System architecture diagrams
- Performance analysis
- Extension guides

## Quick Start

### Running Spell Checker

Using HashSet:

```bash
cd src
python3 speller_hashset.py -d ../data/simple/1/dict ../data/simple/1/infile
```

Using BSTree:

```bash
cd src
python3 speller_bstree.py -d ../data/simple/1/dict ../data/simple/1/infile
```

### Running Tests

```bash
./run_tests.sh
```

Or individually:

```bash
cd tests
python3 test_bstree.py
python3 test_hashset.py
```

### Running Benchmarks

```bash
cd benchmarks
python3 benchmark.py
```

Generate performance graphs (requires matplotlib):

```bash
pip3 install matplotlib
python3 generate_graphs.py
```

## Project Structure

```
python-hashset/
├── src/                    # Source implementations
│   ├── bstree.py          # Binary Search Tree
│   ├── hashset.py         # Hash Set with FNV hashing
│   ├── config.py          # Configuration
│   ├── set_factory.py     # Factory pattern
│   ├── speller.py         # Core spell checking logic
│   ├── speller_bstree.py  # BSTree entry point
│   └── speller_hashset.py # HashSet entry point
├── tests/                  # Unit tests
│   ├── test_bstree.py
│   └── test_hashset.py
├── benchmarks/            # Performance analysis
│   ├── benchmark.py
│   └── generate_graphs.py
├── data/                  # Test datasets
│   ├── simple/            # Basic tests
│   ├── collision_tests/   # Collision scenarios
│   └── large/             # Large dataset (235K words)
└── docs/                  # Documentation
    └── TECHNICAL_DOCUMENTATION.md
```

## Features

### Binary Search Tree

- O(log n) insert and find operations
- Duplicate detection
- Performance statistics

### Hash Set

- O(1) average insert and find
- FNV-1a hash function
- Linear probing collision resolution
- Automatic rehashing at 70% load factor
- Prime-sized hash tables

## Performance

Tested with 235K word dictionary:

| Operation | BSTree | HashSet |
|-----------|--------|---------|
| Insert    | 0.83s  | 0.51s   |
| Find (1000 words) | 0.0013s | 0.0008s |

HashSet is 1.6x faster for both operations.

## Command Line Options

```bash
-d <file>  # Specify dictionary file
-s <size>  # Set initial hash table size
-v         # Verbose mode (-vv, -vvv for more detail)
-h         # Show help
```

## Requirements

- Python 3.x (no external dependencies for core functionality)
- matplotlib (optional, for graph generation)

## Testing

All tests pass:

- BSTree insertion, search, duplicates
- HashSet insertion, search, collisions, rehashing
- Spell checking with both data structures

## Example Output

```bash
$ python3 speller_hashset.py -d ../data/simple/1/dict ../data/simple/1/infile
Spellchecking:

1: twelve

Usage statistics:

Number of Collisions: 0
Number of Rehashes: 0
Average number of collisions per access: 0.0
```
