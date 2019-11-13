#!/usr/bin/env python
#coding=utf-8
from godaddypy import Client, Account
import time, logging, psycopg2
conn=psycopg2.connect(database="cmdb",user="postgres",password="7758521",host="47.244.219.176",port="5432")
cur=conn.cursor()
cur.execute("TRUNCATE TABLE public.dns")
logging.basicConfig(filename="ckdomains.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
##company
api_key = 'dLDQ3np5twWq_63xCRCmEDBLUjSiKuQAYmQ'
api_secret = 'DifHeMdaUAQ2gsZnEBGLKP'
##personal
#api_key = 'e4XjnMnKPF5b_KrovPZUUhZb15fxNqH37UP'
#api_secret = 'SKQue82erEzshQwD9dwZ2P'
my_acct = Account(api_key, api_secret)
delegate_acct = Account(api_key, api_secret, delegate='DELEGATE_ID')
client = Client(my_acct)
delegate_client = Client(delegate_acct)
p = ['IVY.NS.CLOUDFLARE.COM', 'JAY.NS.CLOUDFLARE.COM']
p1 = ['ivy.ns.cloudflare.com', 'jay.ns.cloudflare.com']
def ck_domains(asd):
	try:
		location = "Pending"
		desc = 'Pening'
		t = client.get_domain_info(asd)
		if t.get('nameServers') == p or t.get('nameServers') == p1:
#			print("%s has join cf" % asd)
			desc = 'Cloud_Station'
			location = 'cloudflare'
#cur.execute("INSERT INTO site.info(Code,Description,Status,jump)VALUES(%s,%s,%s,%s)",(asd,'CloudFare','A','none'))
		else:
			y = client.get_records(asd, record_type='CNAME')
			if y[0]['data'] == 'shops.myshopify.com':
				desc = 'shopify'
				location = 'godaddy'
#				print ("%s is a location website!" % asd)
			else:
				desc = 'Err'
#				print ("%s is not a shopify website" % asd)
		return  desc, location
	except Exception as e:
		location = 'Pening'
		desc = 'Pening'
		return  desc, location
		print(e)
		logging.exception("%s is err domain" % asd)
if __name__ == '__main__':
    for line in open("ck_domains.lst"):
        line = line.strip('\n')
        ak = ck_domains(line)
        print(line, ak[0], ak[1])
#        cur.execute("INSERT INTO public.siteinfo(Code,Description,Status,jump)VALUES(%s,%s,%s,%s)",(line,ak,'A','none'))
        cur.execute("INSERT INTO public.dns VALUES (5067421, 'dns', 'None', 'None', 'A', 'admin', '2019-10-30 13:38:57.464686', NULL, 'None', %s, %s, %s)",(ak[1],ak[0],line))
        conn.commit()
    cur.close()
    conn.close()
