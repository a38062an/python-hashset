import config


class hashset:
    def __init__(self):
        self.verbose = config.verbose
        self.hash_table_size = config.init_size
        if not self.isPrime(self.hash_table_size):
            self.hash_table_size = self.nextPrime(self.hash_table_size)
        self.hash_table = [None] * self.hash_table_size
        self.number_of_values = 0
        self.number_of_collisions = 0
        self.number_of_rehashes = 0
        self.number_of_accesses = 0
        self.total_probe_length = 0
        self.number_of_finds = 0

    # Helper functions for finding prime numbers
    def isPrime(self, n):
        i = 2
        while (i * i <= n):
            if (n % i == 0):
                return False
            i = i + 1
        return True

    def nextPrime(self, n):
        while (not self.isPrime(n)):
            n = n + 1
        return n

    def hash(self, string):

        # Hash function
        ''' 
        golden_ratio = (5 ** 0.5 - 1) / 2
        hash_value = 0
        for char in string[:10]:
            hash_value = hash_value * 31 + ord(char)


        fractional_part = (hash_value * golden_ratio) % 1
        hash_index = fractional_part * self.hash_table_size
        return round(hash_index)
        '''
        
        hash_value = 14695981039346656037  # FNV offset basis
        for byte in string.encode():
             hash_value ^= byte
             hash_value *= 1099511628211  # FNV prime
        return hash_value
        

       
    def linear_probe(self, hash_index, value):

        original_hash_index = hash_index
        probe_count = 0

        while probe_count < self.hash_table_size:

            hash_index = (original_hash_index + probe_count) % self.hash_table_size         
            #hash_index = (original_hash_index + int(0.5 * probe_count) + int(0.5 * probe_count * probe_count)) % self.hash_table_size
            #print(f"Probe {probe_count}: checking index {hash_index}, found {self.hash_table[hash_index]}")

            # If we find an empty slot
            if self.hash_table[hash_index] is None:
                self.hash_table[hash_index] = value
                self.number_of_values += 1
                return True

            # If the value already exists return
            elif self.hash_table[hash_index] == value:
                return False


            if self.hash_table[hash_index] is not None:
                self.number_of_collisions += 1

            # Continue the probe
            probe_count += 1

        # If nothing is found return
        return False

    def rehash_insertion(self, hash_index, value):
        original_hash_index = hash_index
        probe_count = 0

        # Loop the size of the hash table
        while probe_count < self.hash_table_size:
            #hash_index = (original_hash_index + int(0.5 * probe_count) + int(0.5 * probe_count * probe_count)) % self.hash_table_size
            hash_index = (original_hash_index + probe_count) % self.hash_table_size
            #print(f"Probe {probe_count}: checking index {hash_index}, found {self.hash_table[hash_index]}")

            # If empty slot is found insert
            if self.hash_table[hash_index] is None:
                self.hash_table[hash_index] = value
                self.number_of_values += 1
                return


            probe_count += 1
            # Not sure if this increment below should be here
            self.number_of_collisions += 1



    def rehash(self):

        self.number_of_rehashes += 1
        current_table = self.hash_table
        new_table_size = self.nextPrime(2 * self.hash_table_size)  # Double table and find next prime
        self.hash_table_size = new_table_size
        self.hash_table = [None] * new_table_size
        self.number_of_values = 0
        # old_number_of_collisions = self.number_of_collisions

        '''Reinsert values into table'''
        # Reinsert manually instead of generic
        for old_value in current_table:
            if old_value is not None:
                hash_index = self.hash(old_value)
                self.rehash_insertion(hash_index, old_value)
                #self.insert(old_value)


    def insert(self, value):

        self.number_of_accesses += 1
        load_factor = self.number_of_values / self.hash_table_size

        '''Rehash and Resize if load factor reached'''


        if load_factor >= 0.7:
            self.rehash()

        #self.print_set()

        hash_index = self.hash(value)
        result = self.linear_probe(hash_index, value)
        return result



    def find(self, value):

        self.number_of_accesses += 1
        self.number_of_finds += 1

        hash_index = self.hash(value)

        '''Collision handling with linear probing'''
        original_hash_index = hash_index
        probe_count = 0

        while probe_count < self.hash_table_size:

            hash_index = (original_hash_index + probe_count) % self.hash_table_size
            #print(f"Probe {probe_count}: checking index {hash_index}, found {self.hash_table[hash_index]}")

            # stop early if empty slot is found
            if self.hash_table[hash_index] is None:
                self.total_probe_length += (probe_count + 1)
                return False

            if self.hash_table[hash_index] == value:
                self.total_probe_length += (probe_count + 1)
                return True

            # Count collision when slot is occupied but not a match
            if self.hash_table[hash_index] is not None:
                self.number_of_collisions += 1

            probe_count += 1

        self.total_probe_length += (probe_count + 1)
        return False

    def print_set(self):
        print("Hash Set: ")
        for index in range(self.hash_table_size):
            value = self.hash_table[index]
            if value is not None:
                print(f"{index}: {value}")
            else:
                print(f"{index}: None")

    def print_stats(self):
        print("Number of Collisions: ", self.number_of_collisions)
        print("Number of Rehashes: ", self.number_of_rehashes)
        if self.number_of_accesses == 0:
            number_of_collisions_per_access = 0
        else:
            number_of_collisions_per_access = self.number_of_collisions / self.number_of_accesses
        print("Average number of collisions per access: ", number_of_collisions_per_access)

