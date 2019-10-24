#include <bits/stdc++.h>
using namespace std;
int main(){
	long long k=0,f=0;	
	string s;
	cin >> s;
	for (int i=0;i<s.length();i++)
		k=k+(s[i]-48);
		
	for (int j=0;j<s.length();j++){
		for (int i=8;i>=1;i--){
			if((k+i)%3==0&&int(s[j]-48)+i<10){
				s[j]=s[j]+char(i);
				cout << s;
				return 0;	
			}
		}
	}
	for (int j=s.length()-1;j>=0;j--){
		for (int i=1;i<=8;i++){
			if((k-i)%3==0&&int(s[j]-48)-i>0){
				s[j]=s[j]-char(i);
				cout << s;
				return 0;	
			}
		}
	}

	
	
	
	
	
	return 0;
}