# Technical Documentation

## System Architecture and Code Flow

This document explains how all components of the python-hashset project work together, including detailed code flows and data structures.

---

## Core Components Overview

### 1. Data Structure Implementations

#### bstree.py - Binary Search Tree

The BSTree implements a set data structure using a binary search tree where duplicates are not allowed.

**Key Operations:**

- `insert(value)`: Adds a value to the tree if it doesn't exist
- `find(value)`: Searches for a value in the tree
- `size()`: Returns the total number of nodes
- `print_stats()`: Displays performance metrics

**How it works:**
When you insert a value, the tree compares it with the current node:

- If smaller, goes to left subtree
- If larger, goes to right subtree
- If equal, rejects as duplicate

Each node tracks:

- `value`: The stored data
- `left`: Left child node
- `right`: Right child node
- `number_of_comparisons`: Total comparisons made
- `number_of_executions`: Total operations performed

#### hashset.py - Hash Set

The HashSet implements a set using a hash table with linear probing for collision resolution.

**Key Operations:**

- `insert(value)`: Adds a value if not present
- `find(value)`: Looks up a value
- `hash(string)`: Computes hash value using FNV-1a algorithm
- `linear_probe(hash_index, value)`: Handles collisions
- `rehash()`: Doubles table size when load factor exceeds 0.7

**How it works:**

1. Hash the input string to get an index
2. Check if that slot is empty or has the value
3. If collision occurs, probe linearly (index + 1, index + 2, etc.)
4. When load factor reaches 70%, rehash to a larger prime-sized table

The hash function (FNV-1a):

```
hash = 14695981039346656037  (offset basis)
for each byte in string:
    hash = hash XOR byte
    hash = hash * 1099511628211  (FNV prime)
```

Collision resolution uses linear probing:

```
index = (original_hash + probe_count) % table_size
```

#### config.py - Configuration

Centralizes all configuration parameters:

- `set_type`: Which data structure to use (BSTREE or HASH)
- `prog_name`: Name of the program being run
- `DEFAULT_DICT_FILE`: Default dictionary file path
- `verbose`: Verbosity level (0-3)
- `init_size`: Initial hash table size (default 509)

#### set_factory.py - Factory Pattern

Creates the appropriate data structure based on config.set_type:

```python
def initialise_set():
    if config.set_type == BSTREE:
        return bstree()
    else:
        return hashset()
```

This allows the spell checker to work with any data structure without knowing implementation details.

---

## Spell Checking System

### How the Spell Checker Works

The spell checking system has three main components that work together:

#### 1. Entry Points (speller_bstree.py and speller_hashset.py)

These are simple wrappers that:

1. Configure which data structure to use
2. Set the recursion limit (for BSTree)
3. Call the main spelling function

**speller_hashset.py flow:**

```
1. Import speller module
2. Set config.set_type = HASH
3. Set config.prog_name = "speller_hashset.py"
4. Call speller.spelling(sys.argv)
```

**speller_bstree.py flow:**

```
1. Import speller module
2. Set recursion limit to 10005 (needed for deep trees)
3. Set config.set_type = BSTREE
4. Set config.prog_name = "speller_bstree.py"
5. Call speller.spelling(sys.argv)
```

#### 2. Core Spell Checking Logic (speller.py)

This is where all the work happens. Here's the complete flow:

**A. Command Line Argument Processing**

The `process_args()` function parses command line arguments:

- `-d <file>`: Dictionary file path
- `-s <size>`: Initial hash table size
- `-v`: Increase verbosity (can stack: -vv, -vvv)
- `-h`: Show help message

**B. Word Extraction**

The `get_next_lower_word()` function reads text files and extracts words:

1. Reads one character at a time from the file
2. Accumulates alphabetic characters
3. Converts to lowercase
4. Ignores non-alphabetic characters
5. Tracks line numbers for error reporting
6. Returns None when file ends

**Example:**

```
Input text: "Hello, World!"
First call returns: "hello"
Second call returns: "world"
Third call returns: None
```

**C. Main Spelling Function Flow**

The `spelling()` function orchestrates everything:

