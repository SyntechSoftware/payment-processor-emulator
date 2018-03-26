# payment-processor-emulator
Easy emulation platform for one non-friendly payment system. Python27+Django+GAE. It is good for testing and debugging you billing against non-production payment gateway.

# Installation

virtualenv env source env/bin/activate pip install -r ./requirement.txt -t ./lib/ ./manage.py migrate ./manage.py collectstatic ./manage.py createsuperuser

# Notice

Please note!! sqlite-db was rewrited during each deploy. If you need to safe data beetwen them - please setup GAE-mysqldb instance
