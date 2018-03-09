import itchat

def wxLogin():
    itchat.auto_login(hotReload=True)

def wxPutTxt(txt):
    back = itchat.send_msg(txt)
    #back = itchat.send_msg('测试','@@63633670417308f4873ff8c2e11f64ee872ddcc0269c4f590f020cf732890606')#运维工作群



