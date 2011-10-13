#include <stdio.h>
#include <stdlib.h>

/* alignment macro: aligns a memory block a to multiplies of a */
#define align(s,a) (((size_t)(s) + ((a) - 1)) & ~((size_t) (a) - 1))
/* Alignment for SSE unit */
#define SSE_ALIGN (16)
/* Number of elements */
#define NUM (12)

extern void ml0(long, float *);
extern void ml1(long, float *);
extern void ml2(long, float *);
extern void ml3(long, float *);
extern void ml4(long, float *);
extern void ml5(long, float *);
extern void ml6(long, float *);
extern void ml7(long, float *);
extern void ml8(long, float *);
extern void ml9(long, float *);

int
main(void) {
    float *a = malloc(sizeof(float)*NUM + SSE_ALIGN);
    /* make sure that pointers are aligned to multiplies of 16 bytes */
    a = (float *) align(a, SSE_ALIGN);

    /* write values to a and b */
    for (int i = 0; i < NUM; i++) {
        a[i] = i;
    }

    /* invoke the function written in the vector language */
    ml0(NUM, a);

    /* read values from c */
    printf("Result for vector a after ml0:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\n");

    ml1(NUM, a);
    printf("Result for vector a after ml1:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\n");

    ml2(NUM, a);
    printf("Result for vector a after ml2:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\n");

    ml3(NUM, a);
    printf("Result for vector a after ml3:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\n");

    ml4(NUM, a);
    printf("Result for vector a after ml4:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\n");

    ml5(NUM, a);
    printf("Result for vector a after ml5:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\n");

    ml6(NUM, a);
    printf("Result for vector a after ml6:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\n");

    ml7(NUM, a);
    printf("Result for vector a after ml7:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\n");

    ml8(NUM, a);
    printf("Result for vector a after ml8:\n");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\n");

    return 0;
}
