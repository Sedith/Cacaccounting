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
    ### Init
    def __init__(self,v):
        if v >= 0:
            self.units = int(math.floor(v))
            self.cents = int(round(v - math.floor(v),2)*100)
        else:
            self.units = int(math.ceil(v))
            self.cents = int( math.floor( (-v + math.ceil(v))*100 ) )

    ### Properties
    @property
    def amount(self):
        return self.amount
    @amount.setter
    def amount(self,v):
        self.amount = v

    ### Conversion
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

    ### Operations
    def __add__(self,other):
        return Money(self.to_float()+other.to_float())

    def __sub__(self,other):
        return Money(self.to_float()-other.to_float())

################################################################################
### Colocaca classes ###
class ColocacaMember:
    ### Init
	def __init__(self, m, a):
		self.mail = m
		self.balance = Money(a)

class ColocacaSession:
    ### Init
    def __init__(self):
        self.members = {}

    ### Properties
    def names(self):
        return self.members().key()

    ### Check
    def check_pseudo_in(self, pseudo):
        pseudo = pseudo.lower()
        if pseudo not in self.members:
            print pseudo+' is not a colocaca member.'
            return False
        else:
            return True

    def check_pseudo_out(self, pseudo):
        pseudo = pseudo.lower()
        if pseudo in self.members:
            print pseudo+' is already a colocaca member.'
            return False
        else:
            return True

    ### Actions
    def add_member(self, pseudo, mail, amount = 0.0):
        pseudo = pseudo.lower()
        mail = mail.lower()
        if self.check_pseudo_out(pseudo):
            self.members[pseudo] = ColocacaMember(mail,amount)

    def del_member(self, pseudo):
        pseudo = pseudo.lower()
        if self.check_pseudo_in(pseudo):
            self.members.pop(pseudo)

    ### To string
    def __str__(self):
        ret = ''
        for pseudo in self.members.keys():
            ret += pseudo+" : "+str(self.members[pseudo].balance)+'  ('+self.members[pseudo].mail+')\n'
        return ret

class Colocaca:
    ### Init
    def __init__(self):
        self.filename = 'colocaca.pickle'
        self.sessions = [ColocacaSession()]
        if exists(self.filename):
            self.load_balance()
        else:
            self.reset_balance()

    ### Access last session
    def get_last_session(self):
        return self.sessions[-1]

    def backup(self):
        if len(self.sessions) == 1:
            print 'no previous balance'
        else:
            self.sessions = self.sessions[:-1]

    ### Access savefile
    def save_balance(self):
        with open(self.filename, 'wb') as savefile:
            pickler = pickle.Pickler(savefile)
            pickler.dump(self.sessions)

    def reset_balance(self):
        last_session = deepcopy(self.get_last_session())
        for member in last_session.members.keys():
            last_session.members[member].balance = Money(0)
        self.sessions = [last_session]
        self.save_balance()

    def load_balance(self):
        with open(self.filename, 'rb') as savefile:
            unpickler = pickle.Unpickler(savefile)
            try:
                self.sessions = unpickler.load()
            except EOFError:
                self.reset_balance()

    ### Operation
    def add_operation(self, payer, debtors, amount):
        new_session = deepcopy(self.get_last_session())
        payer = payer.lower()
        debtors = [debtor.lower() for debtor in debtors]
        for pseudo in [payer]+debtors:
            if not new_session.check_pseudo_in(pseudo):
                return None
        share = float("{0:.2f}".format(float(amount)/(len(debtors))))
        payers_share = float(amount) - share*(len(debtors)-1)
        first_is_baized = False
        if payer in debtors:
            new_session.members[payer].balance += Money(amount - payers_share)
            debtors.remove(payer)
        else:
            new_session.members[payer].balance += Money(amount)
            first_is_baized = True
        for i, debtor in enumerate(debtors):
            if first_is_baized and i == 0:
                new_session.members[debtor].balance -= Money(payers_share)
            else:
                new_session.members[debtor].balance -= Money(share)
        self.sessions += [new_session]

################################################################################
### Main ###
def term_api(colocaca):
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
        colocaca.add_operation(args.payer,args.debtors,args.amount)
    elif args.action == 'add':
        colocaca.get_last_session().add_member(args.pseudo, args.mail, args.amount)
    elif args.action == 'del':
        colocaca.get_last_session().del_member(args.pseudo)
    elif args.action == 'backup':
        colocaca.backup()
    elif args.action == 'display':
        print colocaca.get_last_session()
    elif args.action == 'display_all':
        for i,session in enumerate(colocaca.sessions,1):
            print 'Session '+str(i)
            print session
    elif args.action == 'reset':
        colocaca.reset_balance()


def main():
    ### Load
    colocaca = Colocaca()
    colocaca.load_balance()

    term_api(colocaca)

    session = colocaca.get_last_session()
    #print colocaca.get_last_session()

    ### Save
    colocaca.save_balance()

################################################################################
################################################################################
if __name__ == '__main__':
    main()
