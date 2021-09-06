analyze_tree = {'S': {'id': 1, 'SS': {'(': '(', 'BB': {'X': {'id': 2, 'XX': {'@': '@'}}, ')': ')', ';': ';', 'B': {'@': '@'}}}}}

def display(tree,level=0):
    if level == 0:
        for key in tree.keys():
            print(key,':')
            display(tree[key],level+1)
    else:
        prefix =" " * level * 4
        for key in tree.keys():
            if isinstance(tree[key],dict):
                print(prefix,key,':')
                display(tree[key],level+1)
            else:
                print(prefix,key,':',tree[key])

display(analyze_tree)