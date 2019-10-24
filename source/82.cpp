#include<iostream>
#include<vector>
#include<cmath>
#define int long long
using namespace std;
int fak(int n)
{
	int f=1;
	for(int i=2;i<=n;i++)
	f*=i;
	return f;
}
signed main()
{
	int n,m,x,y,k;
	cin>>n>>m>>x>>y>>k;
	if(k>y)
	{
		cout<<"NO"<<endl;
		return 0;
	}
	y-=k;
	cout<<fak(x+y)/fak(x)/fak(y);
	return 0;
}
