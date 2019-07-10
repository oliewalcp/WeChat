import itchat
from itchat.content import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QThread
from Assist.Saver import *


# 消息接收器
class ChatMessageReceiver(QThread):

    receive_text_signal = pyqtSignal(dict)  # 发送文本消息信号
    send_successfully_signal = pyqtSignal(str, str, str, str, int)  # 发送消息成功的信号
    set_closest_msg_after_success_signal = pyqtSignal(str, str, str, str, str, str)  # 发送设置最近消息的信号
    start_itchat_signal = pyqtSignal()  # 开启了微信环境

    # 开始执行
    def run(self):
        ChatMessageReceiver.__CMR = self
        try:
            itchat.auto_login(hotReload=False)  # 登录微信
            print("登录成功")
            print("开始获取联系人列表")
            friends = itchat.get_friends(update=True)  # 获取微信好友列表，如果设置update=True将从服务器获取列表
            print("获取联系人完成")
            start = True
            print("将联系人的信息同步到本地")
            use_time = time.time()
            # 加载联系人列表
            for f in friends:
                # print(f)
                if start:
                    start = False
                    GlobalVariable.LocalID = friends[0]["UserName"]
                else:
                    save_friend_info(f["UserName"], f["NickName"], f["RemarkName"])
            use_time = int(round((time.time() - use_time) * 1000))
            if use_time >= 60000:
                print("同步完成， 耗时" + str(float(use_time) / 60000) + "分钟")
            elif use_time >= 1000:
                print("同步完成， 耗时" + str(float(use_time) / 1000) + "秒")
            elif use_time < 1000:
                print("同步完成， 耗时" + str(use_time) + "毫秒")
            print("开始监听微信消息")
            self.start_itchat_signal.emit()
            itchat.run()  # 进入微信控制台环境
        except Exception as e:
            repr(e)
            try:
                self.end()
            except:
                pass

    # 窗口关闭，退出微信
    @pyqtSlot()
    def end(self):
        itchat.logout()
        print("微信退出成功")

    """
    发送消息
    param[target_id]:对方的id号
    param[content]:消息内容
    """
    @pyqtSlot(str, str)
    def send_msg(self, target_id, content):
        success = itchat.send(content, target_id)
        if success:
            print("\"" + content + "\"" + "发送成功")
            now_time = get_now_time()
            local_id = get_local_id()
            save_chat_msg(target_id, success["MsgID"], content, now_time, "text", local_id, 1)
            self.set_closest_msg_after_success_signal.emit(target_id, success["MsgID"], local_id, content,
                                                           get_remarkname_by_id(target_id), now_time)
            # self.send_successfully_signal.emit(msg_id, content, "我", now_time, 1)
        else:
            print("\"" + content + "\"" + "发送失败")

    # 接收私聊文本信息
    @staticmethod
    @itchat.msg_register(TEXT)
    def __receive_text(msg):
        ChatMessageReceiver.__CMR.receive_text_signal.emit(msg)

    # 接收私聊图片消息
    @staticmethod
    @itchat.msg_register(PICTURE)
    def __receive_picture(pic):
        pass

    # 接收私聊语音消息
    @staticmethod
    @itchat.msg_register(VIDEO)
    def __receive_video(video):
        pass

    # 接收群聊文本信息
    @staticmethod
    @itchat.msg_register(TEXT, isGroupChat=True)
    def __receive_group_text(msg):
        print(msg)
        # ChatMessageReceiver.__CMR.receive_text_signal.emit(msg)

    # 接收群聊图片消息
    @staticmethod
    @itchat.msg_register(PICTURE, isGroupChat=True)
    def __receive_group_picture(pic):
        pass

    # 接收群聊语音消息
    @staticmethod
    @itchat.msg_register(VIDEO, isGroupChat=True)
    def __receive_group_video(video):
        pass

