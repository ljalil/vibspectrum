from PyQt5 import QtCore

class Signal:
    """Signal
    ========
    Class encapsulating single signal to be managed from SignalManager
    """

    def __init__(self, name, data, path, sampling_frequency):
        self.name = name
        self.data = data
        self.path = path
        if sampling_frequency > 0:
            self.sampling_frequency = sampling_frequency
            self.sampling_period = 1/sampling_frequency
        else:
            self.sampling_frequency = 0
            self.sampling_period = 0

    def get_property(self, index):
        if index == 0:
            return self.name
        if index ==1:
            return self.path
        if index ==2:
            return self.sampling_frequency
        if index == 3:
            return self.sampling_period

    @staticmethod
    def get_properties_list():
        return ["Name", "Path", "Frequency", "Period"]

class SignalsManager(QtCore.QAbstractTableModel):
    def __init__(self):
        super(SignalsManager, self).__init__()
        self.signals_list = []

    def data(self, index, role):
        if role==QtCore.Qt.DisplayRole:
            value = self.signals_list[index.row()].get_property(index.column())
            if isinstance(value, float):
                return str(value)

            return value

    def rowCount(self, index):
        return len(self.signals_list)

    def columnCount(self, index):
        return 4

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return Signal.get_properties_list()[section]

    def add_signal(self, name, data, path, sampling_frequency):
        self.layoutAboutToBeChanged.emit()
        new_signal = Signal(name, data, path, sampling_frequency)
        self.signals_list.append(new_signal)
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()

    def removeRows(self, row, count, index=QtCore.QModelIndex()):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row+count)
        if count == 1:
            del self.signals_list[row]
        else:
            del self.signals_list[row: row+count]
        self.endRemoveRows()

    def update_signal_data(self, index, name, sampling_frequency, sampling_period):
        self.signals_list[index].name = name
        self.signals_list[index].sampling_frequency = sampling_frequency
        self.signals_list[index].sampling_period = sampling_period
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        return True
