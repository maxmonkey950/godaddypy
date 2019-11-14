from godaddypy import Client, Account
from configparser import ConfigParser
import time, logging, psycopg2, requests, sys
cfg = ConfigParser()
cfg.read('config.ini')
config = dict(cfg.items('tuoguan'))
conn = psycopg2.connect(database=config['dbname'], user=config['dbuser'], password=config['dbpass'], host=config['dbhost'], port=config['dbport'])
cur = conn.cursor()

headers = {
    'accept': 'application/json',
    'Authorization': config['ce'],
}

params = [
    ('limit', '1000'),
    ('includes', ['nameServers']),
]

total_datas = {}

def get_domains(marker=""):
    if marker:
        params.append(('marker', marker))
    if requests.get('https://api.godaddy.com/v1/domains', headers=headers, params=params):
        response = requests.get('https://api.godaddy.com/v1/domains', headers=headers, params=params)
        res_list = response.json()
    else:
        print("err")
        raise SystemExits
    for r in res_list:
#        print(r)
        total_datas[r["domain"]] = (
        r["createdAt"], r.get("expires", "0000-00-00T00:00:00.000Z"), r["nameServers"], r["renewAuto"], r["status"])
#        print(total_datas)
    # for v in res_list:
    #     print(v)
    #     print(v["domain"], v["createdAt"], v["expires"], v["nameServers"], v["renewAuto"], v["status"])
    if len(res_list) >= 1000:
        m = res_list[-1]["domain"]
        get_domains(marker=m)

def is_need_update(domain, status):
    if total_datas.get(domain, "")[4] != status:
        return True
    else:
        return False

def update_db():
    global total_datas
    cur.execute("select domains, dnsstatus from public.dns where \"Status\" = 'A'")
    old_data = cur.fetchall()
    need_update_data = []
    for d in old_data:
        try:
            if is_need_update(d[0], d[1]):
                need_update_data.append((total_datas.get(d[0].strip(), [])[4], d[0]))
        except Exception as e:
            print(e)
    print(need_update_data)
    for ts in need_update_data:
        # print(ts)
        try:
            cur.execute("update public.dns set dnsstatus = '%s' where domains = '%s'" % (ts[0], ts[1].strip()))
            conn.commit()
        except Exception as e:
            print(e)

def insert_update():
    conn = psycopg2.connect(database=config['dbname'], user=config['dbuser'], password=config['dbpass'], host=config['dbhost'], port=config['dbport'])
    ###conn = psycopg2.connect(database="cmdb", user="postgres", password="7758521", host="47.244.219.176", port="5432")
    cur = conn.cursor()
	    cur.execute("select domains, dnsstatus from public.dns where \"Status\" = 'A'")
    old_data = cur.fetchall()
    #global total_datas
    need_insert_data = []
    lao={}
    for i in old_data:
        lao[i[0]] = (i[1])
    #print(lao)
    for k,_ in total_datas.items():
     #   print(k)
        if lao.get(k, False):
            print("pass")
            pass
        else:
            need_insert_data.append(k)
            print(k)
    print(need_insert_data)
    for j in need_insert_data:
        try:
            #print(j, total_datas[j][0], total_datas[j][1], total_datas[j][2], total_datas[j][3], total_datas[j][4])
            cur.execute("INSERT INTO public.dns VALUES (5067421, 'dns', 'None', 'None', 'A', 'admin', '2019-10-30 13:38:57.464686', 'NULL', %s,%s,%s,%s,%s,%s)", (j, total_datas[j][0], total_datas[j][1], total_datas[j][2], total_datas[j][3], total_datas[j][4]))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()
            conn = psycopg2.connect(database=config['dbname'], user=config['dbuser'], password=config['dbpass'], host=config['dbhost'], port=config['dbport'])
            ###conn = psycopg2.connect(database="cmdb", user="postgres", password="7758521", host="47.244.219.176", port="5432")
            cur = conn.cursor()

def init_data():
    # TRUNCATE TABLE
    conn = psycopg2.connect(database=config['dbname'], user=config['dbuser'], password=config['dbpass'], host=config['dbhost'], port=config['dbport'])
    ###conn = psycopg2.connect(database="cmdb", user="postgres", password="7758521", host="47.244.219.176", port="5432")
    cur = conn.cursor()
    global total_datas
    for k, v in total_datas.items():
        # print(k, v)
        # print(d['domain'], d['createdAt'], d['renewAuto'], d['status'])
        try:
            cur.execute("INSERT INTO public.dns VALUES (5067421, 'dns', 'None', 'None', 'A', 'admin', '2019-10-30 13:38:57.464686', 'NULL', %s,%s,%s,%s,%s,%s)", (k, v[0], v[1], v[2], v[3], v[4]))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()
            conn = psycopg2.connect(database=config['dbname'], user=config['dbuser'], password=config['dbpass'], host=config['dbhost'], port=config['dbport'])
            ###conn = psycopg2.connect(database="cmdb", user="postgres", password="7758521", host="47.244.219.176", port="5432")
            cur = conn.cursor()

if __name__ == '__main__':
    get_domains()
    if len(sys.argv) == 2 and sys.argv[1] == 'init':
        print("init data")
        init_data()
    elif len(sys.argv) == 2 and sys.argv[1] == 'insert':
        print("insert data")
        insert_update()
    elif len(sys.argv) == 2 and sys.argv[1] == 'update':
        print("update")
        update_db()
    cur.close()
    conn.close()
