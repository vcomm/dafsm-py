import time
import asyncio
from mngeng import *

print(time.time(), ": Welcome:", 0)


# Python program to do inorder traversal without recursion and
# without stack Morris inOrder Traversal

# A binary tree node
class Node:

    # Constructor to create a new node
    def __init__(self, data):
        self.data = data
        self.last = self
        self.parent = None
        self.left = None
        self.right = None

    def step(self, node, visited):
        if node is None:
            return node
        else:
            if node not in visited:
                visited.append(node)
                print("Visit: ", node.data)
            elif node.left is not None and node.left not in visited:
                #node = self.step(node.left, visited)
                node = node.left
            elif node.right is not None and node.right not in visited:
                #node = self.step(node.right, visited)
                node = node.right
            else:
                node = node.parent
            return node

    def push(self, node):
        if node is None:
            return self.last
        else:
            if self.last.left is None:
                self.last = self.last.left = node
            elif self.last.right is None:
                self.last = self.last.right = node
            else:
                self.last = self.push(self.last.parent)
            return self.last

    def walk(self, current, runner):
        if current is None:
            return current
        else:
            if current.left is None:
                print(runner, "inorder: ", current.data)
                current = current.right
            else:
                # Find the inorder predecessor of current
                pre = current.left
                while pre.right is not None and pre.right != current:
                    pre = pre.right

                # Make current as right child of its inorder predecessor
                if pre.right is None:
                    pre.right = current
                    current = current.left

                # Revert the changes made in if part to restore the
                # original tree i.e., fix the right child of predecessor
                else:
                    pre.right = None
                    print(runner, "inorder: ", current.data)
                    current = current.right

            return current


# Iterative function for inorder tree traversal
def MorrisTraversal(root):
    # Set current to root of binary tree
    current = root

    while current is not None:

        if current.left is None:
            print(current.data)
            current = current.right
        else:
            # Find the inorder predecessor of current
            pre = current.left
            while pre.right is not None and pre.right != current:
                pre = pre.right

            # Make current as right child of its inorder predecessor
            if pre.right is None:
                pre.right = current
                current = current.left

            # Revert the changes made in if part to restore the
            # original tree i.e., fix the right child of predecessor
            else:
                pre.right = None
                print(current.data)
                current = current.right

            # Driver program to test the above function


""" 
Constructed binary tree is 
		 1 
		/ \ 
	   2   3 
	 /  \   \
    4    5   6
          \  /
           8 7
"""
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.parent = root.right.parent = root
root.left.left = Node(4)
root.left.right = Node(5)
root.left.left.parent = root.left.right.parent = root.left
root.right.right = Node(6)
root.right.right.parent = root.right
root.right.right.left = Node(7)
root.right.right.left.parent = root.right.right
root.left.right.right = Node(8)
root.left.right.right.parent = root.left.right

root.last = root.right.right.left
root.push(Node(9))

visit = []
current = root

while current is not None:
    current = root.step(current, visit)

"""
fast = slow = root
while (slow or fast) is not None:
    if (slow and fast) is not None and (fast.data == slow.data):
        print(": Detect cycle:", slow.data, fast.data)
        
    if slow is not None:
        print(": Slow Current:", slow.data)
        slow = root.walk(slow, 'Slow')
        
    if fast is not None:
        print(": Fast Current:", fast.data)
        fast = root.walk(root.walk(fast, 'Fast'), 'Fast')
"""

# MorrisTraversal(root)


# This code is contributed by Naveen Aili
