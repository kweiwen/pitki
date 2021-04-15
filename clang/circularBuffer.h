//
//  circularBuffer.h
//  circularBuffer
//
//  Created by kweiwen tseng on 2021/4/15.
//  Copyright © 2021 Sikhaa Electronics. All rights reserved.
//

#ifndef circularBuffer_H_
#define circularBuffer_H_

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct _circularBuffer
{
    float* buffer;
    int readIndex;
    int writeIndex;
    int bufferLength;
    int mask;
}circularBuffer;

void init_circularBuffer(circularBuffer *self, int bufferLength)
{
    self->buffer = calloc(bufferLength, sizeof(float));
    self->readIndex = 0;
    self->writeIndex = 0;
    self->bufferLength = (unsigned int)(powf(2, ceil(logf(bufferLength) / logf(2))));
    self->mask = self->bufferLength - 1;
}

void free_circularBuffer(circularBuffer *self)
{
    free(self->buffer);
}

void flush_data(circularBuffer *self)
{
    for(int index = 0; index < self->bufferLength; index++)
    {
        self->buffer[index] = 0.0;
    }
}

void write_data(circularBuffer *self, float data)
{
    self->buffer[self->writeIndex++] = data;
    self->writeIndex &= self->mask;
}

float read_data(circularBuffer *self, int delay)
{
    self->readIndex = (self->writeIndex - delay);
    self->readIndex &= self->mask;

    return self->buffer[self->readIndex];
}

float doLinearInterpolation(float y1, float y2, float fractional_X)
{
    if (fractional_X >= 1.0) return y2;
    return fractional_X * y2 + (1 - fractional_X)*y1;
}

float doLargrangeInterpolation(float y1, float y2, float fractional_X)
{
    if (fractional_X >= 1.0) return y2;
    return fractional_X * y2 + (1 - fractional_X)*y1;
}

float doHermitInterpolation(float y1, float y2, float fractional_X)
{
    if (fractional_X >= 1.0) return y2;
    return fractional_X * y2 + (1 - fractional_X)*y1;
}

float read_data_interpolation(circularBuffer *self, float delayInFractionalSamples)
{
    float y1 = read_data(self, delayInFractionalSamples);
    float y2 = read_data(self, delayInFractionalSamples + 1);
    float fraction = delayInFractionalSamples - (int)delayInFractionalSamples;

    float interpolation = doLinearInterpolation(y1, y2, fraction);
    return interpolation;
}

void disp_info(circularBuffer *self)
{
    printf("\n\nPrinting the circular buffer:\n");
    printf("---------------------------------\n");
    printf("Buffer: ");
    for(int i=0; i<self->bufferLength; i++)
    {
        printf("%f\t", self->buffer[i]);
    }
    printf("\n");
    printf("Read Index: %d\n", self->readIndex);
    printf("Write Index: %d\n", self->writeIndex);
    printf("\n");
}

#endif /* circularBuffer_H_ */