#!/usr/bin/env python
## auther honux, update the dns records of godaddy, you must keep the redis running and config.ini exist. 
from godaddypy import Client, Account
import time, logging, redis
from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('config.ini')
config = dict(cfg.items('update_records_godaddy'))
pool = redis.ConnectionPool(host='127.0.0.1',port=6379,decode_responses=True)
r = redis.Redis(connection_pool=pool)
logging.basicConfig(filename="godaddy.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG)
api_key = config['vu_key']
api_secret = config['vu_secret']
my_acct = Account(api_key, api_secret)
delegate_acct = Account(api_key, api_secret, delegate='DELEGATE_ID')
client = Client(my_acct)
delegate_client = Client(delegate_acct)

def adddns(asd):
    logging.info("update %s!" % asd)
    try:
        t = client.get_domain_info(asd)
    except Exception as e:
        r.lpush("godaddy_err", asd)
        logging.exception("%s domain has ERR" % asd)
    else:
        p = ['IVY.NS.CLOUDFLARE.COM', 'JAY.NS.CLOUDFLARE.COM']
        if t.get('nameServers') == p:
            client.update_domain(asd, nameServers = ['ns23.domaincontrol.com', 'ns24.domaincontrol.com'])
            logging.error("%s ns has changed, plase wait to effective." % asd)
            time.sleep(3)
            j = 0
            while True:
                v = client.get_domain_info(asd)
                if v.get('nameServers') == p:
                    time.sleep(3)
                    j += 3
                    logging.info('wait... %s s' % j)
                else:
                    logging.info("%s default ns has changed!" % asd)
                    break
        try:
            client.delete_records(asd, name='www', record_type='CNAME')
        except Exception as e:
            i = 0
            while True:
                k = client.get_records(asd, record_type='CNAME', name='www')
                if k:
                    time.sleep(3)
                    i += 3
                    logging.info('waiting... %s s' % i)
                else:
                    break
            logging.info("%s has deleted www record! by except!" % asd)
        else:
            logging.info("%s has deleted www record! by step1!" % asd)
        try:
            client.add_record(asd, {'data':'23.227.38.32','name':'letter','ttl':600, 'type':'A'})
        except Exception as e:
            logging.error("%s letter changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'23.227.38.32','name':'@','ttl':600, 'type':'A'})
        except Exception as e:
            logging.error("%s self type A changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'mailstore1.secureserver.net','name':'@','ttl':600, 'type':'MX'})
        except Exception as e:
            logging.error("%s self type MX changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'smtp.secureserver.net','name':'@','ttl':600, 'type':'MX'})
        except Exception as e:
            logging.error("%s self type MX changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'v=spf1 include:spf.mandrillapp.com ?all','name':'@','ttl':600, 'type':'TXT'})
        except Exception as e:
            logging.error("%s self type TXT changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'shops.myshopify.com','name':'www','ttl':600, 'type':'CNAME'})
        except Exception as e:
            logging.error("%s www changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrLHiExVd55zd/IQ/J/mRwSRMAocV/hMB3jXwaHH36d9NaVynQFYV8NaWi69c1veUtRzGt7yAioXqLj7Z4TeEUoOLgrKsn8YnckGs9i3B3tVFB+Ch/4mPhXWiNfNdynHWBcPcbJ8kjEQ2U8y78dHZj1YeRXXVvWob2OaKynO8/lQIDAQAB;','name':'mandrill._domainkey','ttl':600, 'type':'TXT'})
        except Exception as e:
            logging.error("%s mandrill type TXT changed has ERR" % asd)
            try:
                client.add_record(asd, {'data':'v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrLHiExVd55zd/IQ/J/mRwSRMAocV/hMB3jXwaHH36d9NaVynQFYV8NaWi69c1veUtRzGt7yAioXqLj7Z4TeEUoOLgrKsn8YnckGs9i3B3tVFB+Ch/4mPhXWiNfNdynHWBcPcbJ8kjEQ2U8y78dHZj1YeRXXVvWob2OaKynO8/lQIDAQAB;','name':'mandrill._domainkey','ttl':600, 'type':'TXT'})
            except Exception as e:
                logging.error('Exception occurred')
                r.lpush("godaddy_err", asd)
            else:
                r.lpush("godaddy_ok", asd)
        else:
            r.lpush("godaddy_ok", asd)

if __name__ == '__main__':
    t = 0
    print("running......")
    while True:
        t += 1
        k = (r.brpop("godaddy"))
        print("running...,the %s %s " % (t, k[1]))
        adddns(k[1])
