test:
	@python manage.py test

testdb:
	mysql -u root -e 'create database playdoh_app;'

install:
	@pip install -r requirements/compiled.txt --use-mirrors
	@test -f webpagemaker/settings/local.py || \
		cp webpagemaker/settings/local.py-dist webpagemaker/settings/local.py
	@python manage.py syncdb --noinput

destroy:
	mysql -u root -e 'drop database playdoh_app;'

travis: testdb install test

.PHONY: test travis destroy install preinstall