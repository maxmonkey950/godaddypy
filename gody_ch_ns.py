from godaddypy import Client, Account
import time
api_key = 'xxx'
api_secret = 'xxx'
my_acct = Account(api_key, api_secret)
delegate_acct = Account(api_key, api_secret, delegate='DELEGATE_ID')
client = Client(my_acct)
delegate_client = Client(delegate_acct)

def adddns(asd):
    try:
        t = client.get_domain_info(asd)
    except:
        print ("%s can't find, Maybe it doesn't belong to you!" % asd)
    else:
        p = ['ns23.domaincontrol.com', 'ns24.domaincontrol.com']
        if t.get('nameServers') != p:
            client.update_domain(asd, nameServers = ['ns23.domaincontrol.com', 'ns24.domaincontrol.com'])
            print("%s default dns has changed" % asd)
        else:
            print("%s status is ok!" % asd)

if __name__ == '__main__':
    for line in open("code"):
        line = line.strip('\n')
        adddns(line)
#        print ("%s passed, next!" % line)
#        time.sleep(3)
