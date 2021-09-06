from re import A
import cifa
import param
import semantic
from prettytable import PrettyTable

op = ['=','>','<','==','>=','<=','<>','+','-','*','/','&','|','&&','||']

tot = 0

tnum = 0

iddict = {}  #符号表

numdict = {}                     #num表 对应存入寄存器

def is_number(s):#判断是不是数字
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

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

def middle_analyze(abstract_tree,middle_code,father):
    global tot
    global tnum
    op1 = ""
    arg1 = ""
    arg2 = ""
    op1 = father
    iselse = False
    elsenum = 0
    elsetemp = ''
    start = ''
    for key in abstract_tree.keys():
        if key == 'S':
            middle_analyze(abstract_tree['S'],middle_code,'S')
        elif key == 'if-then-else':
            middle_analyze(abstract_tree['if-then-else'],middle_code,'if-then-else')
        elif key == 'if':
            temp,elsetemp = middle_analyze(abstract_tree['if'],middle_code,'if')
            if arg1 == '':
                arg1 = temp
            elif arg2 == '':
                arg2 = temp
        elif key == 'then':
            temp = middle_analyze(abstract_tree['then'],middle_code,'then')
            if arg1 == '':
                arg1 = temp
            elif arg2 == '':
                arg2 = temp
        elif key == 'else':
            tot+=1
            middle_code[tot] = {'op':'==','arg1':elsetemp,'arg2':1}
            iselse = True
            elsenum = middle_analyze(abstract_tree['else'],middle_code,'else')
        elif key == 'while':
            middle_analyze(abstract_tree['while'],middle_code,'while')
        elif key == 'condition':
            start = tot + 1
            temp = middle_analyze(abstract_tree['condition'],middle_code,'condition')
            if arg1 == '':
                arg1 = temp
            elif arg2 == '':
                arg2 = temp
        elif key == 'do':
            temp = middle_analyze(abstract_tree['do'],middle_code,'do')
            if arg1 == '':
                arg1 = temp
            elif arg2 == '':
                arg2 = temp
        elif key in op:
            temp = middle_analyze(abstract_tree[key],middle_code,key)
            if arg1 == '':
                arg1 = temp
            elif arg2 == '':
                arg2 = temp
        elif is_number(key):
            if arg1 == '':
                arg1 = key
            elif arg2 == '':
                arg2 = key
        else:
            if arg1 == '':
                arg1 = key
            elif arg2 == '':
                arg2 = key
            pass
    if father in op:
        tot+=1
        result = ''
        if father == '=' or father == '!':
            result = arg1
            middle_code[tot]= {'op':op1,'arg1':arg2,'arg2':'','result':result}
        else:
            result = 't'+str(tnum)
            tnum+=1
            middle_code[tot]= {'op':op1,'arg1':arg1,'arg2':arg2,'result':result}
        return result
    if father == 'if':
        tot += 1
        #result = 't' + str(tot)
        middle_code[tot] = {'op':'beq','arg1':arg1,'arg2':0}
        return tot,arg1
    if father == 'then':
        return tot
    if father == 'else':
        return tot
    if father == 'if-then-else':
        middle_code[arg1]['result'] = arg2+1
        if iselse == True:
            middle_code[arg2+1]['result'] = elsenum + 1
    if father == 'condition':
        tot += 1
        middle_code[tot] = {'op':'beq','arg1':arg1,'arg2':0}
        return tot
    if father == 'do':
        tot+=1
        middle_code[tot] = {'op':'beq','arg1':'zero','arg2':'zero'}
        return tot
    if father == 'while':
        middle_code[arg1]['result'] = arg2+1
        middle_code[arg2]['result'] = start
    else:
        return ''

def show_form(middle_code):
    middle_code_form = PrettyTable()
    middle_code_form.field_names = ['index','op','arg1','arg2','result']
    for key in middle_code:
        index = key
        op1 = middle_code[key]['op']
        arg1 = middle_code[key]['arg1']
        arg2 = middle_code[key]['arg2']
        result = middle_code[key]['result']
        middle_code_form.add_row([index,op1,arg1,arg2,result])
    print(middle_code_form)

