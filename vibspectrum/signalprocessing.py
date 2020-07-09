import numpy as np
import matplotlib.pyplot as plt
import pywt

class FourierAnalysis:
    """Docstring for FourierAnalysis. """

    def __init__(self):
        self.signal = None

    def fft(self, symmetric=False):
        sampled_points = self.signal.data.shape[0]
        fft_x = np.linspace(0, self.signal.sampling_frequency, sampled_points)
        fft_y = np.fft.fft(self.signal.data)
        fft_y = np.abs(fft_y)

        if symmetric:
            return fft_x, fft_y

        return (fft_x[:sampled_points//2], fft_y[:sampled_points//2])

    def plot_fft_spectrogram(self, widget, symmetric=False):
        fft_x, fft_y = self.fft(symmetric=symmetric)
        widget.figure.clear()
        axis = widget.figure.add_subplot(111)
        axis.plot(fft_x, fft_y)
        axis.grid(ls=':')
        axis.set_xlabel('Frequency (Hz)')
        axis.set_ylabel('Amplitude')
        widget.figure.tight_layout()
        widget.figure.canvas.draw()

class MultiresolutionAnalysis:
    """MultiresolutionAnalysis
    =============

    """
    def __init__(self, decomposition_level ):
        self.wavelet = None
        self.decomposition_level = None

class WaveletAnalysis:

    def __init__(self):
        self.wavelet = None
        self.scales = None
        self.signal = None
        self.palette = "viridis"
        self.wavelets_list = ['morl', 'mexh', 'shan','fbsp','gaus1', 'gaus2', 'gaus3', 'gaus4', 'gaus5', 'gaus6', 'gaus7', 'gaus8']
    def wavelet_transform(self):
        pass

    def plot_scaleogram(self, widget):
        time = np.linspace(0,self.signal.data.shape[0]*self.signal.sampling_period, self.signal.data.shape[0])
        scales = np.arange(1, self.scales+1)
        [coef, freq] = pywt.cwt(self.signal.data, scales, self.wavelet, self.signal.sampling_period)
        coef = abs(coef)
        widget.figure.clear()
        axis = widget.figure.add_subplot(111)
        cntr_plt = axis.contourf(time, freq, coef, levels=40, cmap=self.palette)
#        widget.figure.colorbar().remove()
        widget.figure.colorbar(cntr_plt, ax=axis)

        axis.set_xlabel('Time (s)')
        axis.set_ylabel('Frequency (Hz)')

        widget.figure.tight_layout()
        widget.figure.canvas.draw()
