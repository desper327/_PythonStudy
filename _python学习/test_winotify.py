import sys,os
sys.path.append(r'D:\TD_Depot\Python\Lib\3.11\.venv\Lib\site-packages')
import winotify

def dismiss_action():
    os.startfile(r"G:/TBZZXKX/Shot")

noti=winotify.Notifier()
notification = noti.create_notification(
    title="Action Required",
    msg="Would you like to open the website?",
    duration=10,
    icon=r"D:\ZYfile\BaiduSyncdisk\MyStudy\_python学习\python.ico",
    launch=dismiss_action,
)


notification.show()
