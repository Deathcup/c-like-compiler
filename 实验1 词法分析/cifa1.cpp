        /*************Written By Zzg************/
           /*******Date : 11,25,2017********/
 
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
 
using namespace std;
string KEYWORD[15]={"if","else","void","return","while","then","for","do",      //�ؼ���
                    "int","char","double","float","case","cin","cout"};
char SEPARATER[8]={';',',','{','}','[',']','(',')'};    //�ָ���
char OPERATOR[8]={'+','-','*','/','>','<','=','!'};     //�����
char FILTER[4]={' ','\t','\r','\n'};                    //���˷�
const int IDENTIFIER=100;         //��ʶ��ֵ
const int CONSTANT=101;           //����ֵ
const int FILTER_VALUE=102;       //�����ַ�ֵ
 
 
/**�ж��Ƿ�Ϊ�ؼ���**/
bool IsKeyword(string word){
    for(int i=0;i<15;i++){
        if(KEYWORD[i]==word){
            return true;
        }
    }
    return false;
}
/**�ж��Ƿ�Ϊ�ָ���**/
bool IsSeparater(char ch){
    for(int i=0;i<8;i++){
        if(SEPARATER[i]==ch){
            return true;
        }
    }
    return false;
}
 
/**�ж��Ƿ�Ϊ�����**/
bool IsOperator(char ch){
    for(int i=0;i<8;i++){
        if(OPERATOR[i]==ch){
            return true;
        }
    }
    return false;
}
/**�ж��Ƿ�Ϊ���˷�**/
bool IsFilter(char ch){
    for(int i=0;i<4;i++){
        if(FILTER[i]==ch){
            return true;
        }
    }
    return false;
}
/**�ж��Ƿ�Ϊ��д��ĸ**/
bool IsUpLetter(char ch){
    if(ch>='A' && ch<='Z') return true;
    return false;
}
/**�ж��Ƿ�ΪСд��ĸ**/
bool IsLowLetter(char ch){
    if(ch>='a' && ch<='z') return true;
    return false;
}
/**�ж��Ƿ�Ϊ����**/
bool IsDigit(char ch){
    if(ch>='0' && ch<='9') return true;
    return false;
}
/**����ÿ���ֵ�ֵ**/
template <class T>
int value(T *a,int n,T str){
	for(int i=0;i<n;i++){
		if(a[i]==str) return i+1;
	}
	return -1;
}
/**�ʷ�����**/
void analyse(FILE * fpin){
    char ch=' ';
    string arr="";
    while((ch=fgetc(fpin))!=EOF){
        arr="";
        if(IsFilter(ch)){}              //�ж��Ƿ�Ϊ���˷�
        else if(IsLowLetter(ch)){       //�ж��Ƿ�Ϊ�ؼ���
            while(IsLowLetter(ch)){
				arr += ch;
				ch=fgetc(fpin);
            }
			//fseek(fpin,-1L,SEEK_CUR);
			if(IsKeyword(arr)){
                printf("%3d    ",value(KEYWORD,15,arr));
				cout<<arr<<"  �ؼ���"<<endl;
			}
			else
            {
                printf("%3d    ",IDENTIFIER);
                cout<<arr<<"  ��ʶ��"<<endl;
            }
        }
        else if(IsDigit(ch)){           //�ж��Ƿ�Ϊ����
            while(IsDigit(ch)||(ch=='.'&&IsDigit(fgetc(fpin)))){
                arr += ch;
                ch=fgetc(fpin);
            }
            fseek(fpin,-1L,SEEK_CUR);
            printf("%3d    ",CONSTANT);
            cout<<arr<<"  ������"<<endl;
        }
        else if(IsUpLetter(ch)||IsLowLetter(ch)||ch=='_'){
            while(IsUpLetter(ch)||IsLowLetter(ch)||ch=='_'||IsDigit(ch)){
                arr += ch;
                ch=fgetc(fpin);
            }
            fseek(fpin,-1L,SEEK_CUR);
            printf("%3d    ",CONSTANT);
            cout<<arr<<"  ��ʶ��"<<endl;
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
                cout<<arr<<"  �����"<<endl;
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
              cout<<arr<<"  �ָ���"<<endl;
              break;
            }
        default :cout<<"\""<<ch<<"\":�޷�ʶ����ַ���"<<endl;
        }
    }
 
}
int main()
{
    char inFile[40];
    FILE *fpin;
    cout<<"������Դ�ļ���������·���ͺ�׺��:";
    while(true){
        cin>>inFile;
        if((fpin=fopen(inFile,"r"))!=NULL)
            break;
        else{
            cout<<"�ļ�������"<<endl;
            cout<<"������Դ�ļ���������·���ͺ�׺��:";
        }
 
    }
    cout<<"------�ʷ���������------"<<endl;
    analyse(fpin);
    return 0;
}

