# python 
# Created by Tuan Anh Phan on 23.07.2023

from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QGridLayout,
    QVBoxLayout,
    QCompleter,
    QLineEdit,
    QLabel,
    QComboBox,
    QDialog,
    QMainWindow,
    QToolBar,
    QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from sys import exit as sys_exit
from sys import argv as sys_argv
from os import path as os_path
from os import getcwd as os_getcwd

from button_config import LineEdit, PushButton, TextEdit, ComboBox

from excel_process import (encrypt_excel,
                           decrypt_excel,
                           check_passwd,
                           get_data_from_excel,
                           write_data_to_excel,
                           encrypt_and_write,
                           read_and_decrypt_data,
                           is_encrypted,
                           is_decrypted)
from Alert import Alert

MAX_COUNT_HISTORY = 10

bg_color = "qlineargradient(spread:pad, x1:0, y1:0, x2:0.930852, y2:0.903409, stop:0 rgba(145, 232, 211, 255), stop:1 rgba(105, 160, 226, 255))"
set_bg_color = "background-color:" + bg_color + ";"
style_sheet_transparent = "border-radius:20px;" + "background-color: rgba(0, 0, 0, 0);" + "font-weight: bold;"
style_sheet_color = "border-radius:20px;" + "background-color: rgb(170, 255, 255);"


