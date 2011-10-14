#include <stdio.h>
#include <stdlib.h>

/* alignment macro: aligns a memory block a to multiplies of a */
#define align(s,a) (((size_t)(s) + ((a) - 1)) & ~((size_t) (a) - 1))
/* Alignment for SSE unit */
#define SSE_ALIGN (16)
/* Number of elements */
#define NUM (4)

extern void arithmetic11(long, float *, float *, float *);
extern void add(long, float *, float *, float *);
extern void sub(long, float *, float *, float *);
extern void mul(long, float *, float *, float *);
extern void divv(long, float *, float *, float *);
extern void iadd(long, float *, float *);
extern void isub(long, float *, float *);
extern void imul(long, float *, float *);
extern void idiv(long, float *, float *);
extern void arithmetic12(long, float *, float *, float *);
extern void arithmetic13(long, float *, float *, float *, float *, float *);

int
main(void) {
    float *a = malloc(sizeof(float)*NUM + SSE_ALIGN),
          *b = malloc(sizeof(float)*NUM + SSE_ALIGN),
          *c = malloc(sizeof(float)*NUM + SSE_ALIGN),
          *d = malloc(sizeof(float)*NUM + SSE_ALIGN),
          *e = malloc(sizeof(float)*NUM + SSE_ALIGN);
    /* make sure that pointers are aligned to multiplies of 16 bytes */
    a = (float *) align(a, SSE_ALIGN);
    b = (float *) align(b, SSE_ALIGN);
    c = (float *) align(c, SSE_ALIGN);
    d = (float *) align(d, SSE_ALIGN);
    e = (float *) align(e, SSE_ALIGN);

    /* write values to a and b */
    for (int i = 0; i < NUM; i++) {
        a[i] = i + 1;
        b[i] = i + 2;
        c[i] = i + 3;
        d[i] = i + 4;
        e[i] = i * 2;
    }

    printf("a: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nb: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\nc: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", c[i]);
    }
    printf("\nd: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", d[i]);
    }
    printf("\ne: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", e[i]);
    }
    printf("\n");


    /* invoke the function written in the vector language */
    printf("== Arithmetic 1.1 ==");
    arithmetic11(NUM, a, b, c);

    /* read values from c */
    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nb: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\nc: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", c[i]);
    }
    printf("\n");

    printf("== Add ==");
    add(NUM, a, b, c);

    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nb: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\nc: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", c[i]);
    }
    printf("\n");

    printf("== Sub ==");
    sub(NUM, d, a, c);

    printf("\nd: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", d[i]);
    }
    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nc: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", c[i]);
    }
    printf("\n");

    printf("== Mul ==");
    mul(NUM, a, b, c);

    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nb: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\nc: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", c[i]);
    }
    printf("\n");

    printf("== Div ==");
    divv(NUM, a, b, c);

    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nb: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\nc: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", c[i]);
    }
    printf("\n");

    printf("== iAdd ==");
    iadd(NUM, a, b);

    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nb: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\n");

    printf("== iSub ==");
    isub(NUM, a, d);

    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nd: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", d[i]);
    }
    printf("\n");

    printf("== iMul ==");
    imul(NUM, a, b);

    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nb: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\n");

    printf("== iDiv ==");
    idiv(NUM, a, b);

    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nb: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\n");


    printf("== Arithmetic 1.2 ==");
    arithmetic12(NUM, a, e, b);

    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\ne: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", e[i]);
    }
    printf("\nb: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\n");


    printf("== Arithmetic 1.3 ==");
    arithmetic13(NUM, a, b, c, d, e);

    printf("\na: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", a[i]);
    }
    printf("\nb: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", b[i]);
    }
    printf("\nc: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", c[i]);
    }
    printf("\nd: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", d[i]);
    }
    printf("\ne: ");
    for (int i = 0; i < NUM; i++) {
        printf("%f ", e[i]);
    }
    printf("\n");

    return 0;
}
