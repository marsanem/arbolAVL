import random, math
from datetime import datetime
from trello import TrelloClient
import os
import datetime

def random_data_generator (max_r):
    for i in range(max_r):
        yield random.randint(0, max_r)

class Node():
    def __init__(self, text):
        self.parent = None
        self.leftChild = None
        self.rightChild = None
        self.height = 0
        self.text = text
    
    def __str__(self):
        return self.text+ "(" + str(self.height) + ")"
    
    def is_leaf(self):
        return (self.height == 0)
   
    def max_children_height(self):
        if self.leftChild and self.rightChild:
            return max(self.leftChild.height, self.rightChild.height)
        elif self.leftChild and not self.rightChild:
            return self.leftChild.height
        elif not self.leftChild and  self.rightChild:
            return self.rightChild.height
        else:
            return -1
        
    def balance (self):
        return (self.leftChild.height if self.leftChild else -1) - (self.rightChild.height if self.rightChild else -1)

class AVLTree():
    def __init__(self, *args):
        self.rootNode = None
        self.elements_count = 0
        self.rebalance_count = 0

    def height(self):
        #print('height')
        if self.rootNode:
            return self.rootNode.height
        else:
            return 0
        
    def rebalance (self, node_to_rebalance):
        #print('rebalance')
        self.rebalance_count += 1
        A = node_to_rebalance 
        F = A.parent #allowed to be NULL
        if node_to_rebalance.balance() == -2:
            if node_to_rebalance.rightChild.balance() <= 0:
                """Rebalance, case RRC """
                B = A.rightChild
                C = B.rightChild
                assert (not A is None and not B is None and not C is None)
                A.rightChild = B.leftChild
                if A.rightChild:
                    A.rightChild.parent = A
                B.leftChild = A
                A.parent = B                                                               
                if F is None:                                                              
                   self.rootNode = B 
                   self.rootNode.parent = None                                                   
                else:                                                                        
                   if F.rightChild == A:                                                          
                       F.rightChild = B                                                                  
                   else:                                                                      
                       F.leftChild = B                                                                   
                   B.parent = F 
                self.recompute_heights (A) 
                self.recompute_heights (B.parent)                                                                                         
            else:
                """Rebalance, case RLC """
                B = A.rightChild
                C = B.leftChild
                assert (not A is None and not B is None and not C is None)
                B.leftChild = C.rightChild
                if B.leftChild:
                    B.leftChild.parent = B
                A.rightChild = C.leftChild
                if A.rightChild:
                    A.rightChild.parent = A
                C.rightChild = B
                B.parent = C                                                               
                C.leftChild = A
                A.parent = C                                                             
                if F is None:                                                             
                    self.rootNode = C
                    self.rootNode.parent = None                                                    
                else:                                                                        
                    if F.rightChild == A:                                                         
                        F.rightChild = C                                                                                     
                    else:                                                                      
                        F.leftChild = C
                    C.parent = F
                self.recompute_heights (A)
                self.recompute_heights (B)
        else:
            assert(node_to_rebalance.balance() == +2)
            if node_to_rebalance.leftChild.balance() >= 0:
                B = A.leftChild
                C = B.leftChild
                """Rebalance, case LLC """
                assert (not A is None and not B is None and not C is None)
                A.leftChild = B.rightChild
                if (A.leftChild): 
                    A.leftChild.parent = A
                B.rightChild = A
                A.parent = B
                if F is None:
                    self.rootNode = B
                    self.rootNode.parent = None                    
                else:
                    if F.rightChild == A:
                        F.rightChild = B
                    else:
                        F.leftChild = B
                    B.parent = F
                self.recompute_heights (A)
                self.recompute_heights (B.parent) 
            else:
                B = A.leftChild
                C = B.rightChild 
                """Rebalance, case LRC """
                assert (not A is None and not B is None and not C is None)
                A.leftChild = C.rightChild
                if A.leftChild:
                    A.leftChild.parent = A
                B.rightChild = C.leftChild
                if B.rightChild:
                    B.rightChild.parent = B
                C.leftChild = B
                B.parent = C
                C.rightChild = A
                A.parent = C
                if F is None:
                   self.rootNode = C
                   self.rootNode.parent = None
                else:
                   if (F.rightChild == A):
                       F.rightChild = C
                   else:
                       F.leftChild = C
                   C.parent = F
                self.recompute_heights (A)
                self.recompute_heights (B)
            
    def recompute_heights (self, start_from_node):
        #print('recompute_heights')
        changed = True
        node = start_from_node
        while node and changed:
            old_height = node.height
            node.height = (node.max_children_height() + 1 if (node.rightChild or node.leftChild) else 0)
            changed = node.height != old_height
            node = node.parent
       
    def add_as_child (self, parent_node, child_node,side):
        #print('add_as_child')
        node_to_rebalance = None
        if side == 0:
            if not parent_node.leftChild:
                parent_node.leftChild = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:
                    node = parent_node
                    while node:
                        node.height = node.max_children_height() + 1
                        if not node.balance () in [-1, 0, 1]:
                            node_to_rebalance = node
                            break #we need the one that is furthest from the root
                        node = node.parent     
            else:
                self.add_as_child(parent_node.leftChild, child_node,0)
        else:
            if not parent_node.rightChild:
                parent_node.rightChild = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:
                    node = parent_node
                    while node:
                        node.height = node.max_children_height() + 1
                        if not node.balance () in [-1, 0, 1]:
                            node_to_rebalance = node
                            break #we need the one that is furthest from the root
                        node = node.parent       
            else:
                self.add_as_child(parent_node.rightChild, child_node,1)
        
        if node_to_rebalance:
            self.rebalance (node_to_rebalance)

    def add_as_child2(self,text, parent_node,side):
        child_node = Node (text)
        #print('add_as_child')
        node_to_rebalance = None
        if side == 0:
            if not parent_node.leftChild:
                parent_node.leftChild = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:
                    node = parent_node
                    while node:
                        node.height = node.max_children_height() + 1
                        if not node.balance () in [-1, 0, 1]:
                            node_to_rebalance = node
                            break #we need the one that is furthest from the root
                        node = node.parent
        else:
            if not parent_node.rightChild:
                parent_node.rightChild = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:
                    node = parent_node
                    while node:
                        node.height = node.max_children_height() + 1
                        if not node.balance () in [-1, 0, 1]:
                            node_to_rebalance = node
                            break #we need the one that is furthest from the root
                        node = node.parent
    
        if node_to_rebalance:
            self.rebalance (node_to_rebalance)

    def insert (self, text, side):
        new_node = Node (text)
        if not self.rootNode:
            self.rootNode = new_node
        else:
            self.elements_count += 1
            self.add_as_child (self.rootNode, new_node, side)
      
    def find_biggest(self, start_node):
        #print('find_biggest')
        node = start_node
        while node.rightChild:
            node = node.rightChild
        return node 
    
    def find_smallest(self, start_node):
        node = start_node
        while node.leftChild:
            node = node.leftChild
        return node
     
    def preorder(self, node, retlst = None):
        if retlst is None:
            retlst = []
        retlst += [node.text]
        if node.leftChild:
            retlst = self.preorder(node.leftChild, retlst) 
        if node.rightChild:
            retlst = self.preorder(node.rightChild, retlst)
        return retlst         
           
    def inorder(self, node, retlst = None):
        if retlst is None:
            retlst = [] 
        if node.leftChild:
            retlst = self.inorder(node.leftChild, retlst)
        retlst += [node.text]
        if node.rightChild:
            retlst = self.inorder(node.rightChild, retlst)
        return retlst
        
    def postorder(self, node, retlst = None):
        if retlst is None:
            retlst = []
        if node.leftChild:
            retlst = self.postorder(node.leftChild, retlst) 
        if node.rightChild:
            retlst = self.postorder(node.rightChild, retlst)
        retlst += [node.text]
        return retlst  
    
    def as_list (self, pre_in_post):
        if not self.rootNode:
            return []
        if pre_in_post == 0:
            return self.preorder (self.rootNode)
        elif pre_in_post == 1:
            return self.inorder (self.rootNode)
        elif pre_in_post == 2:
            return self.postorder (self.rootNode)
          
    def find(self, key):
        #print('find')
        return self.find_in_subtree (self.rootNode, key )
    
    def find_in_subtree (self,  node, key):
        #print('find_in_subtree')
        if node is None:
            return None  # key not found
        if key < node.key:
            return self.find_in_subtree(node.leftChild, key)
        elif key > node.key:
            return self.find_in_subtree(node.rightChild, key)
        else:  # key is equal to node key
            return node
    
    def remove (self, key):
        #print('remove')
        # first find
        node = self.find(key)
        
        if not node is None:
            self.elements_count -= 1
            
            #     There are three cases:
            # 
            #     1) The node is a leaf.  Remove it and return.
            # 
            #     2) The node is a branch (has only 1 child). Make the pointer to this node 
            #        point to the child of this node.
            # 
            #     3) The node has two children. Swap items with the successor
            #        of the node (the smallest item in its right subtree) and
            #        delete the successor from the right subtree of the node.
            if node.is_leaf():
                self.remove_leaf(node)
            elif (bool(node.leftChild)) ^ (bool(node.rightChild)):  
                self.remove_branch (node)
            else:
                assert (node.leftChild) and (node.rightChild)
                self.swap_with_successor_and_remove (node)
            
    def remove_leaf (self, node):
        #print('remove_leaf')
        parent = node.parent
        if (parent):
            if parent.leftChild == node:
                parent.leftChild = None
            else:
                assert (parent.rightChild == node)
                parent.rightChild = None
            self.recompute_heights(parent)
        else:
            self.rootNode = None
        del node
        # rebalance
        node = parent
        while (node):
            if not node.balance() in [-1, 0, 1]:
                self.rebalance(node)
            node = node.parent
        
        
    def remove_branch (self, node):
        #print('remove_branch')
        parent = node.parent
        if (parent):
            if parent.leftChild == node:
                parent.leftChild = node.rightChild or node.leftChild
            else:
                assert (parent.rightChild == node)
                parent.rightChild = node.rightChild or node.leftChild
            if node.leftChild:
                node.leftChild.parent = parent
            else:
                assert (node.rightChild)
                node.rightChild.parent = parent 
            self.recompute_heights(parent)
        del node
        # rebalance
        node = parent
        while (node):
            if not node.balance() in [-1, 0, 1]:
                self.rebalance(node)
            node = node.parent
        
    def swap_with_successor_and_remove (self, node):
        #print('swap_succesor_and_remove')
        successor = self.find_smallest(node.rightChild)
        self.swap_nodes (node, successor)
        assert (node.leftChild is None)
        if node.height == 0:
            self.remove_leaf (node)
        else:
            self.remove_branch (node)
            
    def swap_nodes (self, node1, node2):
        #print('swap_nodes')
        assert (node1.height > node2.height)
        parent1 = node1.parent
        leftChild1 = node1.leftChild
        rightChild1 = node1.rightChild
        parent2 = node2.parent
        assert (not parent2 is None)
        assert (parent2.leftChild == node2 or parent2 == node1)
        leftChild2 = node2.leftChild
        assert (leftChild2 is None)
        rightChild2 = node2.rightChild
        
        # swap heights
        tmp = node1.height 
        node1.height = node2.height
        node2.height = tmp
       
        if parent1:
            if parent1.leftChild == node1:
                parent1.leftChild = node2
            else:
                assert (parent1.rightChild == node1)
                parent1.rightChild = node2
            node2.parent = parent1
        else:
            self.rootNode = node2
            node2.parent = None
            
        node2.leftChild = leftChild1
        leftChild1.parent = node2
        node1.leftChild = leftChild2 # None
        node1.rightChild = rightChild2
        if rightChild2:
            rightChild2.parent = node1 
        if not (parent2 == node1):
            node2.rightChild = rightChild1
            rightChild1.parent = node2
            
            parent2.leftChild = node1
            node1.parent = parent2
        else:
            node2.rightChild = node1
            node1.parent = node2           
           
    # use for debug only and only with small trees            
    def out(self, start_node = None):
        if start_node == None:
            start_node = self.rootNode
        space_symbol = "*"
        spaces_count = 160
        out_string = ""
        initial_spaces_string  = space_symbol * spaces_count * 1 + "\n"
        if not start_node:
            return "AVLTree is empty"
        else:
            level = [start_node]
            while (len([i for i in level if (not i is None)])>0):
                level_string = initial_spaces_string
                for i in range(len(level)):
                    j = (int)((i+1)* spaces_count / (len(level)+1))
                    level_string = level_string[:j] + (str(level[i]) if level[i] else space_symbol) + level_string[j+1:]
                level_next = []
                for i in level:
                    level_next += ([i.leftChild, i.rightChild] if i else [None, None])
                level = level_next
                out_string += level_string
        return out_string

