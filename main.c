#include <stdio.h>
#include <stdlib.h>

/* alignment macro: aligns a memory block a to multiplies of a */
#define align(s,a) (((size_t)(s) + ((a) - 1)) & ~((size_t) (a) - 1))
/* Alignment for SSE unit */
#define SSE_ALIGN (16)
/* Number of elements */
#define NUM (10)

extern void mymin(long, float *, float *, float *);

int
main(void) {
    float *a = malloc(sizeof(float)*NUM + SSE_ALIGN),
          *b = malloc(sizeof(float)*NUM + SSE_ALIGN),
          *c = malloc(sizeof(float)*NUM + SSE_ALIGN);
    /* make sure that pointers are aligned to multiplies of 16 bytes */
    a = (float *) align(a, SSE_ALIGN);
    b = (float *) align(b, SSE_ALIGN);
    c = (float *) align(c, SSE_ALIGN);

    /* write values to a and b */
    for (int i = 0; i < NUM; i++) {
        a[i] = i;
        b[i] = i * ((i % 5) - 2);
    }

    /* invoke the function written in the vector language */
    mymin(NUM, a, b, c);

    printf("Result for vector a:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\n");
    printf("Result for vector b:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\n");
    /* read values from c */
    printf("Result for vector c:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", c[i]);
        if ((i + 1) % 10 == 0)
            printf("\n");
    }
    printf("\n");

    return 0;
}
