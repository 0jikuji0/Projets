// ========== EXERCICE 2 : Allocation dynamique ==========
// Écris une fonction qui :
// 1. Alloue dynamiquement un tableau de 5 entiers
// 2. Le remplit avec les valeurs 1, 2, 3, 4, 5
// 3. L'affiche
// 4. Le libère correctement

#include <stdio.h>
#include <stdlib.h>

int main()
{
    int *tab = (int *)malloc(5 * sizeof(int));
    
    if (tab == NULL)
    {
        printf("Erreur d'allocation\n");
        return 0;
    }

    for (int i = 0; i < 5; i++)
    {
        tab[i] = i + 1;
    }

    printf("Tableau : ");

    for (int i = 0; i < 5; i++)
    {
        printf("%d ", tab[i]);
    }
    printf("\n");

    free(tab);
}