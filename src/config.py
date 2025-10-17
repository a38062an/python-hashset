from enum import Enum

class SetType(Enum):
    BSTREE = 2,
    HASH = 3

set_type = SetType.HASH
prog_name = "speller_hashset.py"
DEFAULT_DICT_FILE = "sample-dictionary"
verbose = 0
init_size = 7
