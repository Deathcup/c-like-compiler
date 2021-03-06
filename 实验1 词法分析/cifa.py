
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
                        lists.append([operator[word],word,'?????????'])
                        num_operator += 1
                    else:
                        
                        #??????????????????????????????
                        word = word[:-1]
                        #print('debug',word)
                        if len(word)>=1:
                            if word in keywords:
                                lists.append([keywords[word],word,'?????????'])
                                num_keywords += 1
                            elif word in separater:
                                lists.append([separater[word],word,'?????????'])
                                num_separater += 1
                            elif word in operator:
                                lists.append([operator[word],word],'?????????')
                                num_operator += 1
                            elif isnum(word):
                                lists.append([word,word,'??????'])
                                num_num += 1
                            elif isid(word):
                                if word not in iddict:
                                    idindex+=1
                                    iddict[word]=idindex
                                lists.append(['?????????id={}'.format(iddict[word]),word,'?????????'])
                                num_id += 1
                            else:
                                print('Error in ???{}??????{}???'.format(j,i))
                                num_error += 1
                        #???????????????????????????
                        if line[i] in separater:
                            lists.append([separater[line[i]],line[i],'?????????'])
                        elif line[i] in operator:
                            lists.append([operator[line[i]],line[i],'?????????'])
                    
                    word = ""
                else:
                    continue
    for word in lists:
        print("????????????{1}  ?????????{2}   ?????????{0}".format(word[0],word[1],word[2]))
    print('\n????????????:\n?????????{0}?????????\n??????{1}???\n?????????{2}???\n?????????{3}???\n?????????{4}???\n??????{5}???\n?????????{6}???\n??????{7}???'.format(tot,num_lines,num_keywords,num_separater,num_operator,num_num,num_id,num_error))

main()