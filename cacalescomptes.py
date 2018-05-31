#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

### Imports
import math

### Money class
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

### Ppl class
class ColocacaMember:

	def __init__(self, p, m):
		self.pseudo = p
		self.mail = m
		self.balance = Money(0)

	@property
	def pseudo(self):
		return self.pseudo
	@pseudo.setter
	def pseudo(self, v):
		self.pseudo = v

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

### Save balance in txtfile
filename = 'colocaca.txt'
def save_balance():
    pass

def load_balance():
    pass

### Member management
def add_member(pseudo, mail):
    pass

def del_member(pseudo):
    pass

### Operations
ppl = {}
def operation(payer, debtors, amount):
    global ppl
    share = float(amount)/(len(debtors)+1)
    print 'Part : '+str(share)
    ppl[payer].balance += Money(amount - share)
    for debtor in debtors:
        ppl[debtor].balance -= Money(share)

### Display
def display():
    global ppl
    for member in ppl.values():
        print member.pseudo+" :"+str(member.balance)

def main():
    print Money(1.6)
    ppl["Cacartin"] = ColocacaMember("Cacartin","moncul@yopmail.com")
    ppl["Cacalex"] = ColocacaMember("Cacalex","soncul@yopmail.com")
    ppl["Cacajim"] = ColocacaMember("Cacajim","songroscul@yopmail.com")

    operation("Cacartin",["Cacalex","Cacajim"],10)
    display()
    operation("Cacalex",["Cacartin","Cacajim"],10)
    display()
    operation("Cacajim",["Cacalex","Cacartin"],10)
    display()


if __name__ == '__main__':
    main()
