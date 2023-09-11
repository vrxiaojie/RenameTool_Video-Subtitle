from qt_material import apply_stylesheet
import sys
if __name__== "__main__":
    app = QtWidgets.QApplication(sys.argv)         # 创建一个QApplication，即将开发的软件app
    MainWindow = QtWidgets.QMainWindow()    #QMainWindow装载需要的组件
    apply_stylesheet(app, theme='dark_teal.xml')
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)     #执行类中的setupUi方法
    MainWindow.show()
    sys.exit(app.exec_())