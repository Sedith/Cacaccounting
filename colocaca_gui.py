#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

from appJar import gui
from colocaca import *


app = None
colocaca = None

def clearAll():
    global app
    app.setLabel("colocaca", colocaca.get_last_session())
    app.setLabelHeights("colocaca",len(colocaca.get_last_session().names())+2)
    app.changeOptionBox("del", colocaca.get_last_session().names())
    app.changeOptionBox("Payer", colocaca.get_last_session().names())
    app.changeOptionBox("Debtors", colocaca.get_last_session().names())
    app.hideAllSubWindows()
    app.clearAllCheckBoxes()
    app.clearAllEntries()

def new_mem_handler(button):
    global app, colocaca
    pseudo = app.getEntry("Pseudo")
    mail = app.getEntry("Mail")
    amount = app.getEntry("Base amount")
    if amount == None:
        amount = 0.
    else:
        amount = float(amount)
    colocaca.get_last_session().add_member(pseudo, mail, amount)
    colocaca.save_balance()
    clearAll()

def del_mem_handler(button):
    global app, colocaca
    pseudo = app.getOptionBox("del")
    colocaca.get_last_session().del_member(pseudo)
    colocaca.save_balance()
    clearAll()

def op_handler(button):
    global app, colocaca
    payer = app.getOptionBox("Payer")
    debtors = app.getOptionBox("Debtors")
    true_debtors = []
    for debtor in debtors.keys():
        if debtors[debtor]:
            true_debtors += [debtor]
    amount = float(app.getEntry("Amount"))
    colocaca.add_operation(payer,true_debtors,amount)
    colocaca.save_balance()
    clearAll()

def event_handler(button):
    global app, colocaca

    if button == "Exit":
        app.stop()
    elif button == "Add":
        app.showSubWindow("New operation")
    elif button == "New member":
        app.showSubWindow("New member")
    elif button == "Remove member":
        app.showSubWindow("Remove member")
    elif button == "Backup":
        colocaca.backup()
        colocaca.save_balance()
        clearAll()

def colocaca_gui():
    global app, colocaca
    app = gui()
    ### Sets
    app.setFont(16)

    ### Main layout
    app.addLabel("title_main", "Les cacalescomptes de la colocaca :")
    app.addLabel("colocaca", colocaca.get_last_session())
    app.setLabelHeights("colocaca",len(colocaca.get_last_session().names())+2)
    app.addButtons(["Add", "Backup"], event_handler)
    app.addButtons(["New member","Remove member"], event_handler)
    app.addButtons(["Exit"], event_handler)
    app.setAllButtonWidths(20)

    ### New member layout
    app.startSubWindow("New member", modal=True)
    app.addLabel("title_new", "Add a new member")
    app.addLabelEntry("Pseudo")
    app.addLabelEntry("Mail")
    app.addLabelNumericEntry("Base amount")
    app.setEntryDefault("Base amount", 0)
    app.setEntryAlign("Base amount", "left")
    app.addButtons(["ok_new", "cancel_new"], [new_mem_handler, clearAll])
    app.setButton("ok_new", "Ok")
    app.setButton("cancel_new", "Cancel")
    app.setAllEntryWidths(30)
    app.setAllLabelWidths(15)
    app.setLabelWidths("title_new",25)
    app.stopSubWindow()

    ### Del layout
    app.startSubWindow("Remove member", modal=True)
    app.addLabel("title_del", "Remove a member")
    app.addOptionBox("del", colocaca.get_last_session().names())
    app.addButtons(["ok_del", "cancel_del"], [del_mem_handler, clearAll])
    app.setButton("ok_del", "Ok")
    app.setButton("cancel_del", "Cancel")
    app.stopSubWindow()

    ### Op layout
    app.startSubWindow("New operation", modal=True)
    app.addLabel("title_op", "Add a new operation")
    app.addLabelOptionBox("Payer", colocaca.get_last_session().names())
    app.setLabelWidths("Payer",10)
    app.addTickOptionBox("Debtors", colocaca.get_last_session().names())
    app.addLabelNumericEntry("Amount")
    app.setLabelWidths("Amount",10)
    app.addButtons(["ok_op", "cancel_op"], [op_handler, clearAll])
    app.setButton("ok_op", "Ok")
    app.setButton("cancel_op", "Cancel")
    app.stopSubWindow()

    app.go()


def main():
    global colocaca
    colocaca = Colocaca()

    colocaca_gui()


################################################################################
################################################################################
if __name__ == '__main__':
    main()
