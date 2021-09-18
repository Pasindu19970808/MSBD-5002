#This code builds a hash trww to be used for Frequent Pattern Mining, by hashing all the frequent itemself candidates into hash buckets. Currently this code is made to work with a has function of x%3

import re
import copy
#candidates = '{1 2 3 }, {1 4 5}, {1 2 4}, {1 2 5}, {1 5 9}, {1 3 6},{2 3 4}, {2 5 9},{3 4 5}, {3 5 6}, {3 5 9}, {3 8 9}, {3 2 6},{4 5 7}, {4 1 8}, {4 7 8}, {4 6 7},{6 1 3}, {6 3 4}, {6 8 9}, {6 2 1}, {6 4 3}, {6 7 9},{8 2 4}, {8 9 1}, {8 3 6}, {8 3 7}, {8 4 7}, {8 5 1}, {8 3 1}, {8 6 2}'

candidates = '{1 4 5}, {1 2 4}, {4 5 7}, {1 2 5}, {4 5 8}, {1 5 9}, {1 3 6}, {2 3 4}, {5 6 7},{3 4 5}, {3 5 6}, {3 5 7}, {6 8 9}, {3 6 7}, {3 6 8}'
res = [int(i) for i in re.findall(r'[^{},]',candidates) if i != ' ']
interval = int(len(res)/3)
res_final = [res[3*int(i):3*int(i+1)] for i in range(0,interval)]

class root:
    def __init__(self):
        self.remainderone = None
        self.remaindertwo = None
        self.remainderzero = None
        
class remainderZeroNode:
    def __init__(self):
        self.content = None
        self.remainderone = None
        self.remaindertwo = None
        self.remainderzero = None
        self.complete = False

class remainderOneNode:
    def __init__(self):
        self.content = None
        self.remainderone = None
        self.remaindertwo = None
        self.remainderzero = None
        self.complete = False

class remainderTwoNode:
    def __init__(self):
        self.content = None
        self.remainderone = None
        self.remaindertwo = None
        self.remainderzero = None
        self.complete = False


def create_hashtree(candidateset,node = None, sort = False, max_leafsize = 3,depth = 0):
    if sort == True:
        candidateset = [sorted(i) for i in candidateset]
    if depth == 0:
        node.remainderone = remainderOneNode()
        node.remaindertwo  = remainderTwoNode()
        node.remainderzero  = remainderZeroNode()
        node.remainderone.content = [i for i in candidateset if i[0]%3 == 1]
        node.remaindertwo.content = [i for i in candidateset if i[0]%3 == 2]
        node.remainderzero.content = [i for i in candidateset if i[0]%3 == 0]
    else:
        node.remainderone = remainderOneNode()
        node.remaindertwo  = remainderTwoNode()
        node.remainderzero  = remainderZeroNode()
        node.remainderone.content = [i for i in candidateset if i[depth]%3 == 1]
        node.remaindertwo.content = [i for i in candidateset if i[depth]%3 == 2]
        node.remainderzero.content = [i for i in candidateset if i[depth]%3 == 0]

    if (len(node.remainderone.content) > max_leafsize) & (depth < 2):
        create_hashtree(candidateset = node.remainderone.content, node = node.remainderone, depth = depth + 1)
    else:
        node.remainderone.complete = True
    if (len(node.remaindertwo.content) > max_leafsize) & (depth < 2):
        create_hashtree(candidateset = node.remaindertwo.content, node = node.remaindertwo, depth = depth + 1)
    else:
        node.remaindertwo.complete = True
    if (len(node.remainderzero.content) > max_leafsize) & (depth < 2):
        create_hashtree(candidateset = node.remainderzero.content, node = node.remainderzero, depth = depth + 1)
    else:
        node.remainderzero.complete = True


def output_hashtree(result,node = None):
    if len(result) == 0:
        for attr in node.__dict__:
            result.append(getattr(node,attr))
        output_hashtree(result,node)
    else:
        for i in range(len(result)):
            if result[i].complete == True:
                result[i] = result[i].content
            else:
                obj = copy.deepcopy(result[i])
                result[i] = list()
                for attr in list(obj.__dict__.keys())[1:-1]:
                    result[i].append(getattr(obj,attr))
                output_hashtree(result=result[i])

rootnode = root()
create_hashtree(res_final,node = rootnode, sort = False, max_leafsize = 3,depth = 0)
final_result = list()
output_hashtree(final_result,node=rootnode)
print(final_result)

