import os
import sys
import fnmatch

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QWidget, QVBoxLayout, QFileDialog, \
    QMessageBox
from qt_material import apply_stylesheet

from ui import Ui_MainWindow

class RenametoolWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setStyleSheet("""
                            QLabel {
                                font-size: 22px;
                                font-weight: bold;
                            }
                            QPushButton {
                                font-size:20px;
                            }
                            QListWidget{
                                font-size:16px;
                            }
                            QLineEdit{
                                font-size:22px;
                                color: #FFFFFF;
                            }
                            QCheckBox{
                                font-size:22px
                            }
                            QRadioButton{
                                font-size:22px
                            }
                            QComboBox{
                                font-size:20px;
                                color: #FFFFFF
                            }
                        """)

        self.msg_box = QMessageBox()
        self.ChooseVIdeoPath_pushButton.clicked.connect(self.ChooseVideoPath)
        self.ChooseSubtitlePath_pushButton.clicked.connect(self.ChooseSubtitlePath)

        self.StartProcess.clicked.connect(self.Rename)

    # 选择视频路径按钮对应函数
    def ChooseVideoPath(self):
        m = QFileDialog.getExistingDirectory(None, "选取文件夹")
        if m == '':
            return
        self.VideoPath_lineEdit.setText(m)

    # 选择字幕路径按钮对应函数
    def ChooseSubtitlePath(self):
        m = QFileDialog.getExistingDirectory(None, "选取文件夹")
        if m == '':
            return
        self.SubtitlePath_lineEdit.setText(m)
        self.LoadLanguage()

    def LoadLanguage(self):
        folder_path = self.SubtitlePath_lineEdit.text()  # 替换为你的文件夹路径
        file_extensions = (".ass", ".srt", ".ssa")  # 支持的文件扩展名
        SubtitleLanguages = set()  # 用于存储提取的语言
        for filename in os.listdir(folder_path):
            if filename.endswith(file_extensions):
                SubtitleLanguages.add(filename.split(".")[-2]) # 提取倒数第二个点之间的部分作为语言
        self.ChooseLanguage_comboBox.clear()
        if len(SubtitleLanguages) !=0:
            self.ChooseLanguage_comboBox.addItems(list(SubtitleLanguages))
        else:
            self.msg_box.warning(self,"注意！",  "当前目录下没有找到字幕文件！")

    def check(self):
        if self.VideoPath_lineEdit.text() == '':
            self.msg_box.critical(self, '错误！', '没有设置视频路径')
            return False

        if self.SubtitlePath_lineEdit.text() == '':
            self.msg_box.critical(self, '错误！', '没有设置字幕路径')
            return False

        if self.NewName_lineEdit.text() == '':
            self.msg_box.critical(self, '错误！', '没有设置新文件名')
            return False

        return True

    def Rename(self):
        if not self.check():
            return
        file_list = os.listdir(self.SubtitlePath_lineEdit.text())
        first_file_list = []
        print(self.ChooseLanguage_comboBox.currentText())

        # 第一次 按语言筛选
        for _, filename in enumerate(file_list):
            if filename.split(".")[-2] == self.ChooseLanguage_comboBox.currentText():
                first_file_list.append(filename)

        first_file_list.sort()

        # 第二次按文件名筛选
        matching = self.NameMatching_lineEdit_lineEdit.text()
        matching = matching.replace('[','?').replace(']','?')

        second_file_list = []
        for _, filename in enumerate(first_file_list):
            if fnmatch.fnmatch(filename, matching):
                second_file_list.append(filename)
                print(filename)


        for index, filename in enumerate(second_file_list):
            old_path = os.path.join(self.SubtitlePath_lineEdit.text(), filename)
            new_filename = f"{self.NewName_lineEdit.text()}-第{index + 1:02d}集.{self.ChooseLanguage_comboBox.currentText()}.{filename.split('.')[-1]}"
            new_path = os.path.join(self.SubtitlePath_lineEdit.text(), new_filename)
            os.rename(old_path, new_path)


if __name__== "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    window = RenametoolWindow()
    sys.exit(app.exec_())