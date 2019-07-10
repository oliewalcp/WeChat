from UI.Component.uiMainWindow import *
from UI.FriendsControllInterface import *
from UI.ChatRecordInterface import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal


# 应用程序主窗口
class MainWindow(QMainWindow, Ui_MainWindow):

    exit_proc_signal = pyqtSignal()  # 退出程序信号

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("微信")
        self.ChatRecordInterface = ChatRecordInterface(self)
        self.FriendControllInterface = FriendsControllInterface(self)
        self.RightLayout.addWidget(self.ChatRecordInterface)
        self.LeftLayout.addWidget(self.FriendControllInterface)

        self.FriendControllInterface.new_msg_signal.connect(self.ChatRecordInterface.add_msg)
        self.FriendControllInterface.click_friend_signal.connect(self.ChatRecordInterface.set_current_friend)

    @pyqtSlot(dict)
    def receive_text(self, msg):
        self.FriendControllInterface.set_friend(msg)

    def closeEvent(self, event):
        self.exit_proc_signal.emit()
        event.accept()
