import cifa

Alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','BB',
         'CC','DD','EE','FF','GG','HH','II','JJ','KK','LL','MM','NN','OO','PP','QQ','RR','SS','TT','UU','VV','WW','XX','YY','ZZ']

class Rule:
    def __init__(self,left,right):
        self.left = left
        self.right = right
    def show(self):
        print("{0} -> ".format(self.left),end='')
        for nonterminal in self.right:
            print(nonterminal,end='')
        print('')

rules = []
set_terminal = set()
set_nonterminal = set()
def read_rules():       #读入文法
    filename = 'wenfa.txt'
    with open(filename, 'r') as f: 
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')                 #去掉\n
            line_in_split = line.split(' ')         #拆分
            set_nonterminal.add(line_in_split[0])      #保存所有非终结符
            for terminal in line_in_split[2:]:   #保存所有终结符
                if terminal not in Alpha:
                    set_terminal.add(terminal)
            rules.append(Rule(line_in_split[0],line_in_split[2:]))

def show_rules():       #打印文法
    for rule in rules:
        rule.show()

    print()
    print('非终结符：')
    for nonterminal in set_nonterminal:
        print(nonterminal,end=' ')


    print()
    print('终结符：')
    for terminal in set_terminal:
        print(terminal,end=' ')
    print()


dict_first = {} # 用字典保存first集

def calculate_first():      #因为文法中不出现A1A2A3 而A1->@ 的情况，不考虑
    for i in set_nonterminal:
        dict_first[i] = set()
    while True:
        cc = 0
        for rule in rules:
            if rule.right[0] not in Alpha:
                len_before = len(dict_first[rule.left])
                dict_first[rule.left].add(rule.right[0])           #非终结符加入到first集中
                if len_before != len(dict_first[rule.left]):        #判断是否有增加新元素
                    cc = 1
                    #print("debug")
            else:
                len_before = len(dict_first[rule.left])
                dict_first[rule.left] = dict_first[rule.left].union(dict_first[rule.right[0]])       #终结符的first集合并
                if len_before != len(dict_first[rule.left]):        #判断是否有增加新元素
                    cc = 1
        if cc == 0:         #退出机制
            break

def show_first():
    print()
    print('first集:')
    for i in sorted(dict_first): 
        print ("{0}:{1}".format(i,dict_first[i])) 

dict_follow = {}
def calculate_follow():
    for i in set_nonterminal:
        dict_follow[i] = set()
    dict_follow['S'].add('$')
    while True:
        cc = 0
        for rule in rules:
            right = rule.right
            left = rule.left
            for i in range(len(right)):
                if i+1 == len(right) and right[i] in Alpha:
                    len_before = len(dict_follow[right[i]])
                    dict_follow[right[i]] = dict_follow[right[i]].union(dict_follow[left])
                    if len_before != len(dict_follow[right[i]]):
                        cc = 1
                    if right[i-1] in Alpha and '@' in dict_first[right[i]]:         #如果最后的非终结符可以为空（只考虑一次）
                        len_before = len(dict_follow[right[i-1]])
                        dict_follow[right[i-1]] = dict_follow[right[i-1]].union(dict_follow[left])
                        if len_before != len(dict_follow[right[i-1]]):
                            cc = 1
                elif i+1 < len(right):
                    if right[i] in Alpha and right[i+1] not in Alpha:
                        len_before = len(dict_follow[right[i]])
                        dict_follow[right[i]].add(right[i+1])
                        if len_before != len(dict_follow[right[i]]):
                            cc = 1
                    elif right[i] in Alpha and right[i+1] in Alpha:
                        len_before = len(dict_follow[right[i]])
                        dict_follow[right[i]] = dict_follow[right[i+1]].union(dict_first[right[i+1]])
                        if '@' in dict_follow[right[i]]:
                            dict_follow[right[i]].remove('@')
                        if len_before != len(dict_follow[right[i]]):
                            cc = 1
        if cc == 0:
            break

def show_follow():
    print()
    print('follow集:')
    for i in sorted(dict_follow): 
        print ("{0}:{1}".format(i,dict_follow[i])) 

list_select = []

def calculate_select():         #计算select集
    for rule in rules:
        left = rule.left
        right = rule.right[0]
        if right == '@':        
            list_select.append(list(dict_follow[left]))     #如果是空select为左边的follow
        elif right in Alpha:        
            list_select.append(list(dict_first[right]))     #如果是非终结符则为其first
        else:
            t = []
            t.append(right)
            list_select.append(t)       #如果是终结符就是终结符

def show_select():
    print()
    print('select集:')
    count = 0
    for i in list_select:
        count += 1
        print('{0}:{1}'.format(count,i))

dicts = {}
def calculate_dicts():
    count = 0
    for rule in rules:
        left = rule.left
        right = rule.right
        select = list_select[count]
        count += 1
        for i in select:
            dicts[(left,i)] = right
			
