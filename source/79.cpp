#include<iostream>
#include<vector>
#include<cmath>
#define int long long
using namespace std;
signed main()
{
	int a,b,c,n;
	cin>>a>>b>>c;
	if(2*a<=b&&2*a<=2*c)
	n=a;
	else
	if(2*c<=b&&2*c<=2*a)
	n=c;
	else
	n=b/2;
	a-=n;
	b-=2*n;
	c-=n;
	int otv=4*n;
	if(a==0)
	{
		cout<<otv;
		return 0;
	}
	a--;
	otv++;
	if(b==0)
	{
		cout<<otv;
		return 0;
	}
	b--;
	otv++;
	if(c==0)
	{
		cout<<otv;
		return 0;
	}
	c--;
	otv++;
	if(b==0)
	{
		cout<<otv;
		return 0;
	}
	
	return 0;
}