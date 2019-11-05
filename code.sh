for i in `cat dm.lst` ; do redis-cli lpush godaddy $i ; sleep 0.5 ; done
