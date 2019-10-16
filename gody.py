#!/usr/bin/env python
from godaddypy import Client, Account
import time
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

def adddns(asd):
    print("update %s!" % asd)
    try:
        t = client.get_domain_info(asd)
    except:
        print("%s domain has ERR" % asd)
    else:
        p = ['IVY.NS.CLOUDFLARE.COM', 'JAY.NS.CLOUDFLARE.COM']
        if t.get('nameServers') == p:
            client.update_domain(asd, nameServers = ['ns23.domaincontrol.com', 'ns24.domaincontrol.com'])
            print("%s ns has changed, plase wait to effective." % asd)
            time.sleep(3)
            j = 0
            while True:
                v = client.get_domain_info(asd)
                if v.get('nameServers') == p:
                    time.sleep(3)
                    j += 3
                    print('wait... %s s' % j)
                else:
                    print("%s default ns has changed!" % asd)
                    break
        try:
            client.delete_records(asd, name='www', record_type='CNAME')
#           time.sleep(3)
        except:
            i = 0
            while True:
                k = client.get_records(asd, record_type='CNAME', name='www')
                if k:
                    time.sleep(3)
                    i += 3
                    print('wait... %s s' % i)
                else:
                    break
            print("%s has deleted www record! by except!" % asd)
        else:
            print("%s has deleted www record! by step1!" % asd)
        try:
            client.add_record(asd, {'data':'shops.myshopify.com','name':'www','ttl':600, 'type':'CNAME'})
#               time.sleep(3)
        except:
            print("%s www changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'23.227.38.32','name':'letter','ttl':600, 'type':'A'})
#               time.sleep(3)
        except:
            print("%s letter changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'23.227.38.32','name':'@','ttl':600, 'type':'A'})
#               time.sleep(3)
        except:
            print("%s self type A changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'mailstore1.secureserver.net','name':'@','ttl':600, 'type':'MX'})
#               time.sleep(3)
        except:
            print("%s self type MX changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'smtp.secureserver.net','name':'@','ttl':600, 'type':'MX'})
#               time.sleep(3)
        except:
            print("%s self type MX changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'v=spf1 include:spf.mandrillapp.com ?all','name':'@','ttl':600, 'type':'TXT'})
#               time.sleep(5)
        except:
            print("%s self type TXT changed has ERR" % asd)
        else:
            pass
        try:
            client.add_record(asd, {'data':'v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrLHiExVd55zd/IQ/J/mRwSRMAocV/hMB3jXwaHH36d9NaVynQFYV8NaWi69c1veUtRzGt7yAioXqLj7Z4TeEUoOLgrKsn8YnckGs9i3B3tVFB+Ch/4mPhXWiNfNdynHWBcPcbJ8kjEQ2U8y78dHZj1YeRXXVvWob2OaKynO8/lQIDAQAB;','name':'mandrill._domainkey','ttl':600, 'type':'TXT'})
        except:
            print("%s mandrill type TXT changed has ERR" % asd)
        else:
            pass

if __name__ == '__main__':
    for line in open("code"):
        line = line.strip('\n')
        adddns(line)
        print ("%s has changed, Next one!" % line)
