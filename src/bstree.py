import config

class bstree:
    def __init__(self):
        self.verbose = config.verbose
        self.value = None
        self.left  = None
        self.right = None
        self.height = 0
        self.number_of_comparisons = 0
        # Number of find or insert operations
        self.number_of_executions = 0


        
    def size(self):
        if self.tree():
            if self.left:
                left_size = self.left.size()
            else:
                left_size = 0
            if self.right:
                right_size = self.right.size()
            else:
                right_size = 0
            return 1 + left_size + right_size
        return 0
        
    def tree(self):
        # This counts as a tree if it has a field self.value
        # it should also have sub-trees self.left and self.right
        return hasattr(self, 'value')

    def insert(self, value):
        self.number_of_executions += 1
        self.number_of_comparisons += 1
        if self.tree() and self.value:
            # Check for duplicates and disallow insertion as we implement Hash Set
            if self.value == value:
                return False

            # Insert into left sub-tree
            if value < self.value:
                # If you hit a base node
                if not self.left.tree():
                    self.left = bstree()
                    self.left.value = value
                    self.left.left = bstree()
                    self.left.right = bstree()
                    return True
                # If you hit a regular node
                return self.left.insert(value)
            # Insert into right sub-tree
            else:
                # If you hit a base node
                if not self.right.tree():
                    self.right = bstree()
                    self.right.value = value
                    self.right.left = bstree()
                    self.right.right = bstree()
                    return True
                # If you hit a regular node
                return self.right.insert(value)
        else:
            self.left = bstree()
            self.right = bstree()
            self.value = value
            return True

    def find(self, value):

        self.number_of_executions += 1
        self.number_of_comparisons += 1

        if self.tree() and self.value:
            if self.value and self.value == value:
                return True
            elif self.value and value < self.value:
                return self.left.find(value)
            elif self.value and value > self.value:
                return self.right.find(value)

        return False
                    
    # You can update this if you want
    def print_set(self):
       # We will use preorder traversal to print out tree contents
       tree_contents = []
       def preorder_traversal(inner_self):

           if inner_self and inner_self.tree():
               tree_contents.append(str(inner_self.value))
               preorder_traversal(inner_self.left)
               preorder_traversal(inner_self.right)

       preorder_traversal(self)
       print("These are the contents: " + " ".join(tree_contents))

    def print_stats(self):
        def find_height(inner_self):
            if inner_self and inner_self.tree():
                return 1 + max(find_height(inner_self.left), find_height(inner_self.right))
            else:
                return 0
        height = find_height(self)

        # Division by zero check
        if self.number_of_executions == 0:
            average_comparison_per_execution = 0
        else:
            average_comparison_per_execution =  self.number_of_comparisons / self.number_of_executions
        print("The average number of comparisons per execution: " + str(average_comparison_per_execution))
        print("The height of the tree: " + str(height))
            
            
