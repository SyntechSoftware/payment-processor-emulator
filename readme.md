virtualenv env
source env/bin/activate
pip install -r ./requirement.txt -t ./lib/
./manage.py migrate
./manage.py collectstatic
./manage.py createsuperuser

Please note!! sqlite-db was rewrited during each deploy.
If you need to safe data beetwen them - please setup GAE-mysqldb instance