class ImportText():
    
    def makeList(self,listName):
        import csv
        f = open(listName,'r')
        return [line.rstrip() for line in f]

    def convertListToTree(self,listName):
        import csv
        f = open(listName,'r')
        listText = [line.rstrip() for line in f]
        lengthList = len(listText)
        resultTree = AVLTree();
        for i in listText:
            if resultTree.rootNode == None:
                resultTree.insert(i,0)
                #print(lengthList)
                #print(resultTree.elements_count)
            else:
                resultTree.rootNode.text
                currentNode = resultTree.rootNode
                done = True
                while(done):
                    moreImportant = (input(i+" is more important than "+currentNode.text+" y/n "))
                    if moreImportant == "y":
                        if(currentNode.rightChild == None):
                            resultTree.add_as_child2(i,currentNode,1)
                            done = False
                        else:
                            currentNode = currentNode.rightChild
                    else:
                        if(currentNode.leftChild == None):
                            resultTree.add_as_child2(i,currentNode,0)
                            done = False
                        else:
                            currentNode = currentNode.leftChild
                #print(resultTree.as_list(1))
                #print(resultTree.rebalance_count)
                #print (resultTree.out())
        return resultTree

class connectionJASON():
    
    def setUp(self):
        self._trello = TrelloClient(api_key='f8fd231446c1fd27f49e0d8f933252f3',
                                api_secret='338b8eef2cc489ce5cfc9f2252c73f5cf51b44a41cc6cb790be20feb9ed19f2d',
                                token='8004f00bc94627ac6eb98333492a76315821ed06e9d04eec4b6480d1f575758b',
                                token_secret='a528cdd05a0dd7314f45995fdf457c45')
                                
    def getCards(self):
        boards = [board for board in self._trello.list_boards() if 'Proy Industria' in str(board.name) ]
        board = boards[0]
        cards = board.get_cards()
        return cards


    def arrangeCards(self,cards):
        resultTree = AVLTree();
        for i in cards:
            if resultTree.rootNode == None:
                resultTree.insert(i,0)
            else:
                #resultTree.rootNode.text
                currentNode = resultTree.rootNode
                done = True
                while(done):
                    moreImportant = (input(str(i)+" is more important than "+str(currentNode.text)+" y/n "))
                    if moreImportant == "y":
                        if(currentNode.rightChild == None):
                            resultTree.add_as_child2(i,currentNode,1)
                            done = False
                        else:
                            currentNode = currentNode.rightChild
                    else:
                        if(currentNode.leftChild == None):
                            resultTree.add_as_child2(i,currentNode,0)
                            done = False
                        else:
                            currentNode = currentNode.leftChild
                print(resultTree.as_list(1))
                #print(resultTree.rebalance_count)
                #print (resultTree.out())
        return resultTree

    def sendCards(self,cards):
        boards = [board for board in self._trello.list_boards() if 'Proy Industria' in str(board.name) ]
        board = boards[0]
        cards = board.get_cards()
        return cards



if __name__ == "__main__":
    """check empty tree creation"""
    #g = ImportText()
    #a = g.convertListToTree('list.txt')
    #print (a.as_list(1))
    #print (a.out())

    c = connectionJASON()
    c.setUp()
    d = c.getCards()
    c.arrangeCards(d)




