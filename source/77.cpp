#include <bits/stdc++.h>
using namespace std;
int main(){
	int a,b,s=0;
	cin >> a >> b;
	if(a>b)
		swap(a,b);
	for (int i=a-1,j=b-2;i>=0 && j>0;i--,j--){
		s+=i;
		if(i>=1)
			s+=j;	
	}
	
	cout << s;		
	
	
	
	
	return 0;
}