class main_windows(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setObjectName("main_windows")
        self.setStyleSheet("QMainWindow#main_windows{" + set_bg_color + "}")
        self.setWindowTitle("Từ điển chuyên ngành")
        self.Alert = Alert()
        ct_widget = central_widget()
        self.src_path = ct_widget.src_path
        self.data_file_path = ct_widget.data_file_path
        self.passwd = ct_widget.passwd

        self.setCentralWidget(ct_widget)
        self.toolbar_config()

    def toolbar_config(self):
        """
        Nhập mật khẩu để được phép chỉnh sửa từ điển, sau khi nhập mật khẩu đúng,
        file excel sẽ được giải mã và tự động mở ra, sau khi chỉnh sửa và lưu, file sẽ đóng lại
        kết thúc quá trình chỉnh sửa
        C2:
        Tạo Qdialog, sử dụng form_layout để lưu trữ data trong file excel, yêu cầu nhập
        mật khẩu để được phép chỉnh sửa, sau đó đổ data vào form_layout
        cho phép thêm từ mới vào.
        """
        tool_bar = QToolBar("Main toolbar")
        tool_bar.setStyleSheet(style_sheet_transparent)
        self.addToolBar(tool_bar)

        # pb_add_word = PushButton("Thêm thuật ngữ")
        # # pb_add_word.setStyleSheet("border-radius:20px;")
        # pb_add_word.setMinimumSize(300, 50)
        # pb_add_word.clicked.connect(self.rt_pb_add_words)
        # tool_bar.addWidget(pb_add_word)

        pb_edit_dict = PushButton("Chỉnh sửa từ điển")
        # pb_edit.setStyleSheet("border-radius:20px;")
        pb_edit_dict.setMinimumSize(300, 50)
        pb_edit_dict.clicked.connect(self.rt_pb_edit_dict)
        tool_bar.addWidget(pb_edit_dict)

    # def rt_pb_add_words(self):
    #     dialog = QDialog()
    #     layout = QFormLayout()
    #     dialog.setLayout(layout)
    #     dialog.setMinimumSize(400, 400)
    #     dialog.setObjectName("diag")
    #     dialog.setStyleSheet("QDialog#diag {" + set_bg_color + "};")
    #
    #     lb_words = QLabel("Thuật ngữ")
    #     lb_words.setStyleSheet(style_sheet_transparent)
    #     lb_words.setFont(QFont("Times New Roman", 30))
    #     ledit_words = LineEdit()
    #     ledit_words.setPlaceholderText("Nhập thuật ngữ vào đây")
    #     ledit_words.setMinimumSize(400, 50)
    #     layout.addRow(lb_words, ledit_words)
    #
    #     lb_meaning = QLabel("Ý nghĩa")
    #     lb_meaning.setStyleSheet(style_sheet_transparent)
    #     lb_meaning.setFont(QFont("Times New Roman", 30))
    #     tedit_meaning = TextEdit()
    #     tedit_meaning.setMinimumSize(400, 50)
    #     tedit_meaning.setPlaceholderText("Nhập ý nghĩa thuật ngữ vào đây")
    #     layout.addRow(lb_meaning, tedit_meaning)
    #
    #     pb_submit = PushButton("Lưu")
    #     pb_submit.setMinimumSize(200, 50)
    #     pb_cancel = PushButton("Hủy")
    #     pb_cancel.setMinimumSize(200, 50)
    #
    #     pb_cancel.clicked.connect(dialog.close)
    #
    #     layout.addRow(pb_submit, pb_cancel)
    #
    #     retval = dialog.exec_()

    def rt_pb_edit_dict(self):
        dialog = QDialog()
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        dialog.setMinimumSize(400, 400)
        dialog.setObjectName("diag")
        dialog.setStyleSheet("QDialog#diag {" + set_bg_color + "};")

        self.ld_enter_key = LineEdit("")
        self.ld_enter_key.setPlaceholderText("Nhập chìa khóa ở đây")
        self.ld_enter_key.setEchoMode(QLineEdit.Password)
        self.ld_enter_key.setMinimumSize(400, 50)
        layout.addWidget(self.ld_enter_key)

        pb_decrypt = PushButton("Giải mã")
        pb_decrypt.setMinimumSize(400, 50)
        pb_decrypt.clicked.connect(self.rt_pb_decrypt)
        layout.addWidget(pb_decrypt)


        pb_encrypt = PushButton("Mã hóa")
        pb_encrypt.setMinimumSize(400, 50)
        pb_encrypt.clicked.connect(self.rt_pb_encrypt)
        layout.addWidget(pb_encrypt)


        pb_cancel = PushButton("Đóng")
        pb_cancel.setMinimumSize(200, 50)
        pb_cancel.clicked.connect(dialog.close)
        layout.addWidget(pb_cancel)

        retval = dialog.exec_()

    def rt_pb_encrypt(self):
        key_text = self.passwd
        if is_encrypted():
            self.Alert.Raise_Warning("Từ điển đã được mã hóa, vui lòng giải mã trước")
        else:
            encrypt_excel(key_text, self.data_file_path)
            self.Alert.Raise_Information("Mã hóa thành công")

    def rt_pb_decrypt(self):
        key_text = self.ld_enter_key.text()
        if key_text == "":
            self.Alert.Raise_Warning("Chưa nhập chìa khóa")
        elif is_decrypted():
            self.Alert.Raise_Warning("Từ điển chưa được mã hóa, vui lòng mã hóa trước khi giải mã")
        elif not check_passwd(key_text):
            self.Alert.Raise_Warning("Khóa không đúng")
        else:
            decrypt_excel(key_text, self.data_file_path)
            self.Alert.Raise_Information("Giải mã thành công")


class central_widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.main_layout = QGridLayout()
        self.main_layout.setAlignment(Qt.AlignHCenter)
        self.setLayout(self.main_layout)
        self.setMinimumSize(800, 800)
        self.path_config()
        self.passwd = "DinhTrong123@123"  # password to encrypt and decrypt data
        self.process_config_file()
        self.Alert = Alert()
        self.font = QFont(self.get_data_from_config_arr(0), int(self.get_data_from_config_arr(1)))

        # self.data_file_path = os_path.join(self.src_path, self.get_data_from_config_arr(2))
        self.data_file_path = os_path.join(self.src_path, "data_out.xlsx")
        self.history_file_path = os_path.join(self.src_path, self.get_data_from_config_arr(3))
        # self.full_data = self.read_data_from_file(self.data_file_path)
        self.full_data = read_and_decrypt_data(self.passwd, self.data_file_path)

        if self.full_data == "ERROR":
            self.Alert.Raise_Warning("Lỗi trong quá trình giải mã từ điển")
        else:
            self.main_UI()

    def path_config(self):
        self.current_path = os_getcwd()
        self.src_path = os_path.join(self.current_path, "src")

    def process_config_file(self):
        with open(os_path.join(self.src_path, "config.txt")) as f:
            data_config = f.read()
        self.data_config = data_config.split("\n")

    def main_UI(self):
        self.config_line1()
        self.config_line3()
        self.config_line2()
        self.exit_button()

    def config_line1(self):
        label_nhaptu = QLabel("Nhập từ cần tra")
        label_nhaptu.setStyleSheet(style_sheet_transparent)
        label_nhaptu.setFont(self.font)
        self.main_layout.addWidget(label_nhaptu, 0, 0)

        self.find_words = QCompleter(list(self.full_data.keys()))
        self.find_words.setCompletionMode(QCompleter.PopupCompletion)
        self.find_words.setCaseSensitivity(Qt.CaseSensitive)

        self.ledit_find_words = LineEdit()
        self.ledit_find_words.setMinimumSize(600, 50)
        self.ledit_find_words.setCompleter(self.find_words)
        self.ledit_find_words.returnPressed.connect(self.rt_enter)
        self.main_layout.addWidget(self.ledit_find_words, 0, 1)

    def config_line2(self):
        label_history = QLabel("Lịch sử tra từ")
        label_history.setFont(self.font)
        label_history.setStyleSheet(style_sheet_transparent)
        self.main_layout.addWidget(label_history, 1, 0)
        self.cbb_history = ComboBox()
        self.cbb_history.setMaxCount(MAX_COUNT_HISTORY)
        self.cbb_history.setMaxVisibleItems(MAX_COUNT_HISTORY)
        self.cbb_history.setDuplicatesEnabled(False)
        self.cbb_history.setInsertPolicy(QComboBox.InsertAtTop)
        self.cbb_history.setMinimumSize(600, 70)
        # self.cbb_history.setFont(self.font)
        # self.cbb_history.setMinimumSize(500, 40)
        # self.cbb_history.setStyleSheet(style_sheet_color)
        self.cbb_history.activated.connect(self.rt_cbb_pressed)
        self.init_history()

        self.main_layout.addWidget(self.cbb_history, 1, 1)

    def config_line3(self):
        label_meaning = QLabel("Ý nghĩa của từ")
        label_meaning.setFont(self.font)
        label_meaning.setStyleSheet(style_sheet_transparent)
        self.main_layout.addWidget(label_meaning, 2, 0)

        self.te_meaning = TextEdit()
        # self.te_meaning.setStyleSheet(style_sheet_color)
        # self.te_meaning.setFont(self.font)
        # self.te_meaning.setAlignment(Qt.AlignHCenter)
        self.te_meaning.setReadOnly(True)
        self.main_layout.addWidget(self.te_meaning, 2, 1)

    def exit_button(self):
        self.lb_history_count = QLabel("")
        self.lb_history_count.setFont(self.font)
        self.lb_history_count.setStyleSheet(style_sheet_transparent)
        self.main_layout.addWidget(self.lb_history_count, 5, 0)

        self.button_exit = PushButton("Thoát")
        self.button_exit.setMinimumSize(600, 50)
        self.button_exit.clicked.connect(self.rt_exit_button)
        self.main_layout.addWidget(self.button_exit, 5, 1)

    def rt_exit_button(self):
        self.write_history()
        self.write_data()
        # self.button_exit.clicked.connect(QApplication.instance().quit)
        exit(0)

    def rt_enter(self):
        self.te_meaning.setText(self.full_data.get(self.ledit_find_words.text())[0])
        self.process_history_ledit()
        self.add_counter_ledit()
        self.display_counter()

    @staticmethod
    def read_data_from_file(file_name) -> dict:
        dict_output = {}
        with open(file_name, "r", encoding='utf-8') as f:
            data = f.read()
            lst_data = data.split("\n")
            for i in range(len(lst_data) // 3):
                dict_output[(lst_data[3 * i]).lower()] = [lst_data[3 * i + 1], int(lst_data[3 * i + 2])]

        return dict_output


    def get_data_from_config_arr(self, index):
        return self.data_config[index].split("=")[1]

    def init_history(self):
        with open(self.history_file_path, "r") as f:
            data = f.read()
        self.history_data = data.split("\n")
        for index, data in enumerate(self.history_data):
            if data != "":
                self.cbb_history.insertItem(index, data)

    def process_history(self, Obj):
        while len(self.history_data) > 10:
            self.history_data.pop()
        if isinstance(Obj, QLineEdit):
            self.history_data.insert(0, Obj.text())
            self.cbb_history.insertItem(0, Obj.text())
        elif isinstance(Obj, QComboBox):
            self.history_data.insert(0, Obj.currentText())
            self.cbb_history.insertItem(0, Obj.currentText())

        self.cbb_history.setCurrentIndex(0)

    def process_history_ledit(self):
        self.process_history(self.ledit_find_words)

    def process_history_cbbox(self):
        self.process_history(self.cbb_history)

    def add_counter(self, Obj):
        # Cộng thêm 1 lần khi tra từ
        if isinstance(Obj, QLineEdit):
            self.full_data[Obj.text()][1] += 1
        elif isinstance(Obj, QComboBox):
            self.full_data[Obj.currentText()][1] += 1

    def add_counter_ledit(self):
        self.add_counter(self.ledit_find_words)

    def add_counter_cbbox(self):
        self.add_counter(self.cbb_history)

    def write_history(self):
        with open(self.history_file_path, "w") as f:
            for data in self.history_data:
                f.writelines(data + "\n")

    def write_data(self):
        # with open(self.data_file_path, "w") as f:
        #     for key in self.full_data:
        #         f.writelines(key + "\n")
        #         f.writelines(self.full_data.get(key)[0] + "\n")
        #         f.writelines(str(self.full_data.get(key)[1]) + "\n")
        encrypt_and_write(self.data_file_path, self.passwd, self.full_data)

    def display_counter(self):
        self.lb_history_count.setText("Lượt tra từ: %s" % self.full_data[self.ledit_find_words.text()][1])

    def rt_cbb_pressed(self):  # Combobox
        self.te_meaning.setText(self.full_data.get(self.cbb_history.currentText())[0])
        self.process_history_cbbox()
        self.add_counter_cbbox()
        # display counter
        self.lb_history_count.setText("Lượt tra từ: %s" % self.full_data[self.cbb_history.currentText()][1])



if __name__ == '__main__':
    app = QApplication(sys_argv)
    screen = main_windows()
    screen.show()
    sys_exit(app.exec_())
