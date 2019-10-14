#!/usr/bin/env python
from godaddypy import Client, Account
import time
api_key = 'xxx'
api_secret = 'xxx'
my_acct = Account(api_key, api_secret)
delegate_acct = Account(api_key, api_secret, delegate='DELEGATE_ID')
client = Client(my_acct)
delegate_client = Client(delegate_acct)

def adddns(asd):
    #t = client.get_domain_info(asd)
    #p = ['ns23.domaincontrol.com', 'ns24.domaincontrol.com']
    #if t.get('nameServers') != p:
    #    client.update_domain(asd, nameServers = ['ns23.domaincontrol.com', 'ns24.domaincontrol.com'])
    #    time.sleep(20)
    try:
        client.delete_records(asd, name='www', record_type='CNAME')
        time.sleep(3)
    except:
        client.add_record(asd, {'data':'shops.myshopify.com','name':'www','ttl':600, 'type':'CNAME'})
        time.sleep(3)
        client.add_record(asd, {'data':'23.227.38.32','name':'letter','ttl':600, 'type':'A'})
        time.sleep(3)
        client.add_record(asd, {'data':'23.227.38.32','name':'@','ttl':600, 'type':'A'})
        time.sleep(3)
        client.add_record(asd, {'data':'mailstore1.secureserver.net','name':'@','ttl':600, 'type':'MX'})
        time.sleep(3)
        client.add_record(asd, {'data':'smtp.secureserver.net','name':'@','ttl':600, 'type':'MX'})
        time.sleep(3)
        client.add_record(asd, {'data':'v=spf1 include:spf.mandrillapp.com ?all','name':'@','ttl':600, 'type':'TXT'})
        time.sleep(5)
        client.add_record(asd, {'data':'v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrLHiExVd55zd/IQ/J/mRwSRMAocV/hMB3jXwaHH36d9NaVynQFYV8NaWi69c1veUtRzGt7yAioXqLj7Z4TeEUoOLgrKsn8YnckGs9i3B3tVFB+Ch/4mPhXWiNfNdynHWBcPcbJ8kjEQ2U8y78dHZj1YeRXXVvWob2OaKynO8/lQIDAQAB;','name':'mandrill._domainkey','ttl':600, 'type':'TXT'})
    else:
        client.add_record(asd, {'data':'shops.myshopify.com','name':'www','ttl':600, 'type':'CNAME'})
        time.sleep(3)
        client.add_record(asd, {'data':'23.227.38.32','name':'letter','ttl':600, 'type':'A'})
        time.sleep(3)
        client.add_record(asd, {'data':'23.227.38.32','name':'@','ttl':600, 'type':'A'})
        time.sleep(3)
        client.add_record(asd, {'data':'mailstore1.secureserver.net','name':'@','ttl':600, 'type':'MX'})
        time.sleep(3)
        client.add_record(asd, {'data':'smtp.secureserver.net','name':'@','ttl':600, 'type':'MX'})
        time.sleep(3)
        client.add_record(asd, {'data':'v=spf1 include:spf.mandrillapp.com ?all','name':'@','ttl':600, 'type':'TXT'})
        time.sleep(5)
        client.add_record(asd, {'data':'v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrLHiExVd55zd/IQ/J/mRwSRMAocV/hMB3jXwaHH36d9NaVynQFYV8NaWi69c1veUtRzGt7yAioXqLj7Z4TeEUoOLgrKsn8YnckGs9i3B3tVFB+Ch/4mPhXWiNfNdynHWBcPcbJ8kjEQ2U8y78dHZj1YeRXXVvWob2OaKynO8/lQIDAQAB;','name':'mandrill._domainkey','ttl':600, 'type':'TXT'})

if __name__ == '__main__':
    for line in open("code"):
        line = line.strip('\n')
        adddns(line)
        print ("%s has changed!" % line)
        time.sleep(10)
