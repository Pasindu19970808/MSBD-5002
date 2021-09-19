from collections import Counter

test = {}
test[1] = ['A','B']
test[2] = ['B','C','D']
test[3] = ['A','C','D','E']
test[4] = ['A','D','E']
test[5] = ['A','B','C']
test


class Node:
    def __init__(self,name,frequency,parent,parent_obj = None):
        self.name = name
        self.count = frequency
        self.parent_name = parent
        self.parent = parent_obj
        self.children = []
        self.children_label = []
        self.leaf = False

    def increment(self):
        self.count += 1

#This function accepts a dictionary of transaction where the key is the Transaction ID and values are the list of items in that transaction
def get_item_frequency(transaction_dict):
    count = Counter()
    for transaction in transaction_dict:
        count.update(transaction_dict[transaction])
    return transaction_dict,count
#This function takes the result of function "get_item_frequency" and removes all items below the support value from the transaction dictionary
def remove_items_below_sup(transaction_dict,count,support):
    final_counts = {i[0]:i[1] for i in sorted(count.items(), key = lambda x: x[1],reverse=True) if i[1] >= support}
    final_counts_idx_order = dict(zip(final_counts.keys(),range(len(final_counts.keys()))))
    for transaction in transaction_dict:
        transaction_dict[transaction] = sorted([i for i in transaction_dict[transaction] if (i in final_counts.keys())],key = lambda x: final_counts_idx_order[x])
    return transaction_dict,final_counts, final_counts_idx_order

#traverse one transaction
def traverse_one_transaction(transaction,root_node,currentidx,start = False):
    if  (currentidx < len(transaction)) and (len(transaction) >= 1):
        # If we are just starting a new transaction update, then Start = True 
        # And if the first transaction is not in the root_node.children_label, 
        # It means that it is a new path. REMEMBER that here the root_node.name is #"Null" meaning that we are at the root still
        if (start is True) and (transaction[currentidx] not in root_node.children_label):
            child_node = Node(transaction[currentidx],0,'Null')
            root_node.children_label.append(transaction[currentidx])
            root_node.children.append(child_node)
        #The below lines of code serves for cases where the transaction item is not 
        # a child of the root_node, meaning that it is a new path 
        # Hence we create a new node and add it to the root_node
        if transaction[currentidx] not in root_node.children_label:
            child_node = Node(transaction[currentidx],0,root_node.name,root_node)
            root_node.children_label.append(transaction[currentidx])
            root_node.children.append(child_node)
            idx = root_node.children_label.index(transaction[currentidx])
            root_node.children[idx].increment()
            traverse_one_transaction(transaction,root_node.children[idx],currentidx + 1)
            #create a child node, add the child label to root_node's children_label and add the node as a tuple (label, node) to root_node.children
        else:
            #find index of child in root_node.children_label
            #use the index to find and update the child in the root_node.children
            idx = root_node.children_label.index(transaction[currentidx])
            root_node.children[idx].increment()
            #Now we can recursively move along the path of the transaction
            traverse_one_transaction(transaction,root_node.children[idx],currentidx + 1)
    else:
        if(len(transaction) >= 1) and (len(root_node.children) == 0):
            root_node.leaf = True

def create_fp_tree(transaction_dict):
    root_node = Node('Null',1,None)
    for trans in transaction_dict:
        traverse_one_transaction(transaction = transaction_dict[trans],root_node = root_node, currentidx = 0,start = True)
    return root_node

def traverse_fp_tree(item,tree,cond_tree):
    #if (tree.leaf is False) and (tree.name != item):
    for child in tree.children:
        #temp_list.append(child)
        if child.name == item:
            cond_tree.children_label.append(child.name)
            cond_tree.children.append(child)
            create_conditional_tree(cond_tree.child,child,Start = True)
        else:
            traverse_fp_tree(item,tree = child,cond_tree = cond_tree)

def create_conditional_tree(cond_tree,child,Start = False):
    if child.parent_name != 'Null':
        cond_tree.parent = child.parent
        if Start is True:
            cond_tree.parent.count = 1
        else:
            cond_tree.parent.count += 1
        create_conditional_tree(cond_tree.child,child.parent)
        

test_dict,count = get_item_frequency(test)

test_dict,final_count,final_counts_idx_order = remove_items_below_sup(test_dict,count,3)

fp_tree = create_fp_tree(test_dict)

conditional_tree = Node('Null',1,None)
traverse_fp_tree('E',fp_tree,conditional_tree)
