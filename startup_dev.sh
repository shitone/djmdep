nohup python manage.py runserver 0.0.0.0:8000 --settings=config.settings.dev &
nohup python manage.py awspqc2client --settings=config.settings.dev &
nohup python manage.py awspqc2db --settings=config.settings.dev &
nohup python manage.py regcenter2client --settings=config.settings.dev &
nohup python manage.py regcenter2db --settings=config.settings.dev &
