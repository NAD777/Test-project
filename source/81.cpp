#include<iostream>
#include<vector>
#include<cmath>
#define int long long
using namespace std;
signed main()
{
	string s,q,max;
	cin>>s;
	int f=0,d=0;
	for(int i=0;i<s.length();i++)
	f+=s[i]-48;
	for(int i=0;i<s.length();i++)
	max+='0';
	for(int i=0;i<s.length();i++)
	{
		for(int j=0;j<10;j++)
		{
			q="";
			if((f-(s[i]-48)+j)%3!=0||j==s[i]-48)
			continue;
			for(int k=0;k<i;k++)
			q+=s[k];
			q+=char(j+48);
			for(int k=i+1;k<s.length();k++)
			q+=s[k];
			if(q>max)
			max=q;
		}
	}
	cout<<max;
	return 0;
}