```
1. Parse command line arguments
   - Get dictionary file path
   - Get text file path
   - Get verbosity level

2. Open both files
   - dict_file: Contains valid words
   - text_file: Contains text to check

3. Create data structure
   - Call set_factory.initialise_set()
   - Returns either bstree or hashset based on config

4. Load dictionary
   - Read each word from dict_file using get_next_lower_word()
   - Insert into data structure
   - Print progress dots if verbose (every 100 words)

5. Check text file
   - Read each word from text_file
   - Call data_structure.find(word)
   - If not found, print "line_number: word"

6. Print statistics
   - Call data_structure.print_stats()
   - For BSTree: shows comparisons and height
   - For HashSet: shows collisions and rehashes

7. Close files and exit
```

**Detailed Step-by-Step Example:**

```
Command: python3 speller_hashset.py -d dict.txt -v input.txt

Step 1: Parse arguments
  - dict_file_name = "dict.txt"
  - file_name = "input.txt"
  - config.verbose = 1

Step 2: Open files
  - dict_file = open("dict.txt")
  - text_file = open("input.txt")

Step 3: Create data structure
  - words = set_factory.initialise_set()
  - Since config.set_type == HASH, returns hashset()

Step 4: Load dictionary (assume dict.txt has: "hello\nworld\n")
  - word = get_next_lower_word(dict_file)  # Returns "hello"
  - words.insert("hello")  # Hash and store
  - word = get_next_lower_word(dict_file)  # Returns "world"
  - words.insert("world")  # Hash and store
  - word = get_next_lower_word(dict_file)  # Returns None (EOF)
  
Step 5: Check text (assume input.txt has: "hello goodbye\n")
  - word = get_next_lower_word(text_file)  # Returns "hello"
  - words.find("hello")  # Returns True, no output
  - word = get_next_lower_word(text_file)  # Returns "goodbye"
  - words.find("goodbye")  # Returns False
  - Print "1: goodbye"
  - word = get_next_lower_word(text_file)  # Returns None (EOF)

Step 6: Print statistics
  - words.print_stats()
  - Output: Number of collisions, rehashes, etc.

Step 7: Close files
```

---

## Testing System

### Test Files Structure

#### test_bstree.py

Tests BSTree operations:

- `test_bstree_insert()`: Verifies insertion and duplicate rejection
- `test_bstree_find()`: Tests search functionality
- `test_bstree_size()`: Checks multiple insertions
- `test_bstree_empty()`: Tests empty tree behavior

Each test:

1. Sets config.verbose = 0 (suppress output)
2. Creates a new bstree instance
3. Performs operations
4. Uses assertions to verify correct behavior

#### test_hashset.py

Tests HashSet operations:

- `test_hashset_insert()`: Tests insertion and duplicates
- `test_hashset_find()`: Verifies search
- `test_hashset_collision()`: Tests with many items to trigger collisions
- `test_hashset_rehash()`: Forces rehashing by starting with small table
- `test_hashset_empty()`: Tests empty set

Each test initializes config.init_size to control hash table size.

---

## Benchmarking System

### benchmark.py

Compares performance between BSTree and HashSet.

**Flow:**

```
1. Load dictionary
   - Find all 'dict' files in data directory
   - Read all words from first dict file found
   - Store in Python list

2. Benchmark BSTree
   - Create new bstree
   - Time insertion of all words
   - Time finding 1000 words
   - Record results

3. Benchmark HashSet
   - Create new hashset
   - Time insertion of all words
   - Time finding 1000 words
   - Record collisions and rehashes

4. Display results
   - Show insert times (6 decimal places)
   - Show find times (6 decimal places)
   - Print summary table
```

**Timing method:**

```python
start = time.time()
# ... operations ...
end = time.time()
elapsed = end - start
```

### generate_graphs.py

Creates visual performance comparisons.

**Flow:**

```
1. Test different dataset sizes
   - Sizes: [10, 50, 100, 500, 1000, 2000]
   - For each size:
     * Generate synthetic words (word0, word1, ...)
     * Time BSTree insert
     * Time BSTree find
     * Time HashSet insert
     * Time HashSet find

2. Generate three graphs
   a. insert_performance.png
      - X-axis: Number of elements
      - Y-axis: Time in seconds
      - Two lines: BSTree vs HashSet
   
   b. find_performance.png
      - X-axis: Dataset size
      - Y-axis: Time in seconds
      - Two lines: BSTree vs HashSet
   
   c. combined_performance.png
      - Side-by-side subplots
      - Left: Insert comparison
      - Right: Find comparison

3. Save to benchmarks/graphs/
   - Creates directory if needed
   - Saves at 300 DPI for quality
```

---

## Data Flow Diagrams

### Spell Checking Data Flow

