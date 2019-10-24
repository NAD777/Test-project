#include<iostream>
#include<vector>
#include<cmath>
#define int long long
using namespace std;
bool flag;
int endd=0;
void rec(int n,int m,int k,vector<int>&v,int &end)
{
	if(flag)
	return;
	if(n==m)
	{
		flag=true;
		endd=end;
		return;
	}
	else
	if(k<10)
	{
		//cout<<k<<' '<<n/10*10+(n/10+n%10)%10<<"      "<< (n/10+n%10)%10*10+n%10<<endl;
		end++;
		v[end]=n/10*10+(n/10+n%10)%10;
		if(v[end]>10)
		rec(v[end],m,k+1,v,end);
		if(flag)
		return;
		v[end]=(n/10+n%10)%10*10+n%10;
		if(v[end]>10)
		rec(v[end],m,k+1,v,end);
		end--;
	}
}
signed main()
{
	int n,m;
	cin>>n>>m;
	vector<int>v(15,0);
	int end=0;
	v[0]=n;
	rec(n,m,0,v,end);
	if(flag)
	{
		cout<<"YES"<<endl;
		for(int i=0;i<=endd;i++)
		cout<<v[i]<<' ';
	}
	else
	cout<<"NO"<<endl;
	return 0;
}