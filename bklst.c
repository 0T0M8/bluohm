#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct s_book {
 int pages;
 char title[64];
 struct  s_book *next;
}; 
typedef struct s_book book;

book *head = NULL;

void mkbk(char *title, int pages) {
 book *newbk, *tmpbk;
 while (!head) { 
 tmpbk = malloc(sizeof(book));
 memset(tmpbk, 0, sizeof(book));
 tmpbk->pages = pages;
 strcpy(tmpbk->title, title);
 tmpbk->title[63] = '\0';
 tmpbk->next = 0;
 newbk = tmpbk;
 head = newbk;
 }

 for (tmpbk=head; tmpbk; tmpbk=tmpbk->next);
 
 tmpbk = malloc(sizeof(book));
 memset(tmpbk, 0, sizeof(book));
 tmpbk->pages = pages;
 strcpy(tmpbk->title, title);
 tmpbk->title[63] = '\0';
 tmpbk->next = NULL;
 newbk = tmpbk;
}

void lsbk(char *searchstr) {
 book *tmpbk;
 for (tmpbk=head; tmpbk; tmpbk=tmpbk->next)
  if ( !searchstr || strcmp(searchstr, tmpbk->title) == 0)
   printf("%s %d\n", tmpbk->title, tmpbk->pages); 
}

int main () {
 mkbk("The Fault in Our Stars", 367);
 printf("New Book Inserted...\n");
 
 lsbk(0); 
 return 0;
}
