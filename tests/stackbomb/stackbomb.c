#include <stdio.h>
#include <stdlib.h>

/* alignment macro: aligns a memory block a to multiplies of a */
#define align(s,a) (((size_t)(s) + ((a) - 1)) & ~((size_t) (a) - 1))
/* Alignment for SSE unit */
#define SSE_ALIGN (16)
/* Number of elements */
#define NUM (16)

extern void stackbomb(long, float *);

int
main(void) {
    float *a = malloc(sizeof(float)*NUM + SSE_ALIGN);
    /* make sure that pointers are aligned to multiplies of 16 bytes */
    a = (float *) align(a, SSE_ALIGN);

    /* write values to a and b */
    for (int i = 0; i < NUM; i++) {
        a[i] = i;
    }

    printf("Starting val for vector a:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
        if ((i + 1) % 10 == 0)
            printf("\n");
    }
    printf("\n");

    /* invoke the function written in the vector language */
    stackbomb(NUM, a);

    /* read values from c */
    printf("Result for vector a:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
        if ((i + 1) % 10 == 0)
            printf("\n");
    }
    printf("\n");

    return 0;
}
