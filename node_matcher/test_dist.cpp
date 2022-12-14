#include "dist.h"

int main(){
    double p_x = 121.396, p_y = 31.159;
    double n1_x = 121.394, n1_y = 31.1627, n2_x = 121.394, n2_y=31.1626;
    cout << getNearestDistance(n1_x, n1_y, n2_x, n2_y, p_x, p_y) << endl;
}