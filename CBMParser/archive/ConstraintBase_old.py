from Rules import *

#Description:
#The ConstraintBase class generates the constraints from the variables defined in Rules.py

class ConstraintBase:
    def __init__(self):
        self.constraintBase=[]
    #find_all_paths - generates all grammars from all POS combinations as possible recursion and backtracking.
    #This code is based on the source here: https://www.python.org/doc/essays/graphs/
    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path and NodeEnabled[node]==1:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
    #regexGen - Maps the generated grammar (from find_all_paths) from their symbols, to 
    #the actual Word object containing the POS and its information.
    def regexGen(self, paths):
        #Check against NodeEnabled dictionary which path combinations to allow or disallow.
        #idxToDelete = []
        #prunedPaths=[]
        #---This entire code portion has been superceded by using an if condition in find_all_paths
        #for idx, path in enumerate(paths):
        #    for i in path:
        #        if i in NodeEnabled and NodeEnabled[i]==0:
        #            if idx not in idxToDelete:
        #                idxToDelete.append(idx)
        #for idx, path in enumerate(paths):
        #    if idx not in idxToDelete:
        #        prunedPaths.append(paths[idx])
        #Map to Word objects using mappings dictionary.
        for path in paths:
            regex=''
            for i in path:
                if i in mapping:
                    regex+=mapping[i].word
            self.constraintBase.append(regex)
    @property
    def constraint(self):
        return self.constraintBase