// ========== EXERCICE 1 : Basics ==========
// Écris un programme qui :
// 1. Déclare une variable entière x = 42
// 2. Crée un pointeur p qui pointe vers x
// 3. Affiche la valeur de x, l'adresse de x, et la valeur pointée par p
// 4. Modifie x via le pointeur et affiche le résultat


#include <stdio.h>
#include <stdlib.h>

int main(){
    int x = 42;
    int *p = &x;

    printf("la valeur de x : %d\n", x);
    printf("l'adresse de x : %p\n", &x);
    printf("la valeur pointée de x par p : %d\n", *p);

    *p = 100;
    printf("voici x après l'avoir modifier avec le pointeur : %d", *p);
}