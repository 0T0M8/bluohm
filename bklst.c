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
int numbks = 0;

void mkbk(char *title, int pages) {
 book *newbk, *tmpbk;
 if (!head) { 
 tmpbk = malloc(sizeof(book));
 if (!tmpbk) { printf("malloc failed!"); exit(1); }
 numbks++;
 memset(tmpbk, 0, sizeof(book));
 tmpbk->pages = pages;
 strncpy(tmpbk->title, title, 63);
 tmpbk->title[63] = '\0';
 tmpbk->next = NULL;
 head = tmpbk;
 return;
 }

 for (tmpbk=head; tmpbk->next; tmpbk=tmpbk->next);
 
 newbk = malloc(sizeof(book));
 if (!tmpbk) { printf("malloc failed!"); exit(1); }
 numbks++; 
 memset(newbk, 0, sizeof(book));
 newbk->pages = pages;
 strncpy(newbk->title, title, 63);
 newbk->title[63] = '\0';
 newbk->next = NULL;
 
 tmpbk->next = newbk;
}

void lsbk(char *searchstr) {
 book *tmpbk;
 for (tmpbk=head; tmpbk; tmpbk=tmpbk->next)
  if ( !searchstr || strcmp(searchstr, tmpbk->title) == 0)
   printf("Pages:%d\t%s\n", tmpbk->pages, tmpbk->title); 
}

void rmbk(char *searchstr) {
 book *tmpbk, *prev;
 for (tmpbk=head, prev=tmpbk; tmpbk; tmpbk=tmpbk->next) {
  if ( strcmp(tmpbk->title, searchstr)==0 ) {
    if (tmpbk == head) {
      head = tmpbk->next;
      free(tmpbk); 
    } else {
      prev->next = (tmpbk->next) ? tmpbk->next: 0;
    }
  free(tmpbk);
  }
 }
}

int main () {
 mkbk("The Fault in Our Stars", 367);
 mkbk("Stollen", 477);
 mkbk("The Boy Who Harnessed the Wind", 730);
 mkbk("Grit", 730);
 mkbk("To Kill a Mockingbird", 576); 
 mkbk("Grit", 331);
 mkbk("The Diary of Anne Frank", 355);
 mkbk("Circles of Gold", 730);
 mkbk("Cain & Abel", 730);
 mkbk("Astra and Hugo", 412);
 mkbk("Around the World in 80 Days", 210);
 mkbk("5 months in a Balloon", 635);

 printf("BookCount: %d", numbks);
 printf("\n..................................\n"); 
 lsbk(0); 
 printf("\n..................................\n");
 rmbk("Stollen");
 lsbk(0);
 return 0;
}