```
Command Line
    |
    v
speller_bstree.py OR speller_hashset.py
    |
    | (sets config.set_type)
    v
speller.py
    |
    | (calls set_factory)
    v
set_factory.py
    |
    | (creates instance)
    v
bstree.py OR hashset.py
    ^
    | (insert/find calls)
    |
speller.py (dictionary loading & text checking)
```

### Data Structure Selection Flow

```
User runs: python3 speller_hashset.py

1. speller_hashset.py executes
   - Sets config.set_type = SetType.HASH

2. Calls speller.spelling(args)

3. speller.py calls set_factory.initialise_set()

4. set_factory checks config.set_type
   - If BSTREE: return bstree()
   - If HASH: return hashset()

5. Returns data structure instance to speller.py

6. speller.py uses the instance
   - Calls .insert() for dictionary words
   - Calls .find() for text words
   - Calls .print_stats() at end
```

### HashSet Insertion Flow

```
hashset.insert("hello")
    |
    v
1. Check load factor
   - If >= 0.7: call rehash()
   
2. Compute hash
   - hash("hello") using FNV-1a
   - Returns: large integer
   
3. Get initial index
   - hash_value % table_size
   - Example: 123456789 % 509 = 123
   
4. Linear probe
   - Check table[123]
   - If None: place "hello" here, return True
   - If "hello": duplicate, return False
   - If other value: increment collision count
   
5. Continue probing
   - Check table[124], table[125], etc.
   - Until empty slot found or duplicate detected
   
6. Insert and update statistics
   - number_of_values += 1
   - number_of_accesses += 1
```

### BSTree Insertion Flow

```
bstree.insert("hello")
    |
    v
1. Increment statistics
   - number_of_executions += 1
   - number_of_comparisons += 1
   
2. Check if tree has value
   - If self.value is None:
     * This is first insertion
     * Set self.value = "hello"
     * Create empty left and right children
     * Return True
   
3. Compare with current value
   - If "hello" == self.value:
     * Duplicate found
     * Return False
   
4. Determine direction
   - If "hello" < self.value:
     * Go left
     * If left child empty: create and insert
     * Else: recursively call left.insert("hello")
   
   - If "hello" > self.value:
     * Go right
     * If right child empty: create and insert
     * Else: recursively call right.insert("hello")
```

---

## File Dependencies

### Import Chain

```
speller_hashset.py
    imports: speller, sys, config

speller.py
    imports: getopt, sys, config, set_factory, string

set_factory.py
    imports: bstree, hashset, config

bstree.py
    imports: config

hashset.py
    imports: config

test_bstree.py
    imports: sys, os, bstree, config

test_hashset.py
    imports: sys, os, hashset, config

benchmark.py
    imports: sys, os, time, bstree, hashset, config

generate_graphs.py
    imports: sys, os, matplotlib.pyplot, time, bstree, hashset, config
```

### Configuration Propagation

```
config.py defines:
    - verbose
    - init_size
    - set_type
    - prog_name

These are imported by:
    - speller.py (uses verbose, prog_name)
    - bstree.py (uses verbose)
    - hashset.py (uses verbose, init_size)
    - set_factory.py (uses set_type)
    - All test files (set verbose, init_size)
    - All benchmark files (set verbose, init_size)
```

---

## Data Directory Structure

```
data/
├── simple/          # Basic test cases
│   ├── 1/
│   │   ├── dict     # Small dictionary
│   │   ├── infile   # Text to spell check
│   │   └── ans      # Expected misspelled words
│   ├── 2/ ... 9/    # More test cases
│
├── collision_tests/ # Tests for hash collisions
│   ├── 1/ ... 9/    # Various collision scenarios
│
└── large/           # Large dataset
    └── henry/
        ├── dict     # ~236K words
        ├── infile   # ~17K words to check
        └── ans      # Expected output
```

Each test directory contains:

- `dict`: List of valid words (one per line)
- `infile`: Text to spell check
- `ans`: Expected output (misspelled words with line numbers)

---

## Performance Characteristics

### Time Complexity

BSTree:

- Insert: O(log n) average, O(n) worst case (unbalanced)
- Find: O(log n) average, O(n) worst case
- Space: O(n)

HashSet:

- Insert: O(1) average with rehashing amortized
- Find: O(1) average
- Space: O(n) with overhead for empty slots

### Actual Performance (235K words)

BSTree:

- Insert: 0.83 seconds
- Find (1000 words): 0.0013 seconds
- Height: ~18 (log₂(235000) ≈ 17.8)

