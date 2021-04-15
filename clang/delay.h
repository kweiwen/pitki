#include "circularBuffer.h"

typedef struct _delay
{
    circularBuffer digitalDelayLine;
    float delaytime;
    float mix;
    float feedback;
}delay;


void init_delay(delay* self, int bufferLength)
{
    init_circularBuffer(&self->digitalDelayLine, bufferLength); // create only one digital delay line
    self->delaytime = 0;
    self->mix = 0;
    self->feedback = 0;
}


void free_delay(delay* self)
{
    free_circularBuffer(&self->digitalDelayLine);
}


float process_delay(delay *self, float input, float feedback, float delaytime, float mix)
{
    float drySignal = input;
    float wetSignal = read_data(&self->digitalDelayLine, delaytime);
    write_data(&self->digitalDelayLine, drySignal + (wetSignal * feedback));
    return wetSignal * mix + drySignal * (1 - mix);
}