from UI.Component.uiFriendsControllInterface import *
from UI.FriendBar import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from MessageHandler.ChatMessageHandler import *
from Assist.Saver import *

# 朋友列表界面
class FriendsControllInterface(QWidget, Ui_FriendsControllInterface):

    new_msg_signal = pyqtSignal(str, str, str, str, int)  # 收到新消息的信号
    click_friend_signal = pyqtSignal(str)  # 选择一个朋友聊天的信号
    """
    私有成员变量：
    __Friend_Bar:朋友id号——朋友消息控件
    __Bar_Friend:朋友消息控件——朋友id号
    __Current_Friend:当前朋友的id号
    """

    def __init__(self, parent=None):
        super(FriendsControllInterface, self).__init__(parent)
        self.setupUi(self)
        self.Message.setText("消息")
        self.FriendCircle.setText("朋友圈")
        self.Friend.setText("联系人")
        self.FriendListLayout.addStretch()

        self.__Friend_Bar = {}
        self.__Bar_Friend = {}

        self.__read_all_friend_with_record()

    # 读取全部有聊天记录的朋友
    def __read_all_friend_with_record(self):
        import os
        all_file = os.listdir(GlobalVariable.FriendDataDirectory)
        for f in all_file:
            temp_f = os.path.join(GlobalVariable.FriendDataDirectory, f)
            if os.path.isfile(temp_f):
                temp_id = f[:-4]
                record = get_record_list(temp_id)
                self.__add_friend_msg_widget(temp_id, get_remarkname_by_id(temp_id), record[len(record) - 1].Content)

    """
    添加朋友消息控件
    param[friend_id]:朋友的id号
    param[remark_name]:朋友的备注
    param[closest_msg]:最近的一条消息
    """
    def __add_friend_msg_widget(self, friend_id, remark_name, closest_msg):
        new_bar = FriendBar(self)
        self.FriendListLayout.insertWidget(0, new_bar)
        self.__Friend_Bar[friend_id] = new_bar
        self.__Bar_Friend[new_bar] = friend_id
        new_bar.set_remark_name(remark_name)
        new_bar.set_closest_msg(closest_msg)
        new_bar.set_friend_id(friend_id)
        new_bar.click_signal.connect(self.__select_friend)
    """
    设置朋友的消息
    param[msg_content]:原生消息json报文
    """
    def set_friend(self, msg):
        msg_handler = ChatMessageHandler(msg)
        friend_id = msg_handler.get_current_user()
        msg_content = msg_handler.get_content()
        friend_remark_name = msg_handler.get_remark_name()
        sender = msg_handler.get_sender()
        now_time = get_now_time()
        save_msg(msg_handler, now_time)
        try:
            new_bar = self.__Friend_Bar[friend_id]
            new_bar.set_closest_msg(msg_content)  # 将新消息设置到消息控件里面
            msg_id = msg_handler.get_msg_id()
            # 如果当前正在与该朋友聊天
            if GlobalVariable.CurrentFriendId == friend_id:
                if sender == friend_id:
                    self.new_msg_signal.emit(msg_id, msg_content, friend_remark_name, now_time, 1)  # 将新的消息插入到聊天界面
                else:
                    self.new_msg_signal.emit(msg_id, msg_content, "我", now_time, 0)  # 将新的消息插入到聊天界面
            self.FriendListLayout.removeWidget(new_bar)
            self.FriendListLayout.insertWidget(0, new_bar)
        except Exception as e:
            self.__add_friend_msg_widget(friend_id, friend_remark_name, msg_content)

    """
    选择朋友事件
    param[friend_id]:朋友的id号
    """
    @pyqtSlot(str)
    def __select_friend(self, friend_id):
        try:
            friend_bar = self.__Friend_Bar[GlobalVariable.CurrentFriendId]
            friend_bar.set_not_selected()
        except Exception as e:
            pass
        GlobalVariable.CurrentFriendId = friend_id
        self.click_friend_signal.emit(friend_id)
