import cifa
import param
import os

iddict2 = {}
iddict = {}

#通过value找key
def get_key(dict,value):
    return [k for k,v in dict.items() if v == value][0]

#打印树
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

#报错函数
def error(num,id):
    print('error:')
    if num == 0:
        print('变量{}不能重复定义'.format(get_key(iddict,id)))
    if num == 1:
        print('变量{}未定义就使用'.format(get_key(iddict,id)))
    if num == 2:
        print('{} 不同类型变量不能赋值'.format(get_key(iddict,id)))
    exit()

#拼接语法
def get_rule(analyze_tree):
    rule = ''
    for key in analyze_tree.keys():
        rule += key
    return rule

# S(),X()等函数是对应非终结符的处理函数

def P(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('H->',rule)
    if rule == '(J)':
        abstract_tree['('] = '('
        J(analyze_tree['J'],abstract_tree)
        print('debug')
        print(analyze_tree['A'])
        print(abstract_tree)
        abstract_tree[')'] = ')'
        
    if rule == 'num':
        num = analyze_tree['num']
        abstract_tree[num] = num
    if rule == 'id':
        id = analyze_tree['id']
        if id not in iddict2:
            error(1,id)
        abstract_tree[get_key(iddict,id)] = get_key(iddict,id)


def O(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('O->',rule)
    if rule == '!P':
        abstract_tree['!'] = {}
        P(analyze_tree['P'],abstract_tree['!'])
    if rule == 'P':
        P(analyze_tree['P'],abstract_tree)

def NN(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('NN->',rule)
    if rule == '>ONN' or rule == '>=ONN' or rule == '<ONN' or rule == '<=ONN': 
        type = [k for k in analyze_tree['NN'].keys()][0]
        if type == '@':
            O(analyze_tree['O'],abstract_tree)
        else:
            abstract_tree[type] = {}
            O(analyze_tree['O'],abstract_tree[type])
            NN(analyze_tree['NN'],abstract_tree[type])
    if rule == '@':
        pass
        
def N(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('N->',rule)
    if rule == 'ONN':
        type = [k for k in analyze_tree['NN'].keys()][0]
        if type == '@':
            O(analyze_tree['O'],abstract_tree)
        else:
            abstract_tree[type] = {}
            O(analyze_tree['O'],abstract_tree[type])
            NN(analyze_tree['NN'],abstract_tree[type])

def MM(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('MM->',rule)
    if rule == '=NMM'or rule == '==NMM'or rule == '<>NMM': 
        type = [k for k in analyze_tree['MM'].keys()][0]
        if type == '@':
            N(analyze_tree['N'],abstract_tree)
        else:
            abstract_tree[type] = {}
            N(analyze_tree['N'],abstract_tree[type])
            MM(analyze_tree['MM'],abstract_tree[type])
    if rule == '@':
        pass
        
def M(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('M->',rule)
    if rule == 'NMM':
        type = [k for k in analyze_tree['MM'].keys()][0]
        if type == '@':
            N(analyze_tree['N'],abstract_tree)
        else:
            abstract_tree[type] = {}
            N(analyze_tree['N'],abstract_tree[type])
            MM(analyze_tree['MM'],abstract_tree[type])

def LL(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('LL->',rule)
    if rule == '&&MLL':
        type = [k for k in analyze_tree['LL'].keys()][0]
        if type == '@':
            M(analyze_tree['M'],abstract_tree)
        else:
            abstract_tree[type] = {}
            M(analyze_tree['M'],abstract_tree[type])
            LL(analyze_tree['LL'],abstract_tree[type])
    if rule == '@':
        pass
        
def L(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('L->',rule)
    if rule == 'MLL':
        type = [k for k in analyze_tree['LL'].keys()][0]
        if type == '@':
            M(analyze_tree['M'],abstract_tree)
        else:
            abstract_tree[type] = {}
            M(analyze_tree['M'],abstract_tree[type])
            LL(analyze_tree['LL'],abstract_tree[type])

def JJ(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('JJ->',rule)
    if rule == '||LJJ':
        type = [k for k in analyze_tree['JJ'].keys()][0]
        if type == '@':
            L(analyze_tree['L'],abstract_tree)
        else:
            abstract_tree[type] = {}
            L(analyze_tree['L'],abstract_tree[type])
            JJ(analyze_tree['JJ'],abstract_tree[type])
    if rule == '@':
        pass
        
def J(analyze_tree,abstract_tree): #条件判断语句
    rule = get_rule(analyze_tree)
    print('J->',rule)
    if rule == 'LJJ':
        type = [k for k in analyze_tree['JJ'].keys()][0]
        if type == '@':
            L(analyze_tree['L'],abstract_tree)
        else:
            abstract_tree[type] = {}
            L(analyze_tree['L'],abstract_tree[type])
            JJ(analyze_tree['JJ'],abstract_tree[type])


def K(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('K->',rule)
    if rule == 'else{S};':
        abstract_tree['else'] = {}
        S(analyze_tree['S'],abstract_tree['else'])
    if rule == '@':
        pass

def D(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('D->',rule)
    if rule == 'if(J){S};K':
        abstract_tree['if-then-else'] = {}
        abstract_tree['if-then-else']['if'] = {}
        abstract_tree['if-then-else']['then'] = {}
        J(analyze_tree['J'],abstract_tree['if-then-else']['if'])
        S(analyze_tree['S'],abstract_tree['if-then-else']['then'])
        K(analyze_tree['K'],abstract_tree['if-then-else'])
    if rule == 'while(J){S};':
        abstract_tree['while'] = {}
        abstract_tree['while']['condition'] = {}
        abstract_tree['while']['do'] = {}
        J(analyze_tree['J'],abstract_tree['while']['condition'])
        S(analyze_tree['S'],abstract_tree['while']['do'])

def H(analyze_tree,abstract_tree,kind):
    rule = get_rule(analyze_tree)
    print('H->',rule)
    if rule == '(A)':
        abstract_tree['('] = '('
        A(analyze_tree['A'],abstract_tree,kind)
        print('debug')
        print(analyze_tree['A'])
        print(abstract_tree)
        abstract_tree[')'] = ')'
        
    if rule == 'num':
        num = analyze_tree['num']
        abstract_tree[num] = num
    if rule == 'id':
        id = analyze_tree['id']
        if id not in iddict2:
            error(1,id)
        if iddict2[id] != kind:
            error(2,id)
        abstract_tree[get_key(iddict,id)] = get_key(iddict,id)

def GG(analyze_tree,abstract_tree,kind):
    rule = get_rule(analyze_tree)
    print('GG->',rule)
    if rule == '*HGG' or rule == '/HGG':
        type = [k for k in analyze_tree['GG'].keys()][0]
        if type == '@':
            H(analyze_tree['H'],abstract_tree,kind)
        else:
            abstract_tree[type] = {}
            H(analyze_tree['H'],abstract_tree[type],kind)
            GG(analyze_tree['GG'],abstract_tree[type],kind)
    if rule == '@':
        pass
        
def G(analyze_tree,abstract_tree,kind):
    rule = get_rule(analyze_tree)
    print('G->',rule)
    if rule == 'HGG':
        type = [k for k in analyze_tree['GG'].keys()][0]
        if type == '@':
            H(analyze_tree['H'],abstract_tree,kind)
        else:
            abstract_tree[type] = {}
            H(analyze_tree['H'],abstract_tree[type],kind)
            GG(analyze_tree['GG'],abstract_tree[type],kind)

def FF(analyze_tree,abstract_tree,kind):
    rule = get_rule(analyze_tree)
    print('FF->',rule)
    if rule == '+GFF' or rule == '-GFF':
        type = [k for k in analyze_tree['FF'].keys()][0]
        if type == '@':
            G(analyze_tree['G'],abstract_tree,kind)
        else:
            abstract_tree[type] = {}
            G(analyze_tree['G'],abstract_tree[type],kind)
            FF(analyze_tree['FF'],abstract_tree[type],kind)
    if rule == '@':
        pass
        
def F(analyze_tree,abstract_tree,kind):
    rule = get_rule(analyze_tree)
    print('F->',rule)
    if rule == 'GFF':
        type = [k for k in analyze_tree['FF'].keys()][0]
        if type == '@':
            G(analyze_tree['G'],abstract_tree,kind)
        else:
            abstract_tree[type] = {}
            G(analyze_tree['G'],abstract_tree[type],kind)
            FF(analyze_tree['FF'],abstract_tree[type],kind)

def EE(analyze_tree,abstract_tree,kind):
    rule = get_rule(analyze_tree)
    print('EE->',rule)
    if rule == '&FEE':
        type = [k for k in analyze_tree['EE'].keys()][0]
        if type == '@':
            F(analyze_tree['F'],abstract_tree,kind)
        else:
            abstract_tree[type] = {}
            F(analyze_tree['F'],abstract_tree[type],kind)
            EE(analyze_tree['EE'],abstract_tree[type],kind)
    if rule == '@':
        pass
        
def E(analyze_tree,abstract_tree,kind):
    rule = get_rule(analyze_tree)
    print('E->',rule)
    if rule == 'FEE':
        type = [k for k in analyze_tree['EE'].keys()][0]
        if type == '@':
            F(analyze_tree['F'],abstract_tree,kind)
        else:
            abstract_tree[type] = {}
            F(analyze_tree['F'],abstract_tree[type],kind)
            EE(analyze_tree['EE'],abstract_tree[type],kind)


def AA(analyze_tree,abstract_tree,kind):
    rule = get_rule(analyze_tree)
    print('AA->',rule)
    if rule == '|EAA':
        type = [k for k in analyze_tree['AA'].keys()][0]
        if type == '@':
            E(analyze_tree['E'],abstract_tree,kind)
        else:
            abstract_tree[type] = {}
            E(analyze_tree['E'],abstract_tree[type],kind)
            AA(analyze_tree['AA'],abstract_tree[type],kind)
    if rule == '@':
        pass
        
def A(analyze_tree,abstract_tree,kind):
    rule = get_rule(analyze_tree)
    print('A->',rule)
    if rule == 'EAA':
        type = [k for k in analyze_tree['AA'].keys()][0]
        if type == '@':
            E(analyze_tree['E'],abstract_tree,kind)
        else:
            abstract_tree[type] = {}
            E(analyze_tree['E'],abstract_tree[type],kind)
            AA(analyze_tree['AA'],abstract_tree[type],kind)

def XX(analyze_tree,abstract_tree,type):
    rule = get_rule(analyze_tree)
    print('XX->',rule)
    if rule == ',X':
        X(analyze_tree['X'],abstract_tree,type)
    if rule == '@':
        pass

def X(analyze_tree,abstract_tree,type): #传入type
    rule = get_rule(analyze_tree)
    print('X->',rule)
    if rule == 'idXX':
        if type in ['int','bool']:
            id = analyze_tree['id']
            print('debug:','id:{} is {}'.format(id, type))
            if id in iddict2:
                error(0,id)
            else:
                iddict2[id] = type
            abstract_tree[get_key(iddict,id)] = get_key(iddict,id)
            XX(analyze_tree['XX'],abstract_tree,type)
        elif type in ['get','put']:
            id = analyze_tree['id']
            if id not in iddict2:
                error(1,id)
            print('debug:','{} id:{}'.format(type,id))
            abstract_tree[get_key(iddict,id)] = get_key(iddict,id)
            XX(analyze_tree['XX'],abstract_tree,type)



def C(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('C->',rule)
    if rule == 'intX;':
        abstract_tree['int'] = {}
        X(analyze_tree['X'],abstract_tree['int'],'int')
    if rule == 'boolX;':
        abstract_tree['bool'] = {}
        X(analyze_tree['X'],abstract_tree['bool'],'bool')
    if rule == 'get(X);':
        abstract_tree['get'] = {}
        X(analyze_tree['X'],abstract_tree['get'],'get')
        pass
    if rule == 'put(X);':
        abstract_tree['put'] = {}
        X(analyze_tree['X'],abstract_tree['put'],'put')
        pass

def B(analyze_tree,abstract_tree):
    rule = get_rule(analyze_tree)
    print('B->',rule)
    if rule == 'S':
        abstract_tree['S'] = {}
        S(analyze_tree['S'],abstract_tree['S'])
    if rule == '@':
        pass


def S(analyze_tree,abstract_tree): #传入对应分析树和抽象语法树
    rule = get_rule(analyze_tree)
    print('S->',rule)
    if rule == 'CB':
        C(analyze_tree['C'],abstract_tree)
        B(analyze_tree['B'],abstract_tree)
    if rule == 'id=A;B':
        id = analyze_tree['id']
        if id not in iddict2:
            error(1,id)
        abstract_tree['='] = {}
        abstract_tree['='][get_key(iddict,id)] = get_key(iddict,id)
        A(analyze_tree['A'],abstract_tree['='],iddict2[id])
        B(analyze_tree['B'],abstract_tree)
    if rule == 'DB':
        D(analyze_tree['D'],abstract_tree)
        B(analyze_tree['B'],abstract_tree)


def analyze(iddict,wordlist,analyze_tree):
    abstract_tree = {'S':{}}
    S(analyze_tree['S'],abstract_tree['S'])
    print()
    print(iddict2)
    print()
    display(abstract_tree)
    print('分析成功，没有语义错误')
    return abstract_tree

def main():
    global iddict,iddict2
    iddict,wordlist = cifa.main()         #进行词法分析 返回符号表,分析结果
    analyze_tree = param.main(iddict,wordlist)       #返回语法分析树
    #os.system("clear")
    abstract_tree = analyze(iddict,wordlist,analyze_tree)
    return abstract_tree,iddict,wordlist

if __name__ == '__main__':
    main()
