#include <bits/stdc++.h>
using namespace std;
int main(){
	long long n,m,x,y,k;
	cin >> n >> m >> x >> y >> k;
	vector < vector  <int > > v(n+2,vector <int> (m+2,0));
	v[k+1][1]=1;	
	for(int i=1;i<=n;i++){
		for (int j=1;j<=m;j++){
			v[i][j]=v[i-1][j]+v[i][j-1]+v[i][j];
		}
	}
	if(v[x+1][y+1]>0)
		cout << "YES" << endl << v[x+1][y+1];
	else
		cout << "NO";
	
	
	
	
	
	
	
	return 0;
}