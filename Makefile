DJS = "DJANGO_SETTINGS_MODULE=settings.dev"

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  bash            starts bash inside a running container."
	@echo "  mysql-client    start mysql client"
	@echo "  celery          start a celery worker"
	@echo "  django          start django (port: 8000)"
	@echo "  dptp            start django shell with ptpython extension"
	@echo "  qr              run 'fab qr' command"
	@echo "  hlt             run 'fab hlt', command"

bash:
	docker exec -it horsebook_hbweb_1 /bin/bash

mysql-client:
	docker exec -it code_hbmysql_1 mysql -h 127.0.0.1 -p=abcd

celery:
	docker exec -it horsebook_hbweb_1 /bin/sh -c "cd /srv/ && $(DJS) C_FORCE_ROOT=1 /usr/local/bin/celery worker -A celeryd -E -l INFO --autoreload"

django:
	docker exec -it horsebook_hbweb_1 /bin/sh -c "cd /srv/ && $(DJS) python manage.py runserver 0.0.0.0:8080"

ptp:
	docker exec -it horsebook_hbweb_1 /bin/sh -c "$(DJS) python /srv/support/manage.py ptp"

qr:
	docker exec -it horsebook_hbweb_1 /bin/sh -c "cd /srv && fab qr"

hlt:
	docker exec -it horsebook_hbweb_1 /bin/sh -c "cd /srv && fab hlt"
