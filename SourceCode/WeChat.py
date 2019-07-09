import sys
from PyQt5.QtWidgets import QApplication
from UI.MainWindow import MainWindow
from MessageHandler.ChatMessageReceiver import ChatMessageReceiver
import time

if __name__ == "__main__":
    # 开启图形界面循环
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()

    chat_message_receiver = ChatMessageReceiver()
    # 消息接收器的信号
    chat_message_receiver.receive_text_signal.connect(main.receive_text)
    chat_message_receiver.send_successfully_signal.connect(main.ChatRecordInterface.add_msg)
    chat_message_receiver.start_itchat_signal.connect(main.FriendControllInterface.read_all_friend_with_record)
    chat_message_receiver.set_closest_msg_after_success_signal.connect(main.FriendControllInterface.set_closest_msg)
    # 界面控件的信号
    main.exit_proc_signal.connect(chat_message_receiver.end)
    main.ChatRecordInterface.send_msg_signal.connect(chat_message_receiver.send_msg)

    chat_message_receiver.start()
    status = app.exec_()
    # 界面关闭，等待微信监控程序关闭，等待5秒
    timer = 0.0
    while chat_message_receiver.isRunning():
        time.sleep(0.001)
        timer += 0.001
        if timer >= 5000:
            break

    sys.exit(status)

