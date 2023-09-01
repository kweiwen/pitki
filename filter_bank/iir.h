#include <iostream>
#include <stdio.h>
#include <stdlib.h>

#pragma once

typedef struct iir_ 
{
    int index_b;
    int index_a;
    int len_a;
    int len_b;
    double *coeff_a;
    double *coeff_b;
    double *x;
    double *y;
    double filtered;
}iir;

typedef struct dual_iir_ 
{
    iir L;
    iir R;
}dual_iir;

void init_iir(iir* self, double* b, double* _a, int bSize, int aSize, double* coeff_b, double* coeff_a, double* x, double* y)
{
    self->len_a = aSize - 1;
    self->len_b = bSize;

    self->coeff_a = coeff_a;
    self->coeff_b = coeff_b;

    double a0 = _a[0];
    const double* a = &_a[1];

    for (int i = 0; i < 2 * self->len_a - 1; i++)
    {
        // std::cout << "index: " << i << "value:" << a[(2 * self->len_a - 2 - i) % self->len_a] / a0 << std::endl;
        self->coeff_a[i] = a[(2 * self->len_a - 2 - i) % self->len_a] / a0;
    }

    for (int i = 0; i < 2 * self->len_b - 1; i++)
    {
        // std::cout << "index: " << i << "value:" << b[(2 * self->len_b - 1 - i) % self->len_b] / a0 << std::endl;
        self->coeff_b[i] = b[(2 * self->len_b - 1 - i) % self->len_b] / a0;
    }

    self->x = x;
    for (int i = 0; i < aSize; i++)
    {
        self->x[i] = 0;
    }

    self->y = y;
    for (int i = 0; i < bSize; i++)
    {
        self->y[i] = 0;
    }

    self->index_a = 0;
    self->index_b = 0;
}

double process_iir(iir* self, double value)
{
    self->x[self->index_b] = value;
    
    double b_terms = 0;
    double* b_shift = &self->coeff_b[self->len_b - self->index_b - 1]; 
    for(int i=0; i < self->len_b; i++)
    {
        b_terms += self->x[i] * b_shift[i];
    }
    
    double a_terms = 0;
    double* a_shift = &self->coeff_a[self->len_a - self->index_a - 1];
    for(int i=0; i < self->len_a; i++)
    {
        a_terms += self->y[i] * a_shift[i];	
    }
    
    double filtered = b_terms - a_terms;
    
    self->y[self->index_a] = filtered;
    self->index_b++;
    if (self->index_b == self->len_b)
    {
        self->index_b = 0;
    }
    self->index_a++;
    if (self->index_a == self->len_a)
    {
        self->index_a = 0;;
    }
    
    self->filtered = filtered;
    return filtered;
} 

void init_dual_iir(dual_iir* self, double* b, double* _a, int bSize, int aSize, double* coeff_b_L, double* coeff_a_L, double* x_L, double* y_L, double* coeff_b_R, double* coeff_a_R, double* x_R, double* y_R)
{
    init_iir(&self->L, b, _a, bSize, aSize, coeff_b_L, coeff_a_L, x_L, y_L);
    init_iir(&self->R, b, _a, bSize, aSize, coeff_b_R, coeff_a_R, x_R, y_R);
}

void process_dual_iir(dual_iir* self, double L, double R)
{
    double outputL = process_iir(&self->L, L);
    double outputR = process_iir(&self->R, R);
}
