# -*- coding: utf-8 -*-
import datetime
import unicodedata
import zenhan
from escpos import *

class Receipt(object):
	def __init__(self, printer, width=35, tab=25):
		printer.jpInit()
		self.price = 0
		self.tax = 0.08
		self.printer = printer
		self.__setTab(width, tab)


	def header(self, img=None, store=None, clerk=None, date=None):
		self.printer.setAlign('center')
		if img is not None:
			self.printer.image(img)
			self.printer.text('\n')
		if store is not None:
			self.printer.jpText(store + "店\n")
		self.printer.jpText("ご利用ありがとうございます。\n\n")
		if clerk is not None:
			self.printer.jpText("担当 " + clerk + "\n")
		if date is not None:
			self.printer.jpText(date)
		else:
			week = ['月', '火', '水', '木', '金', '土', '日']
			now = datetime.datetime.now()
			txt = now.strftime('%Y年%-m月%-d日（')
			txt += week[now.weekday()]
			txt += now.strftime('） %-H:%M')
			self.printer.jpText(txt)
		self.printer.text("\n\n")
		self.printer.jpText("領 収 証\n\n", dw=True)
		self.printer.setAlign('left')


	def item(self, name, price, pcs=1):
		# Suffix
		suffix = ""
		if pcs > 1:
			suffix = "×" + pcs
		area = self.area - Receipt.strWidth(suffix)

		# Name
		i = 0
		name = name.encode('shift-jis', 'ignore').decode('shift-jis')
		while True:
			width = Receipt.strWidth(name)
			if (width <= area):
				break
			i -= 1
			name = name[0:i]
		name += suffix

		# Price
		self.price += price
		price_str = self.__priceText(price)

		# Print
		self.printer.jpText(name + "\t" + price_str + "\n")


	def footer(self, cash=None):
		self.__setTab(self.area + self.free, 15)
		self.printer.jpText("\n小　　計\t" + self.__priceText(self.price) + "\n")
		self.printer.jpText("内消費税\t" + self.__priceText(round(self.price * self.tax)) + "\n")
		self.printer.jpText("合計", dw=True)
		self.printer.jpText("\t" + self.__priceText(self.price, zen=True) + "\n\n")

		if cash is None:
			cash = self.price
		change = cash - self.price
		self.printer.jpText("お預り\t" + self.__priceText(cash, zen=True) + "\n")
		self.printer.jpText("お釣り\t" + self.__priceText(change, zen=True) + "\n\n")

		#self.printer.jpText("レジNo.1\n\n")
		self.printer.barcode('8583795648480','EAN13',64,2,'','')
		self.printer.cut()


	def __setTab(self, width, tab):
		self.area = tab
		self.free = width - tab
		self.printer.setTab(tab)


	def __priceText(self, val, zen=False):
		string = "{:,d}".format(val)
		if zen:
			string = zenhan.h2z(string)
		space = self.free - (Receipt.strWidth(string) + 2)
		return (" " * space) + "￥" + string


	@staticmethod
	def strWidth(ustr):
		# http://ymotongpoo.hatenablog.com/entry/20120511/1336706463
		width = 0
		for c in ustr:
			cw = unicodedata.east_asian_width(c)
			if cw in u"WFA":
				width += 2
			else:
				width += 1
		return width


if __name__ == '__main__':
	epson = printer.Network('192.168.1.13', port=9100)

	receipt = Receipt(epson)
	receipt.header(img='rabbithouse.png', clerk='香風智乃', date='114年5月14日（月） 19:19')
	receipt.item('ﾎｯﾄｺｰﾋｰｺﾛﾝﾋﾞｱ', 300)
	receipt.item('ﾎｯﾄｺｰﾋｰﾌﾞﾙｰﾏｳﾝﾃﾝ', 300)
	receipt.item('ﾎｯﾄｺｰﾋｰｵﾘｼﾞﾅﾙ', 300)
	receipt.footer(1000)


