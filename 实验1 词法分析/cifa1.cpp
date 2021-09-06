        /*************Written By Zzg************/
           /*******Date : 11,25,2017********/
 
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
 
using namespace std;
string KEYWORD[15]={"if","else","void","return","while","then","for","do",      //关键字
                    "int","char","double","float","case","cin","cout"};
char SEPARATER[8]={';',',','{','}','[',']','(',')'};    //分隔符
char OPERATOR[8]={'+','-','*','/','>','<','=','!'};     //运算符
char FILTER[4]={' ','\t','\r','\n'};                    //过滤符
const int IDENTIFIER=100;         //标识符值
const int CONSTANT=101;           //常数值
const int FILTER_VALUE=102;       //过滤字符值
 
 
/**判断是否为关键字**/
bool IsKeyword(string word){
    for(int i=0;i<15;i++){
        if(KEYWORD[i]==word){
            return true;
        }
    }
    return false;
}
/**判断是否为分隔符**/
bool IsSeparater(char ch){
    for(int i=0;i<8;i++){
        if(SEPARATER[i]==ch){
            return true;
        }
    }
    return false;
}
 
/**判断是否为运算符**/
bool IsOperator(char ch){
    for(int i=0;i<8;i++){
        if(OPERATOR[i]==ch){
            return true;
        }
    }
    return false;
}
/**判断是否为过滤符**/
bool IsFilter(char ch){
    for(int i=0;i<4;i++){
        if(FILTER[i]==ch){
            return true;
        }
    }
    return false;
}
/**判断是否为大写字母**/
bool IsUpLetter(char ch){
    if(ch>='A' && ch<='Z') return true;
    return false;
}
/**判断是否为小写字母**/
bool IsLowLetter(char ch){
    if(ch>='a' && ch<='z') return true;
    return false;
}
/**判断是否为数字**/
bool IsDigit(char ch){
    if(ch>='0' && ch<='9') return true;
    return false;
}
/**返回每个字的值**/
template <class T>
int value(T *a,int n,T str){
	for(int i=0;i<n;i++){
		if(a[i]==str) return i+1;
	}
	return -1;
}
/**词法分析**/
void analyse(FILE * fpin){
    char ch=' ';
    string arr="";
    while((ch=fgetc(fpin))!=EOF){
        arr="";
        if(IsFilter(ch)){}              //判断是否为过滤符
        else if(IsLowLetter(ch)){       //判断是否为关键字
            while(IsLowLetter(ch)){
				arr += ch;
				ch=fgetc(fpin);
            }
			//fseek(fpin,-1L,SEEK_CUR);
			if(IsKeyword(arr)){
                printf("%3d    ",value(KEYWORD,15,arr));
				cout<<arr<<"  关键字"<<endl;
			}
			else
            {
                printf("%3d    ",IDENTIFIER);
                cout<<arr<<"  标识符"<<endl;
            }
        }
        else if(IsDigit(ch)){           //判断是否为数字
            while(IsDigit(ch)||(ch=='.'&&IsDigit(fgetc(fpin)))){
                arr += ch;
                ch=fgetc(fpin);
            }
            fseek(fpin,-1L,SEEK_CUR);
            printf("%3d    ",CONSTANT);
            cout<<arr<<"  整形数"<<endl;
        }
        else if(IsUpLetter(ch)||IsLowLetter(ch)||ch=='_'){
            while(IsUpLetter(ch)||IsLowLetter(ch)||ch=='_'||IsDigit(ch)){
                arr += ch;
                ch=fgetc(fpin);
            }
            fseek(fpin,-1L,SEEK_CUR);
            printf("%3d    ",CONSTANT);
            cout<<arr<<"  标识符"<<endl;
        }
        else switch(ch){
        case '+':
        case '-':
        case '*':
        case '/':
        case '>':
        case '<':
        case '=':
        case '!':
            {
                arr += ch;
                printf("%3d    ",value(OPERATOR,8,*arr.data()));
                cout<<arr<<"  运算符"<<endl;
                break;
            }
        case ';':
        case ',':
        case '(':
        case ')':
        case '[':
        case ']':
        case '{':
        case '}':
            {
              arr += ch;
              printf("%3d    ",value(SEPARATER,8,*arr.data()));
              cout<<arr<<"  分隔符"<<endl;
              break;
            }
        default :cout<<"\""<<ch<<"\":无法识别的字符！"<<endl;
        }
    }
 
}
int main()
{
    char inFile[40];
    FILE *fpin;
    cout<<"请输入源文件名（包括路径和后缀）:";
    while(true){
        cin>>inFile;
        if((fpin=fopen(inFile,"r"))!=NULL)
            break;
        else{
            cout<<"文件名错误！"<<endl;
            cout<<"请输入源文件名（包括路径和后缀）:";
        }
 
    }
    cout<<"------词法分析如下------"<<endl;
    analyse(fpin);
    return 0;
}