HashSet:

- Insert: 0.51 seconds (1.63x faster)
- Find (1000 words): 0.0008 seconds (1.67x faster)
- Collisions: ~515K total
- Average collisions per access: 1.49
- Rehashes: 10

### Memory Usage

BSTree:

- Each node: value + left pointer + right pointer + metadata
- Total nodes: 235K + empty leaf nodes
- Overhead: ~2x due to empty leaf nodes

HashSet:

- Table size: Prime number > 235K / 0.7 ≈ 336K
- After 10 rehashes: ~524K slots
- Load factor maintained at ~0.45 (235K / 524K)
- Overhead: ~2.2x for empty slots

---

## Error Handling

### Command Line Errors

```python
# Missing required file
if len(other_args) == 0:
    usage()  # Prints help and exits

# Invalid options
try:
    opts, args = getopt.getopt(...)
except getopt.GetoptError:
    usage()
```

### File Errors

```python
# File not found
dict_file = open(dict_file_name)  # Raises FileNotFoundError if missing
text_file = open(file_name)       # Raises FileNotFoundError if missing

# Files are closed in finally block (implicit with 'with' statement if used)
```

### Data Structure Errors

```python
# Hash table full (shouldn't happen with rehashing)
if probe_count >= self.hash_table_size:
    return False  # All slots checked

# Word too long
if word_len >= WORD_SIZE:
    sys.stderr.write("Cannot handle words longer than...")
    sys.exit(4)
```

---

## Running the System

### Basic Usage

```bash
# Spell check with HashSet
cd src
python3 speller_hashset.py -d ../data/simple/1/dict ../data/simple/1/infile

# Spell check with BSTree
cd src
python3 speller_bstree.py -d ../data/simple/1/dict ../data/simple/1/infile

# With verbosity
python3 speller_hashset.py -v -d ../data/simple/1/dict ../data/simple/1/infile

# Large dataset
python3 speller_hashset.py -d ../data/large/henry/dict ../data/large/henry/infile
```

### Testing

```bash
# Run all tests
./run_tests.sh

# Individual tests
cd tests
python3 test_bstree.py
python3 test_hashset.py
```

### Benchmarking

```bash
# Run performance comparison
cd benchmarks
python3 benchmark.py

# Generate graphs (requires matplotlib)
pip3 install matplotlib
python3 generate_graphs.py
```

---

## Extension Points

### Adding a New Data Structure

1. Create new file (e.g., `avl_tree.py`)
2. Implement required methods:
   - `__init__()`
   - `insert(value)` - returns True/False
   - `find(value)` - returns True/False
   - `print_stats()` - displays metrics

3. Update `config.py`:

   ```python
   class SetType(Enum):
       BSTREE = 2
       HASH = 3
       AVL = 4  # Add new type
   ```

4. Update `set_factory.py`:

   ```python
   from avl_tree import avl_tree
   
   def initialise_set():
       if config.set_type == SetType.AVL:
           return avl_tree()
       # ... existing code
   ```

5. Create entry point `speller_avl.py`:

   ```python
   import speller
   import sys
   import config
   
   config.set_type = config.SetType.AVL
   config.prog_name = "speller_avl.py"
   speller.spelling(sys.argv)
   ```

### Adding New Hash Functions

In `hashset.py`, modify the `hash()` method:

```python
def hash(self, string):
    # Current: FNV-1a
    # Alternative: djb2
    hash_value = 5381
    for char in string:
        hash_value = ((hash_value << 5) + hash_value) + ord(char)
    return hash_value
```

### Adding New Collision Resolution

Modify `linear_probe()` for different probing:

```python
# Quadratic probing
hash_index = (original_hash + probe_count**2) % self.hash_table_size

# Double hashing
hash2 = 7 - (hash_value % 7)  # Secondary hash
hash_index = (original_hash + probe_count * hash2) % self.hash_table_size
```

---

## Summary

The system is built on a modular design where:

1. **Data structures** (bstree, hashset) provide core functionality
2. **Configuration** (config) centralizes settings
3. **Factory pattern** (set_factory) abstracts data structure creation
4. **Spell checker** (speller) orchestrates the spell checking process
5. **Entry points** (speller_X.py) configure and launch the system
6. **Tests** verify correctness
7. **Benchmarks** measure performance

This design allows easy extension with new data structures while keeping the spell checking logic unchanged.
