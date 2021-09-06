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

while True:
    word = input('变量名：')
    print(isid(word))