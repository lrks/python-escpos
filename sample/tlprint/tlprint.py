# -*- coding: utf-8 -*-
import datetime
import time
import os.path
import requests
import traceback

from twitter import *
from escpos import *

class TLPrint(object):
	def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret, q, ipaddr):
		auth = OAuth(consumer_key=consumer_key, consumer_secret=consumer_secret, token=access_token_key, token_secret=access_token_secret)
		self.twitter = Twitter(auth=auth)
		self.ids = []
		self.q = q
		self.ipaddr = ipaddr
		epson = printer.Network(ipaddr, port=9100)
		epson.jpInit()
		epson.setAlign('center')
		epson.jpText('Twitter\n', dw=True, dh=True)
		epson.jpText('「' + q + '」の検索結果\n\n', dw=True)
		epson.close()


	def print(self):
		tweet = []
		for t in self.twitter.search.tweets(q=self.q, result_type="recent", count=100)['statuses']:
			tid = 0
			if 'retweeted_status' in t:
				tid = t['retweeted_status']['id']
			else:
				tid = t['id']

			if tid in self.ids:
				continue
			if t['text'].startswith('RT'):
				continue
			self.ids.append(tid)
			tweet.append(t)

		if len(tweet) == 0:
			return

		for s in sorted(tweet, key=lambda tw: tw['id']):
			self.__print(s)


	def __print(self, t):
		# Date
		unixtime = time.mktime(time.strptime(t['created_at'],"%a %b %d %H:%M:%S +0000 %Y")) + 32400
		date = datetime.datetime.fromtimestamp(unixtime).strftime('%Y/%m/%d %H:%M:%S')

		# Image
		image = []
		if 'extended_entities' in t:
			for m in t['extended_entities']['media']:
				#print("KOKOKA!")
				image.append(m['media_url'] + ':thumb')
				#print("AAAAAA!")
		elif ('entities' in t and 'media' in t['entities']):
			for m in t['entities']['media']:
				image.append(m['media_url'] + ':thumb')

		# Text
		text = t['text']

		# User
		name = t['user']['name']
		screen_name = t['user']['screen_name']
		icon = t['user']['profile_image_url']

		# Print
		epson = printer.Network(self.ipaddr, port=9100)	# Broken pipe 対策
		epson.jpInit()
		epson.setAlign('center')
		self.__image_print(icon, epson)
		epson.setAlign('left')
		epson.jpText(name + '\n')
		epson.setAlign('right')
		epson.jpText('@' + screen_name + '\n\n')
		epson.setAlign('left')
		epson.jpText(text + '\n')
		epson.setAlign('center')
		for img in image:
			self.__image_print(img, epson)
		epson.setAlign('left')
		epson.jpText(date + '\n\n\n')
		epson.close()

		print("-----------------------------------")
		print(icon, name, screen_name, text, image, date)


	def __image_print(self, url, printer):
		root, ext = os.path.splitext(url)
		if ':' in ext:
			idx = ext.index(':')
			ext = ext[0:idx]
		name = '/tmp/printer' + ext
		raw = requests.get(url).content
		f = open(name, 'wb')
		f.write(raw)
		f.close()
		printer.image(name)


def main(consumer_key, consumer_secret, access_token_key, access_token_secret):
	tlp = TLPrint(consumer_key, consumer_secret, access_token_key, access_token_secret, '釧路高専 OR どぶろっく OR 花香よしあき', '192.168.10.10')

	while True:
		try:
			print("GET......")
			tlp.print()
		except Exception as e:
			print("ERROR!")
			print(traceback.format_exc())
			time.sleep(120)
		finally:
			time.sleep(60)


if __name__ == '__main__':
	main('consumer_key', 'consumer_secret', 'access_token_key', 'access_token_secret')

