from PyQt5.QtWidgets import *
from UI.Component.uiFriendBar import *
from PyQt5.QtCore import pyqtSignal
from Assist.GlobalVariable import GlobalVariable


# 朋友列表的朋友
class FriendBar(QWidget, Ui_FriendBar):

    click_signal = pyqtSignal(str)  # 选中信号

    def __init__(self, current_id, parent=None):
        super(FriendBar, self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.ClosestRecord.setStyleSheet("color: rgb(200, 120, 120);")
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.mousePressEvent = self.__click_event
        self.enterEvent = self.__mouse_into
        self.leaveEvent = self.__mouse_out
        self.__CurrentId = current_id

    # 设置对方的备注名
    def set_remark_name(self, name):
        self.FriendName.setText(name)

    # 设置最近的消息
    def set_closest_msg(self, msg):
        self.ClosestRecord.setText(msg)

    # 设置所属朋友的id号
    def set_friend_id(self, friend_id):
        self.__FriendId = friend_id

    # 鼠标点击事件
    def __click_event(self, event):
        QWidget.mousePressEvent(self, event)
        if GlobalVariable.CurrentFriendId == self.__FriendId:
            return
        self.set_chatting()
        self.click_signal.emit(self.__FriendId)

    # 鼠标进入事件
    def __mouse_into(self, event):
        QWidget.enterEvent(self, event)
        if GlobalVariable.CurrentFriendId == self.__FriendId:
            return
        self.set_selected()

    # 鼠标离开事件
    def __mouse_out(self, event):
        QWidget.leaveEvent(self, event)
        if GlobalVariable.CurrentFriendId == self.__FriendId:
            return
        self.set_not_selected()

    # 设置未选中状态
    def set_not_selected(self):
        self.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.ClosestRecord.setStyleSheet("color: rgb(200, 120, 120);")

    # 设置选中状态
    def set_selected(self):
        self.setStyleSheet("background-color: rgb(150, 150, 150);")
        self.ClosestRecord.setStyleSheet("color: rgb(250, 200, 200);")

    # 设置聊天状态
    def set_chatting(self):
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ClosestRecord.setStyleSheet("color: rgb(180, 180, 180);")