from prettytable import PrettyTable
table = PrettyTable(["步骤", "分析栈", "当前输入a","剩余输入串", "所用产生式"])

def show_dicts():
    print()
    print("预测分析表:")
    print(dicts)



read_rules()
show_rules()
calculate_first()
show_first()
calculate_follow()
show_follow()
calculate_select()
show_select()
calculate_dicts()
show_dicts()

# 构造非终结符集合
Vh = list(set_nonterminal)
# 构造终结符集合
Vt = list(set_terminal)

# 获取输入栈中的内容
def printstack(stack):
    rtu = ''
    for i in stack:
        rtu += i + ' '
    return rtu

# 得到输入串剩余串
def printstr(str, index):
    rtu = ''
    for i in range(index, len(str), 1):
        rtu += str[i] + ' '
    return rtu

def error(msg = ''):
    table.align['步骤'] = 'l'
    table.align['分析栈'] = 'l'
    table.align['剩余输入串'] = 'l'
    table.align['所用产生式'] = 'l'
    table.align['当前输入a'] = 'l'
    print(table)
    print('Error',msg)
    exit()


analyze_tree = {'S':{}}

def find_tree(tree,x):
    for i in tree.keys():
        if i in Vh:
            temp = find_tree(tree[i],x)
            if temp == {}:
                return temp

    for i in tree.keys():
        if i == x and tree[i] == {}:
            return tree[i]

def display(tree,level=0): #输出树
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
    

# 语法分析程序
def analyze(str,idlist,numlist):
    # 用列表模拟栈
    stack = []
    location = 0
    # 将#号入栈
    stack.append(str[location])

    # 将文法开始符入栈
    stack.append('S')
    # 将输入串第一个字符读进a中
    location += 1
    a = str[location]

    flag = True
    count = 1       #计算步骤
    table.add_row([count, printstack(stack),a, printstr(str, location),''])
    while flag:
        if count == 1:
            pass
        else:
            if x in Vt:
                table.add_row([count, printstack(stack),a, printstr(str, location),''])
            else:
                ss = ''
                for i in s:
                    ss += i
                temp = x + '->' + ss
                table.add_row([count, printstack(stack),a, printstr(str, location),temp])
        x = stack.pop()
        if x in Vt:          #栈顶是终结符
            if x == str[location]:   #该字符匹配，输入串向后挪一位
                location += 1
                a = str[location]
            else:            #否则错误
                if(x==')'):
                    error('丢失右括号')
                if(a==')'):
                    error('丢失左括号')
                if(a=='num'):
                    error('丢失运算符')
                error()
        elif x == '$':       #栈顶是结束符
            if x == a:       #当前输入字符也是结束符，分析结束
                flag = False
            else:            #否则错误
                error()
        elif (x, a) in dicts.keys():    #M[x,a]是产生式
            #print('debug:',count)
            s = dicts[(x, a)]
            tree = find_tree(analyze_tree,x)
            #print(tree)
            for i in s:
                if i in Vt:
                    if i == 'id':
                        tree[i] = idlist.pop(0)
                    elif i == 'num':
                        tree[i] = numlist.pop(0)
                    elif x == 'MM' and i == '=':
                        tree['=='] = '=='
                    else:
                        tree[i] = i
                elif i == '@':
                    tree[i] = '@'
                elif i in Vh:
                    #display(analyze_tree)
                    tree[i] = {}
                else:
                    error()

            for i in range(len(s) - 1, -1, -1):         #倒序入栈
                if s[i] != '@':
                    stack.append(s[i])
        else:
            if(a=='num'):
                error('丢失运算符')
            if(a=='id'):
                error('丢失运算符')
            if(a==')'):
                error('丢失操作数')
            error()
        count += 1

def main(iddict,wordlist):
    strlist = ['$']
    # filename = "param_in.txt"
    # with open(filename,'r') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         line = line.strip('\n')
    #         strlist.append(line)
    for word in wordlist:
        strlist.append(word[3])
    strlist.append('$')

    idlist = []                     #id顺序
    for word in wordlist:
        if word[3] == 'id':
            idlist.append(word[0])

    numlist = []                     #num顺序
    for word in wordlist:
        if word[3] == 'num':
            numlist.append(word[1])
    
    print()
    print("待分析记号流:")
    print(strlist)
    #strlist = ['$','id','+','id','$']
    analyze(strlist,idlist,numlist)
	#左对齐
    table.align['步骤'] = 'l'
    table.align['分析栈'] = 'l'
    table.align['剩余输入串'] = 'l'
    table.align['所用产生式'] = 'l'
    table.align['当前输入a'] = 'l'
    print(table)
    print("分析成功!")
    print('分析树字典')
    print(analyze_tree)
    print('打印分析树')
    display(analyze_tree)
    return analyze_tree

if __name__ == '__main__':
    iddict,wordlist = cifa.main()         #进行词法分析 返回符号表,分析结果
    main(iddict,wordlist)