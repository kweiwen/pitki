from math import pi
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt

def _higherorder(fc, sr, index, orderindex, norm=True):
    omega = 2 * pi * fc / sr
    sineOmega = np.sin(omega)
    cosineOmega = np.cos(omega)
    orderangle = (np.pi / orderindex) * (index + 0.5)
    alpha = sineOmega * np.sin(orderangle)

    if norm:
        a0 = 1 + alpha
        A0 = 1
    else:
        a0 = 1
        A0 = 1 + alpha

    A1 = -(2 * cosineOmega) / a0
    A2 = (1 - alpha) / a0
    B1 = (1 - cosineOmega) / a0
    B0 = B1 / 2
    B2 = B0
    b_lp = np.array([B0, B1, B2])
    a_lp = np.array([A0, A1, A2])

    A1 = -(2 * cosineOmega) / a0
    A2 = (1 - alpha) / a0
    B1 = -(1 + cosineOmega) / a0
    B0 = -B1 / 2
    B2 = B0
    b_hp = np.array([B0, B1, B2])
    a_hp = np.array([A0, A1, A2])

    return [b_lp, a_lp], [b_hp, a_hp]

def Butterworth6dB(fc, sr, norm=True):
    '''
    1st Order Butterworth
    :param fc:
    :param sr:
    :param norm:
    :return:
    '''
    omega = 2 * pi * fc / sr
    sineOmega = np.sin(omega)
    cosineOmega = np.cos(omega)

    if norm:
        a0 = 1 + sineOmega + cosineOmega
        A0 = 1
    else:
        a0 = 1
        A0 = 1 + sineOmega + cosineOmega

    A1 = (sineOmega - cosineOmega - 1) / a0
    B0 = (sineOmega) / a0
    B1 = (sineOmega) / a0
    b_lp = np.array([B0, B1])
    a_lp = np.array([A0, A1])

    A1 = (sineOmega - cosineOmega - 1) / a0
    B0 = (1 + cosineOmega) / a0
    B1 = -(1 + cosineOmega) / a0
    b_hp = np.array([B0, B1])
    a_hp = np.array([A0, A1])

    return [b_lp, a_lp], [b_hp, a_hp]

def Butterworth12dB(fc, sr, norm=True):
    '''
    2nd Order Butterworth
    :param fc:
    :param sr:
    :return:
    '''
    omega = 2 * pi * fc / sr

    sineOmega = np.sin(omega)
    cosinePmega = np.cos(omega)
    alpha = sineOmega * np.sqrt(2) / 2

    if norm:
        a0 = 1 + alpha
        A0 = 1
    else:
        a0 = 1
        A0 = 1 + alpha

    A1 = -(2 * cosinePmega) / a0
    A2 = (1 - alpha) / a0
    B1 = (1 - cosinePmega) / a0
    B0 = B1 / 2
    B2 = B0
    b_lp = np.array([B0, B1, B2])
    a_lp = np.array([A0, A1, A2])

    A1 = -(2 * cosinePmega) / a0
    A2 = (1 - alpha) / a0
    B1 = -(1 + cosinePmega) / a0
    B0 = -B1 / 2
    B2 = B0
    b_hp = np.array([B0, B1, B2])
    a_hp = np.array([A0, A1, A2])

    return [b_lp, a_lp], [b_hp, a_hp]

def Butterworth18dB(fc, sr, norm=True):
    '''
    3rd Order Butterworth
    :param fc:
    :param sr:
    :return:
    '''
    f1, f1_ = _higherorder(fc, sr, 0, 3, norm)
    f2, f2_ = Butterworth6dB(fc, sr, norm)

    b_lp = np.convolve(f1[0], f2[0])
    a_lp = np.convolve(f1[1], f2[1])

    b_hp = np.convolve(f1_[0], f2_[0])
    a_hp = np.convolve(f1_[1], f2_[1])

    return [b_lp, a_lp], [b_hp, a_hp]

def Butterworth24dB(fc, sr, norm=True):
    '''
    4th Order Butterworth
    :param fc:
    :param sr:
    :return:
    '''
    f1, f1_ = _higherorder(fc, sr, 0, 4, norm)
    f2, f2_ = _higherorder(fc, sr, 1, 4, norm)

    b_lp = np.convolve(f1[0], f2[0])
    a_lp = np.convolve(f1[1], f2[1])

    b_hp = np.convolve(f1_[0], f2_[0])
    a_hp = np.convolve(f1_[1], f2_[1])

    return [b_lp, a_lp], [b_hp, a_hp]


def Butterworth30dB(fc, sr, norm=True):
    '''
    5th Order Butterworth
    :param fc:
    :param sr:
    :return:
    '''
    # First and second sections of the 5th order filter
    f1, f1_ = _higherorder(fc, sr, 0, 5, norm)
    f2, f2_ = _higherorder(fc, sr, 1, 5, norm)
    f3, f3_ = Butterworth6dB(fc, sr)

    # Convolve the first two sections
    b_lp_temp = np.convolve(f1[0], f2[0])
    a_lp_temp = np.convolve(f1[1], f2[1])

    b_hp_temp = np.convolve(f1_[0], f2_[0])
    a_hp_temp = np.convolve(f1_[1], f2_[1])

    # Then convolve with the third section to get the final coefficients
    b_lp = np.convolve(b_lp_temp, f3[0])
    a_lp = np.convolve(a_lp_temp, f3[1])

    b_hp = np.convolve(b_hp_temp, f3_[0])
    a_hp = np.convolve(a_hp_temp, f3_[1])

    return [b_lp, a_lp], [b_hp, a_hp]


