# python 
# Created by Tuan Anh Phan on 31.05.2023
from PyQt5.QtWidgets import QWidget, QMessageBox

class Alert(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.Alert = QMessageBox()
        # self.setStyleSheet()

    def Raise_Alert(self, Title, Icon, Text):
        self.Alert.setWindowTitle(Title)
        self.Alert.setIcon(Icon)
        self.Alert.setText(Text)
        self.Alert.setStandardButtons(QMessageBox.Ok)
        self.Alert.buttonClicked.connect(self.Alert.close)
        retval = self.Alert.exec_()

    def Raise_Warning(self, Text):
        self.Raise_Alert("Lỗi", QMessageBox.Warning, Text)

    def Raise_Critical(self, Text):
        self.Raise_Alert("Lỗi", QMessageBox.Critical, Text)

    def Raise_Information(self, Text):
        self.Raise_Alert("Lỗi", QMessageBox.Information, Text)


if __name__ == '__main__':
    pass
