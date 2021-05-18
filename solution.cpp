#include <iostream>
#include <string>
using namespace std;
int main() {

    //freopen("input.txt","r",stdin);
    long long n; cin >> n;
    while(n != 1) {
        cout << n << " ";
        if(n&1) n = 3*n + 1;
        else n >>= 1;
    }
    cout << n << endl;
    return 0;
}