def LinkwitzRiley12dB(fc, sr, norm=True):
    f1, f1_ = Butterworth6dB(fc, sr, norm)
    f2, f2_ = Butterworth6dB(fc, sr, norm)

    b_lp = np.convolve(f1[0], f2[0])
    a_lp = np.convolve(f1[1], f2[1])

    b_hp = np.convolve(f1_[0], f2_[0])
    a_hp = np.convolve(f1_[1], f2_[1])

    # two transfer function need to substract to achieve all-pass filter
    return [b_lp, a_lp], [-b_hp, a_hp]

def LinkwitzRiley24dB(fc, sr, norm=True):
    f1, f1_ = Butterworth12dB(fc, sr, norm)
    f2, f2_ = Butterworth12dB(fc, sr, norm)

    b_lp = np.convolve(f1[0], f2[0])
    a_lp = np.convolve(f1[1], f2[1])

    b_hp = np.convolve(f1_[0], f2_[0])
    a_hp = np.convolve(f1_[1], f2_[1])

    return [b_lp, a_lp], [b_hp, a_hp]

def LinkwitzRiley36dB(fc, sr, norm=True):
    f1, f1_ = Butterworth18dB(fc, sr, norm)
    f2, f2_ = Butterworth18dB(fc, sr, norm)

    b_lp = np.convolve(f1[0], f2[0])
    a_lp = np.convolve(f1[1], f2[1])

    b_hp = np.convolve(f1_[0], f2_[0])
    a_hp = np.convolve(f1_[1], f2_[1])

    return [b_lp, a_lp], [-b_hp, a_hp]

def LinkwitzRiley48dB(fc, sr, norm=True):
    f1, f1_ = Butterworth24dB(fc, sr, norm)
    f2, f2_ = Butterworth24dB(fc, sr, norm)

    b_lp = np.convolve(f1[0], f2[0])
    a_lp = np.convolve(f1[1], f2[1])

    b_hp = np.convolve(f1_[0], f2_[0])
    a_hp = np.convolve(f1_[1], f2_[1])

    return [b_lp, a_lp], [b_hp, a_hp]

def Bessel12dB(fc, sr, norm=True):
    '''
    2nd Order Bessel
    :param fc:
    :param sr:
    :param norm:
    :return:
    '''
    omega = 2 * pi * fc / sr
    sineOmega = np.sin(omega)
    cosineOmega = np.cos(omega)
    alpha = sineOmega / (2 * np.sqrt(1/3))
    if norm:
        a0 = 1 + alpha
        A0 = 1
    else:
        a0 = 1
        A0 = 1 + alpha

    A1 = -2 * cosineOmega / a0
    A2 = (1 - alpha) / a0
    B1 = (1 - cosineOmega) / a0
    B0 = B1 / 2
    B2 = B0
    b_lp = np.array([B0, B1, B2])
    a_lp = np.array([A0, A1, A2])


    A1 = -2 * cosineOmega / a0
    A2 = (1 - alpha) / a0
    B1 = -(1 + cosineOmega) / a0
    B0 = -B1 / 2
    B2 = B0
    b_hp = np.array([B0, B1, B2])
    a_hp = np.array([A0, A1, A2])

    return [b_lp, a_lp], [b_hp, a_hp]

def Bessel18dB(fc, sr, norm=True):
    f1, f1_ = Bessel12dB(fc, sr, norm)
    f2, f2_ = Butterworth6dB(fc, sr, norm)

    b_lp = np.convolve(f1[0], f2[0])
    a_lp = np.convolve(f1[1], f2[1])

    b_hp = np.convolve(f1_[0], f2_[0])
    a_hp = np.convolve(f1_[1], f2_[1])

    return [b_lp, a_lp], [b_hp, a_hp]

def Bessel24dB(fc, sr, norm=True):
    f1, f1_ = Bessel12dB(fc, sr, norm)
    f2, f2_ = Bessel12dB(fc, sr, norm)

    b_lp = np.convolve(f1[0], f2[0])
    a_lp = np.convolve(f1[1], f2[1])

    b_hp = np.convolve(f1_[0], f2_[0])
    a_hp = np.convolve(f1_[1], f2_[1])

    return [b_lp, a_lp], [b_hp, a_hp]

if __name__ == "__main__":
    # LP, HP = Butterworth6dB(1200, 48000)
    # print(len(LP[0]))
    # LP, HP = Butterworth12dB(1200, 48000)
    # print(len(LP[0]))
    # LP, HP = Butterworth18dB(1200, 48000)
    # print(len(LP[0]))
    # LP, HP = Butterworth24dB(1200, 48000)
    # print(len(LP[0]))
    LP, HP = Butterworth30dB(1200, 48000, False)
    print(len(LP[0]))


    # LP, HP = LinkwitzRiley12dB(1200, 48000)
    # print(len(LP[0]))
    # LP, HP = LinkwitzRiley24dB(1200, 48000)
    # print(len(LP[0]))
    # LP, HP = LinkwitzRiley36dB(1200, 48000)
    # print(len(LP[0]))
    # LP, HP = LinkwitzRiley48dB(1200, 48000)
    # print(len(LP[0]))


    w, h = signal.freqz(LP[0] - HP[0], LP[1])
    amplitude = abs(h)
    angle = np.unwrap(np.angle(h))

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    plt.title('frequency response of RIR')
    plt.xlabel(r'normalized frequency (x$\pi$rad/sample)')

    ax1.plot(w / max(w), amplitude, 'g')
    ax1.set_ylabel('amplitude (dB)', color='g')
    ax1.set_ylim(0, 2)
    ax1.grid()

    ax2.plot(w / max(w), angle, 'b--')
    ax2.set_ylabel('phase (radians)', color='b')

    plt.xscale("log")
    plt.show()