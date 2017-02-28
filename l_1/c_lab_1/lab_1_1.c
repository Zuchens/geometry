#include "predicates.c"
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char* getfield(char* line, int num)
{
    const char* tok;
    for (tok = strtok(line, ";");
            tok && *tok;
            tok = strtok(NULL, ";\n"))
    {
        if (!--num)
            return tok;
    }
    return NULL;
}
double det(double* pa, double* pb,double* pc){
    double d = pa[0]*pb[1]+pb[0]*pc[1]+pc[0]*pa[1]-pc[0]*pb[1]-pb[0]*pa[1]-pa[0]*pc[1];
    return d;
}
void points_100(FILE* stream,double* pa,double* pb){
    clock_t begin = clock();
    char line[1024];
    FILE *f = fopen("input.txt", "w");
    while (fgets(line, 1024, stream))
    {
        char* tmp = strdup(line);
        char* tmp2 = tmp;
        char* y_char= getfield(tmp2, 2);
        char* x_char= getfield(tmp, 1);
        double x;
        sscanf(x_char,"%lf", &x);
        double y;
        sscanf(y_char,"%lf", &y);
        double pc[2] ={x,y};
        double is_left  = det(pa,pb,pc);
        fprintf(f,"%f\n", is_left);
        free(tmp);
    }
    fclose(f);
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("%f",time_spent);
}
void points_10_14(FILE* stream,double* pa,double* pb){
    clock_t begin = clock();
    char line[1024];
    while (fgets(line, 1024, stream))
    {
        char* tmp = strdup(line);
        char* tmp2 = tmp;
        char* y_char= getfield(tmp2, 2);
        char* x_char= getfield(tmp, 1);
        double x;
        sscanf(x_char,"%lf", &x);
        double y;
        sscanf(y_char,"%lf", &y);
        double pc[2] ={x,y};
        double is_left  = orient2dexact(pa,pb,pc);
        //printf("Field 3 would be %f \n",is_left);
        free(tmp);
    }
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("%f",time_spent);
}

int main()
{
    exactinit();
    double pa[2] = {-1.0,0.0};
    double pb[2] = {1.0,0.1};
    FILE* stream = fopen("100_points.csv", "r");
    points_100(stream,pa,pb);
    //FILE* stream_14 = fopen("10_14_points.csv", "r");
    //points_10_14(stream_14,pa,pb);


}
