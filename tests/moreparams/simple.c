#include <stdio.h>
#include <stdlib.h>

/* alignment macro: aligns a memory block a to multiplies of a */
#define align(s,a) (((size_t)(s) + ((a) - 1)) & ~((size_t) (a) - 1))
/* Alignment for SSE unit */
#define SSE_ALIGN (16)
/* Number of elements */
#define NUM (3)

extern void simple(long, float *);

int
main(void) {
    float *a = malloc(sizeof(float)*NUM + SSE_ALIGN);
    /* make sure that pointers are aligned to multiplies of 16 bytes */
    a = (float *) align(a, SSE_ALIGN);
    
    float *b = malloc(sizeof(float)*NUM + SSE_ALIGN);
    /* make sure that pointers are aligned to multiplies of 16 bytes */
    b = (float *) align(a, SSE_ALIGN);
   
    float *c = malloc(sizeof(float)*NUM + SSE_ALIGN);
    /* make sure that pointers are aligned to multiplies of 16 bytes */
    c = (float *) align(a, SSE_ALIGN);

    float *d = malloc(sizeof(float)*NUM + SSE_ALIGN);
    /* make sure that pointers are aligned to multiplies of 16 bytes */
    d = (float *) align(a, SSE_ALIGN);

    float *e = malloc(sizeof(float)*NUM + SSE_ALIGN);
    /* make sure that pointers are aligned to multiplies of 16 bytes */
    e = (float *) align(a, SSE_ALIGN);

    float *f = malloc(sizeof(float)*NUM + SSE_ALIGN);
    /* make sure that pointers are aligned to multiplies of 16 bytes */
    f = (float *) align(a, SSE_ALIGN);

    /* write values to a and b */
    for (int i = 0; i < 3; i++) {
        a[i] = i;
    }
    for (int i = 0; i < 3; i++) {
        b[i] = i;
    }
    for (int i = 0; i < 3; i++) {
        c[i] = i;
    }
    for (int i = 0; i < 3; i++) {
        d[i] = i;
    }
    for (int i = 0; i < 3; i++) {
        e[i] = i;
    }
    for (int i = 0; i < 3; i++) {
        f[i] = i;
    }

    /* invoke the function written in the vector language */
    simple(NUM, a, b, c, d, e, f);

    /* read values from c */
    printf("Result for vector a:\n");
    for (int i = 0; i < 100; i++) {
        printf("%f ", a[i]);
        if ((i + 1) % 10 == 0)
            printf("\n");
    }
    printf("\n");

    return 0;
}
