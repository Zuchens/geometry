#include<iostream>
using namespace std;

struct Point
{
    int x, y;
};

int main()
{
    Point points[] = {{0, 3}, {2, 2}, {1, 1}, {2, 1},
                      {3, 0}, {0, 0}, {3, 3}};
    int n = sizeof(points)/sizeof(points[0]);
    cout << n;
    return 0;
}

