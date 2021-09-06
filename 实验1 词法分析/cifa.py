
keywords = {"if":1,"else":2,"void":3,"return":4,"while":5,"then":6,"for":7,"bool":8,
            "int":9,"char":10,"double":11,"float":12,"case":13,"get":14,"put":15}

separater = {';':16,',':17,'{':18,'}':19,'[':20,']':21,'(':22,')':23}

operator = {'+':24,'-':25,'*':26,'/':27,'>':28,'<':29,'=':30,'!':31,'&&':32,'||':33,'==':34,'<>':35,'>=':36,'<=':37,'&':38,'|':39}

def isnum(s):
    c = 1
    if s[0] == '-':
        c = -1
    elif s[0] == '+':
        c = 1
    elif s[0] == '0':
        if s[1] == 'x' or s[1] == 'X':
            try:
                float(s[2:])
                return True
            except ValueError:
                pass
        else:
            try:
                float(s[1:])
                return True
            except ValueError:
                pass
    else:
        try:
            float(s)
            return True
        except ValueError:
            pass
    '''
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.digit(s)
        return True
    except (TypeError, ValueError):
        pass    

    '''



 
    return False

def isid(word):
    if word[0].isalpha() or word[0] == '_':
        if len(word) == 1:
            return True
        for i in word[1:]:
            if i.isalpha() or i.isdigit() or i == '_':
                return True
            else:
                return False
    else:
        return False
    #return word.isidentifier()



def main():
    tot = 0
    num_lines = 0
    num_keywords = 0
    num_separater = 0
    num_operator = 0
    num_id = 0
    num_num = 0
    num_error = 0
    lists = []
    iddict = {} 
    idindex = 0
    with open('test1.txt', 'r') as lines:
        j = 0
        for line in lines:
            num_lines+=1
            j+=1
            word = ""
            for i in range(0, len(line)):
                word += line[i]
                if line[i] != ' ':
                    tot += 1
                if line[i] == ' ' or line[i] in separater or line[i] in operator:
                    if word in operator:
                        lists.append([operator[word],word,'操作符'])
                        num_operator += 1
                    else:
                        
                        #判断之前读入的字符串
                        word = word[:-1]
                        #print('debug',word)
                        if len(word)>=1:
                            if word in keywords:
                                lists.append([keywords[word],word,'关键字'])
                                num_keywords += 1
                            elif word in separater:
                                lists.append([separater[word],word,'分隔符'])
                                num_separater += 1
                            elif word in operator:
                                lists.append([operator[word],word],'操作符')
                                num_operator += 1
                            elif isnum(word):
                                lists.append([word,word,'数字'])
                                num_num += 1
                            elif isid(word):
                                if word not in iddict:
                                    idindex+=1
                                    iddict[word]=idindex
                                lists.append(['符号表id={}'.format(iddict[word]),word,'标识符'])
                                num_id += 1
                            else:
                                print('Error in 第{}行第{}列'.format(j,i))
                                num_error += 1
                        #判断最近读入的字符
                        if line[i] in separater:
                            lists.append([separater[line[i]],line[i],'分隔符'])
                        elif line[i] in operator:
                            lists.append([operator[line[i]],line[i],'操作符'])
                    
                    word = ""
                else:
                    continue
    for word in lists:
        print("表达式：{1}  记号：{2}   属性：{0}".format(word[0],word[1],word[2]))
    print('\n统计结果:\n总共有{0}个字符\n共计{1}行\n关键字{2}个\n分隔符{3}个\n操作符{4}个\n数字{5}个\n标识符{6}个\n出错{7}处'.format(tot,num_lines,num_keywords,num_separater,num_operator,num_num,num_id,num_error))

main()