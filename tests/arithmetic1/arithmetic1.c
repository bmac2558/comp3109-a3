#include <stdio.h>
#include <stdlib.h>

/* alignment macro: aligns a memory block a to multiplies of a */
#define align(s,a) (((size_t)(s) + ((a) - 1)) & ~((size_t) (a) - 1))
/* Alignment for SSE unit */
#define SSE_ALIGN (16)
/* Number of elements */
#define NUM (8)

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
extern void arithmetic13(long, float *, float *, float *);
extern void arithmetic14(long, float *, float *, float *, float *, float *);

void printit(char *name, float *vector) {
    printf("%s: ", name);
    for (int i = 0; i < NUM; i++)
        printf("%f ", vector[i]);
    printf("\n");
}

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
    printit("a", a);
    printit("b", b);
    printit("c", c);
    printit("d", d);
    printit("e", e);


    printf("\n== Arithmetic 1.1 ==\n");
    arithmetic11(NUM, a, b, c);

    printit("a", a);
    printit("b", b);
    printit("c", c);


    printf("\n== Add ==\n");
    add(NUM, a, b, c);

    printit("a", a);
    printit("b", b);
    printit("c", c);

    printf("\n== Sub ==\n");
    sub(NUM, d, a, c);

    printit("d", d);
    printit("a", a);
    printit("c", c);

    printf("\n== Mul ==\n");
    mul(NUM, a, b, c);

    printit("a", a);
    printit("b", b);
    printit("c", c);

    printf("\n== Div ==\n");
    divv(NUM, a, b, c);

    printit("a", a);
    printit("b", b);
    printit("c", c);


    printf("\n== iAdd ==\n");
    iadd(NUM, a, b);

    printit("a", a);
    printit("b", b);

    printf("\n== iSub ==\n");
    isub(NUM, a, b);

    printit("a", a);
    printit("b", b);

    printf("\n== iMul ==\n");
    imul(NUM, a, b);

    printit("a", a);
    printit("b", b);

    printf("\n== iDiv ==\n");
    idiv(NUM, a, b);

    printit("a", a);
    printit("b", b);


    printf("\n== Arithmetic 1.2 ==\n");
    arithmetic12(NUM, a, e, b);

    printit("a", a);
    printit("e", e);
    printit("b", b);


    printf("\n== Arithmetic 1.3 ==\n");
    arithmetic13(NUM, a, e, b);

    printit("a", a);
    printit("e", e);
    printit("b", b);
 

    printf("\n== Arithmetic 1.4 ==\n");
    for (int i = 0; i < NUM; i++) {
        a[i] = i + 1;
        b[i] = i + 2;
        c[i] = i + 3;
        d[i] = i + 4;
        e[i] = i * 2;
    }
    arithmetic14(NUM, a, b, c, d, e);

    printit("a", a);
    printit("b", b);
    printit("c", c);
    printit("d", d);
    printit("e", e);

    return 0;
}
