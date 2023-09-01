#include "iir.h"
#pragma once

typedef struct coupled_allpass_ 
{
    iir h1;
    iir h2;
    double pos;
    double neg;
}coupled_allpass;

typedef struct stereo_coupled_allpass_ 
{
    coupled_allpass L;
    coupled_allpass R;
}stereo_coupled_allpass;

void init_allpass(iir* self, int aSize, double* coeff_a, double* x, double* y)
{
    self->len_a = aSize;

    self->coeff_a = coeff_a;
    
    self->x = x;
    for (int i = 0; i < aSize; i++)
    {
        self->x[i] = 0;
    }

    self->y = y;
    for (int i = 0; i < aSize; i++)
    {
        self->y[i] = 0;
    }

    self->index_a = 0;
}

double process_allpass(iir* self, double value) 
{
    self->x[self->index_a] = value;
    
    // Feed-forward (using coeff_a in reverse order)
    double b_terms = 0;
    for (uint8_t i = 0; i < self->len_a; i++) 
    {
        b_terms += self->x[(self->index_a + self->len_a - i) % self->len_a] * self->coeff_a[self->len_a - 1 - i];
    }
    
    // Feed-back (using coeff_a in provided order)
    double a_terms = 0;
    for (uint8_t i = 1; i < self->len_a; i++) 
    { 
        // start from 1 because a[0] = 1 for the current output
        a_terms += self->y[(self->index_a + self->len_a - i) % self->len_a] * self->coeff_a[i];
    }

    double filtered = b_terms - a_terms;
    self->y[self->index_a] = filtered;

    self->index_a++;
    if(self->index_a == self->len_a)
        self->index_a = 0;
    
    self->filtered = filtered;
    return filtered;
}

void init_coupled_allpass(coupled_allpass* self, int d1, double* coeff_d1, int d2, double* coeff_d2, double* h1x, double* h1y, double* h2x, double* h2y)
{
    init_allpass(&self->h1, d1, coeff_d1, h1x, h1y);
    init_allpass(&self->h2, d2, coeff_d2, h2x, h2y);
}

void process_coupled_allpass(coupled_allpass* self, double value)
{
    process_allpass(&self->h1, value);
    process_allpass(&self->h2, value);
    
    self->pos = (self->h1.filtered + self->h2.filtered) * 0.5;
    self->neg = (self->h1.filtered - self->h2.filtered) * 0.5;
}

void init_stereo_coupled_allpass(stereo_coupled_allpass* self, int d1_size, double* coeff_d1, int d2_size, double* coeff_d2, double* h1xL, double* h1yL, double* h2xL, double* h2yL, double* h1xR, double* h1yR, double* h2xR, double* h2yR)
{
    init_coupled_allpass(&self->L, d1_size, coeff_d1, d2_size, coeff_d2, h1xL, h1yL, h2xL, h2yL);
    init_coupled_allpass(&self->R, d1_size, coeff_d1, d2_size, coeff_d2, h1xR, h1yR, h2xR, h2yR);
}

void process_stereo_coupled_allpass(stereo_coupled_allpass* self, double L, double R)
{
    process_coupled_allpass(&self->L, L);
    process_coupled_allpass(&self->R, R);
}

void init_stereo_allpass(dual_iir* self, int a, double* coeff_a, double* xL, double* yL, double* xR, double* yR)
{
    init_allpass(&self->L, a, coeff_a, xL, yL);
    init_allpass(&self->R, a, coeff_a, xR, yR);
}

void process_stereo_allpass(dual_iir* self, double L, double R)
{
    process_allpass(&self->L, L);
    process_allpass(&self->R, R);
}