from godaddypy import Client, Account
import time, logging, psycopg2, requests, sys
conn=psycopg2.connect(database="xxx",user="postgres",password="xxx",host="xxx",port="5432")
cur=conn.cursor()

headers = {
    'accept': 'application/json',
              'Authorization': 'sso-key xxx:xxx',
}

params = [
    ('limit', '1000'),
    ('includes', ['nameServers']),
]

total_datas = {}
def get_domains(marker=""):
    if marker:
        params.append(('marker', marker))
    response = requests.get('https://api.godaddy.com/v1/domains', headers=headers, params=params)
    res_list = response.json()
    for r in res_list:
        print(r)
        total_datas[r["domain"]] = (r["createdAt"], r["expires"], r["nameServers"], r["renewAuto"], r["status"])
    # for v in res_list:
    #     print(v)
    #     print(v["domain"], v["createdAt"], v["expires"], v["nameServers"], v["renewAuto"], v["status"])
    if len(res_list)>=1000:
        m = res_list[-1]["domain"]
        get_domains(marker=m)

def is_need_update(domain, status):
    if total_datas.get(domain, "") != status:
        return True
    else:
        return False

def update_db():
    global total_datas
    cur.execute("select domains, dnsstatus from public.dns")
    old_data = cur.fetchall()
    need_update_data = []
    for d in old_data:
        if is_need_update(d[0], d[1]):
            print(total_datas)
            need_update_data.append((total_datas.get(d[0].strip(), [])[4], d[0]))

    print(need_update_data)
    for ts in need_update_data:
        print(ts)
        cur.execute("update public.dns set dnsstatus = '%s' where domains = '%s'" %(ts[0], ts[1].strip()))
        conn.commit()

def init_data():
    global total_datas
    for k, v in total_datas.items():
        #print(k, v)
        cur.execute("INSERT INTO public.dns VALUES (5067421, 'dns', 'None', 'None', 'A', 'admin', '2019-10-30 13:38:57.464686', 'NULL', %s,%s,%s,%s,%s,%s)",(k, v[0],v[1],v[2],v[3],v[4]))
        conn.commit()
if __name__ == '__main__':
    get_domains()
    if len(sys.argv) == 2 and sys.argv[1] == 'init':
        init_data()
    else:
        print("update")
        update_db()
