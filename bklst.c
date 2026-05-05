#include <stdio.h>

struct s_book {
 int pages;
 char title[64];
 struct  s_book *next;
}; 
typedef struct s_book book;

int main () {
 printf("Hello, World!");
 return 0;
}
