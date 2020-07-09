from PyQt5 import QtCore, QtGui, QtWidgets, uic
from vibspectrum.signalmanager import Signal, SignalsManager
from vibspectrum.signalprocessing import WaveletAnalysis, FourierAnalysis
from vibspectrum import utilities

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = uic.loadUi('vibspectrum.ui', self)
        self.signal_manager = SignalsManager()
        self.freq_per_validator = QtGui.QDoubleValidator()

        #Signals TabView
        self.ui.signals_tableView.setModel(self.signal_manager)
        self.ui.signals_tableView.clicked.connect(self.on_signal_viewer_clicked)

        #Signals Loading/Deleting
        self.ui.signal_load_path_pushButton.clicked.connect(self.on_signal_load_clicked)
        self.ui.signal_delete_pushButton.clicked.connect(self.on_delete_signal_button_clicked)
        self.ui.signal_choose_dir_pushButton.clicked.connect(self.on_open_signal_file_clicked)

        #Signals information
        self.ui.signal_general_name_lineEdit.textChanged.connect(self.on_signal_data_changed)

        self.ui.signal_sampling_frequency_lineEdit.setValidator(self.freq_per_validator)
        self.ui.signal_sampling_period_lineEdit.setValidator(self.freq_per_validator)

        self.ui.signal_sampling_frequency_lineEdit.textChanged.connect(self.update_signal_frequency)
        self.ui.signal_sampling_period_lineEdit.textChanged.connect(self.update_signal_period)

        #Plotting
        self.ui.tf_wavelet_plotting_plot_pushButton.clicked.connect(self.trigger_wa_plot)
        self.ui.spectrum_fft_plot_pushButton.clicked.connect(self.trigger_fft_plot)

    #Signals management
    def on_signal_load_clicked(self):
        signal_path = str(self.ui.signal_load_path_lineEdit.text())

        for signal in self.signal_manager.signals_list:
            if signal.path == signal_path:
                self.signal_exists_dialog()
                return

        signal_data = utilities.load_txt_file(signal_path)
        self.signal_manager.add_signal("", signal_data, signal_path, 1)
        self.ui.panner_end_doubleSpinBox.setValue(signal_data.shape[0])

    def on_open_signal_file_clicked(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Load signal",QtCore.QDir.homePath() ,"Data files (*.txt *.csv)")
        self.ui.signal_load_path_lineEdit.setText(file[0])

    def on_signal_viewer_clicked(self, index):
        if not index.isValid():
            return

        self.plot_signal_waveform()

        current_index = index.row()
        selected_signal_name = self.signal_manager.signals_list[current_index].name
        selected_signal_path = self.signal_manager.signals_list[current_index].path
        selected_signal_frequency = self.signal_manager.signals_list[current_index].sampling_frequency
        selected_signal_period = self.signal_manager.signals_list[current_index].sampling_period

        self.ui.signal_general_name_lineEdit.setText(selected_signal_name)
        self.ui.signal_load_path_lineEdit.setText(selected_signal_path)
        self.ui.signal_sampling_frequency_lineEdit.setText(str(selected_signal_frequency))
        self.ui.signal_sampling_period_lineEdit.setText(str(selected_signal_period))

    def on_delete_signal_button_clicked(self):
        current_row = self.ui.signals_tableView.currentIndex().row()
        test = self.signal_manager.removeRow(current_row, self.ui.signals_tableView.currentIndex())


    #Signal information
    def on_signal_data_changed(self):
        if not self.ui.signals_tableView.currentIndex().isValid():
            return
        index = self.ui.signals_tableView.currentIndex().row()
        name = str(self.ui.signal_general_name_lineEdit.text())
        frequency = float(self.ui.signal_sampling_frequency_lineEdit.text())
        period = float(self.ui.signal_sampling_period_lineEdit.text())
        self.signal_manager.update_signal_data(index, name, frequency, period)

    def update_signal_frequency(self, freq):
        #While editing, if all content of this line edit is cleared, clear also the other line edit content
        if not freq:
            self.ui.signal_sampling_period_lineEdit.clear()

        try:
            float(freq)
        except ValueError:
            print('Cannot convert value')
            return

        if float(freq) <= 0:
            return
        if not self.ui.signal_sampling_period_lineEdit.hasFocus():
            self.ui.signal_sampling_period_lineEdit.setText(str(1/float(freq)))
            self.on_signal_data_changed()

    def update_signal_period(self, per):
        #While editing, if all content of this line edit is cleared, clear also the other line edit content
        if not per:
            self.ui.signal_sampling_frequency_lineEdit.clear()

        try:
            float(per)
        except ValueError:
            print('Cannot convert value')
            return

        if float(per) <= 0:
            return

        if not self.ui.signal_sampling_frequency_lineEdit.hasFocus():
            self.ui.signal_sampling_frequency_lineEdit.setText(str(1/float(per)))
            self.on_signal_data_changed()

    #Plotting

    def plot_signal_waveform(self):
        data = self.signal_manager.signals_list[self.ui.signals_tableView.currentIndex().row()].data
        self.ui.waveform_widget.figure.clear()
        axis = self.ui.waveform_widget.figure.add_subplot(111)
        axis.plot(data, lw=.5)
        axis.spines['right'].set_visible(False)
        axis.spines['left'].set_visible(False)
        axis.spines['top'].set_visible(False)
        axis.set_yticks([])
        axis.set_xlim([0, data.shape[0]])
        axis.tick_params(axis='x', labelsize=7)
        self.ui.waveform_widget.figure.tight_layout()
        self.ui.waveform_widget.figure.canvas.draw()

    def trigger_wa_plot(self):
        self.wavelet_analyzer = WaveletAnalysis()
        wavelet = self.wavelet_analyzer.wavelets_list[self.ui.tf_wavelet_settings_wavelet_comboBox.currentIndex()]
        self.wavelet_analyzer.wavelet = wavelet
        self.wavelet_analyzer.scales = int(self.tf_wavelet_settings_scales_spinBox.value())
        self.wavelet_analyzer.palette = str(self.ui.tf_wavelet_plotting_palette_comboBox.currentText())
        current_signal = self.signal_manager.signals_list[self.ui.signals_tableView.currentIndex().row()]
        self.wavelet_analyzer.signal = current_signal
        sampling_frequency = float(self.ui.signal_sampling_frequency_lineEdit.text())
        sampling_period = float(self.ui.signal_sampling_period_lineEdit.text())
        self.wavelet_analyzer.signal.sampling_frequency = sampling_frequency
        self.wavelet_analyzer.signal.sampling_period = sampling_period
        self.wavelet_analyzer.plot_scaleogram(self.ui.plot_widget)

    def trigger_fft_plot(self):
        self.fourier_analyzer = FourierAnalysis()
        current_signal = self.signal_manager.signals_list[self.ui.signals_tableView.currentIndex().row()]
        self.fourier_analyzer.signal = current_signal
        symmetric = self.ui.spectrum_fft_symmetrical_checkBox.isChecked()
        self.fourier_analyzer.plot_fft_spectrogram(self.ui.plot_widget, symmetric=symmetric)

    def signal_exists_dialog(self):
        diag = QtWidgets.QMessageBox()
        diag.setIcon(QtWidgets.QMessageBox.Information)
        diag.setWindowTitle("Signal already loaded")
        diag.setInformativeText("The signal you are attempting to add already exists in loaded signals list")
        diag.setStandardButtons(QtWidgets.QMessageBox.Ok)
        diag.exec_()
