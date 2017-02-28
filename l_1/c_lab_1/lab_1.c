#include "predicates.c"
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
const char* getfield(char* line, int num)
{
    const char* tok;
    for (tok = strtok(line, ",");
        tok && *tok;
        tok = strtok(NULL, ",\n"))
    {
    if (!--num)
        return tok;
    }
    return NULL;
}

int main(){
    FILE* stream = fopen("file2.csv","r");
    char line[1024];
    while (fgets(line, 1024, stream))
    {
        char* tmp = strdup(line);
        double pa;
        sscanf(getfield(tmp, 1),"%lf", &pa);
        //double pb;
        //sscanf(getfield(tmp, 2),"%lf", &pb);
        printf("Field 3 would be %s\n", getfield(tmp, 2));
        free(tmp);
    }
    exactinit();
    /*double pa[2] = {-1.0,0.0};
    double pb[2] = {1.0,0.1};
    double pc[2] ={-1.2,1.1};
    clock_t begin = clock();
    int a  = orient2d(pa,pb,pc);
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("%f",time_spent);
    printf("%d",a);*/
    return 0;
}