def generate_code(op1,arg1,arg2,result):
    global iddict
    global numdict
    tresult = result
    codelist=[]
    code = ''
    if is_number(arg1) == False:
        if arg1 in [i for i in iddict]:
            arg1 = 's' + str(iddict[arg1])
        arg1 = '$'+arg1
    if is_number(arg2) == False:
        if arg2 in [i for i in iddict]:
            arg2 = 's' + str(iddict[arg2])
        arg2 = '$'+arg2
    if is_number(result) == False:
        if result in [i for i in iddict]:
            result = 's' + str(iddict[result])
        result = '$'+result

    if arg1 == 0 or arg1 == '0':
        arg1 = '$zero'
    if arg2 == 0 or arg2 == '0':
        arg2 = '$zero'
    if result == 0 or result == '0':
        result = '$zero'

    if arg1 == 1 or arg1 == '1':
        arg1 = '$k1'
    if arg2 == 1 or arg2 == '1':
        arg2 = '$k1'
    if result == 1 or result == '1':
        result = '$k1'

    if arg1 in [key for key in numdict]:
        arg1 = numdict[arg1]
    if arg2 in [key for key in numdict]:
        arg2 = numdict[arg2]
    if result in [key for key in numdict]:
        result = numdict[result]

    
    if op1 == '+':
        code = '{} {},{},{}'.format('add',result,arg1,arg2)
        codelist.append(code)
    if op1 == '-':
        code = '{} {},{},{}'.format('sub', result, arg1, arg2)
        codelist.append(code)
    if op1 == '*':
        code = '{} {},{},{}'.format('mult', result, arg1, arg2)
        codelist.append(code)
    if op1 == '/':
        code = '{} {},{},{}'.format('div', result, arg1, arg2)
        codelist.append(code)
    if op1 == '==':
        code = '{} {},{},{}'.format('slt', '$a0', arg1, arg2)
        codelist.append(code)
        code = '{} {},{},{}'.format('slt', '$a1', arg2, arg1)
        codelist.append(code)
        code = '{} {},{},{}'.format('nor', result, '$a0', '$a1')
        codelist.append(code)
    if op1 == '<>':
        code = '{} {},{},{}'.format('slt', '$a0', arg1, arg2)
        codelist.append(code)
        code = '{} {},{},{}'.format('slt', '$a1', arg2, arg1)
        codelist.append(code)
        code = '{} {},{},{}'.format('xor', result, '$a0', '$a1')
        codelist.append(code)
    if op1 == '<':
        code = '{} {},{},{}'.format('slt', result, arg1, arg2)
        codelist.append(code)
    if op1 == '>=':
        code = '{} {},{},{}'.format('slt', '$a0', arg1, arg2)
        codelist.append(code)
        code = '{} {},{},{}'.format('xor', result, '$a0', '$k1')
        codelist.append(code)
    if op1 == '>':
        code = '{} {},{},{}'.format('slt', result, arg2, arg1)
        codelist.append(code)
    if op1 == '<=':
        code = '{} {},{},{}'.format('slt', '$a0', arg2, arg1)
        codelist.append(code)
        code = '{} {},{},{}'.format('xor', result, '$a0', '$k1')
        codelist.append(code)
    if op1 == '&' or op1 == '&&':
        code = '{} {},{},{}'.format('and', result, arg2, arg1)
        codelist.append(code)
    if op1 == '|' or op1 == '||':
        code = '{} {},{},{}'.format('or', result, arg2, arg1)
        codelist.append(code)
    if op1 == '=':
        code = '{} {},{},{}'.format('add', result, arg1, '$zero')
        codelist.append(code)
    if op1 == '!':
        code = '{} {},{},{}'.format('nor', result, arg1, '$zero')
        codelist.append(code)
    if op1 == 'beq':
        code = '{} {},{},{}'.format('beq', arg1, arg2,'loop{}'.format(tresult))
        codelist.append(code)
    return codelist

def object_analyze(middle_code):
    global tot
    object_code = []
    for key in middle_code:
        index = key
        op1 = middle_code[key]['op']
        arg1 = middle_code[key]['arg1']
        arg2 = middle_code[key]['arg2']
        result = middle_code[key]['result']
        object_code.append('loop{}:'.format(index))
        codelist = generate_code(op1,arg1,arg2,result)
        for code in codelist:
            object_code.append(code)
    object_code.append('loop{}:'.format(tot+1))
    return object_code

if __name__ == '__main__':
    abstract_tree,iddict,wordlist = semantic.main()
    cnt = 0
    for word in wordlist:
        if word[3] == 'num':
            numdict[word[1]]='$a'+str(cnt)
            cnt+=1
    print(abstract_tree)
    print(iddict)
    print('------------------中间代码生成--------------')
    middle_code = {}
    middle_analyze(abstract_tree['S'],middle_code,'S')
    show_form(middle_code)
    print('------------------目标代码生成--------------')
    object_code = object_analyze(middle_code)
    for key in numdict:
        print('li {},{}'.format(numdict[key],key))
    for i in object_code:
        print(i)
    print('syscall')
    with open('mips.txt','w') as f:
        f.write('li $k1,1')
        f.write('\n')
        for key in numdict:
            f.write('li {},{}'.format(numdict[key],key))
            f.write('\n')
        for i in object_code:
            f.write(i)
            f.write('\n')
        f.write('syscall')
    print('成功在mips.txt中生成目标代码')