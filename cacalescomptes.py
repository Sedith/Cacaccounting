#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

### Imports
import math
import argparse
import pickle
from copy import deepcopy
from os.path import exists

################################################################################
### Money class ###
class Money:

    def __init__(self,v):
        if v >= 0:
            self.units = int(math.floor(v))
            self.cents = int(round(v - math.floor(v),2)*100)
        else:
            self.units = int(math.ceil(v))
            self.cents = int( math.floor( (-v + math.ceil(v))*100 ) )

    @property
    def amount(self):
        return self.amount
    @amount.setter
    def amount(self,v):
        self.amount = v

    def to_float(self):
        if self.units >= 0:
            return float(self.units) + float(self.cents)/100
        else:
            return float(self.units) - float(self.cents)/100

    def __str__(self):
        if self.cents < 10:
            return str(self.units)+",0"+str(self.cents)
        else:
            return str(self.units)+","+str(self.cents)

    def __add__(self,other):
        return Money(self.to_float()+other.to_float())

    def __sub__(self,other):
        return Money(self.to_float()-other.to_float())

################################################################################
### Ppl class ###
class ColocacaMember:

	#def __init__(self, p, m, a):
	def __init__(self, m, a):
		#self.pseudo = p
		self.mail = m
		self.balance = Money(a)

	#@property
	#def pseudo(self):
	#	return self.pseudo
	#@pseudo.setter
	#def pseudo(self, v):
	#	self.pseudo = v

	@property
	def mail(self):
		return self.mail
	@mail.setter
	def mail(self, v):
		self.mail = v

	@property
	def balance(self):
		return self.balance
	@balance.setter
	def balance(self, v):
		self.balance = v

################################################################################
### Global variables ###
filename = 'colocaca.pickle'
colocaca = [{}]

################################################################################
### Check if name is in or out colocaca ###
def check_pseudo_in(pseudo):
    global colocaca
    pseudo = pseudo.lower()
    if pseudo not in colocaca[-1]:
        print pseudo+' is not a colocaca member.'
        return False
    else:
        return True

def check_pseudo_out(pseudo):
    global colocaca
    pseudo = pseudo.lower()
    if pseudo in colocaca[-1]:
        print pseudo+' is already a colocaca member.'
        return False
    else:
        return True

################################################################################
### Save balance in txtfile ###
def save_balance():
    global colocaca, filename
    with open(filename, 'wb') as savefile:
        pickler = pickle.Pickler(savefile)
        pickler.dump(colocaca)

def reset_balance():
    global colocaca
    colocaca = [{}]
    save_balance()

def load_balance():
    global colocaca, filename
    with open(filename, 'rb') as savefile:
        unpickler = pickle.Unpickler(savefile)
        try:
            colocaca = unpickler.load()
        except EOFError:
            reset_balance()

################################################################################
### Actions ###
def add_member(pseudo, mail, amount):
    global colocaca
    pseudo = pseudo.lower()
    mail = mail.lower()
    if check_pseudo_out(pseudo):
        colocaca[-1][pseudo] = ColocacaMember(mail,amount)

def del_member(pseudo):
    global colocaca
    pseudo = pseudo.lower()
    if check_pseudo_in(pseudo):
        colocaca[-1].pop(pseudo)

def add_operation(payer, debtors, amount):
    global colocaca
    payer = payer.lower()
    debtors = [debtor.lower() for debtor in debtors]
    for pseudo in [payer]+debtors:
        if not check_pseudo_in(pseudo):
            return
    colocaca = colocaca+deepcopy([colocaca[-1]])
    share = float("{0:.2f}".format(float(amount)/(len(debtors))))
    payers_share = float(amount) - share*(len(debtors)-1)
    first_is_baized = False
    if payer in debtors:
        colocaca[-1][payer].balance += Money(amount - payers_share)
        debtors.remove(payer)
    else:
        colocaca[-1][payer].balance += Money(amount)
        first_is_baized = True
    for i, debtor in enumerate(debtors):
        if first_is_baized and i == 0:
            colocaca[-1][debtor].balance -= Money(payers_share)
        else:
            colocaca[-1][debtor].balance -= Money(share)

def backup():
    global colocaca
    if len(colocaca) == 1:
        print 'no previous balance'
    else:
        colocaca = colocaca[:-1]

def display():
    global colocaca
    for pseudo in colocaca[-1].keys():
        print pseudo+" : "+str(colocaca[-1][pseudo].balance)+'  ('+colocaca[-1][pseudo].mail+')'

def display_all():
    global colocaca
    for i,caca in enumerate(colocaca):
        print '----------\nBalance '+str(i)+' :'
        for pseudo in caca.keys():
            print pseudo+" : "+str(caca[pseudo].balance)+'  ('+caca[pseudo].mail+')'

################################################################################
### Main ###
def main():
    ### Fetch previous balance
    global filename
    if exists('./'+filename):
        load_balance()
    else:
        reset_balance()

    ### Parse Args
    parser = argparse.ArgumentParser(description='Cacalescomptes.')
    subparsers = parser.add_subparsers(dest='action', help='Action.')
    subparsers.required = True

    operation_parser = subparsers.add_parser('pay')
    operation_parser.add_argument('payer', help='Name of the payer.')
    operation_parser.add_argument('amount', help='Amount of the operation.', type=float)
    operation_parser.add_argument('debtors', nargs='*', help='List of the debtors.')

    add_member_parser = subparsers.add_parser('add')
    add_member_parser.add_argument('pseudo', help='Name of the new member.')
    add_member_parser.add_argument('mail', help='Mail of the new member.')
    add_member_parser.add_argument('amount', nargs='?', default=0, help='Initial credit.', type=float)

    del_member_parser = subparsers.add_parser('del')
    del_member_parser.add_argument('pseudo', help='Name of the member to delete.')

    subparsers.add_parser('backup')
    subparsers.add_parser('display')
    subparsers.add_parser('display_all')
    subparsers.add_parser('reset')

    args = parser.parse_args()

    ### Execute command
    if args.action == 'pay':
        add_operation(args.payer,args.debtors,args.amount)
        display()
    elif args.action == 'add':
        add_member(args.pseudo, args.mail, args.amount)
        display()
    elif args.action == 'del':
        del_member(args.pseudo)
        display()
    elif args.action == 'backup':
        backup()
        display()
    elif args.action == 'display':
        display()
    elif args.action == 'display_all':
        display_all()
    elif args.action == 'reset':
        reset_balance()

    ### Save
    save_balance()

################################################################################
################################################################################
if __name__ == '__main__':
    main()
