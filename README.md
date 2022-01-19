# calendar_manager

## How To Setup
```
cd calendar_manager
```
```
env\Scripts\activate.bat
```

```
pip install -r requirements.txt
```
### Change the default DATABASE in calendar_manager/setting.py
```python
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'calendar_manager',
    'USER':'root',
    'PASSWORD':'Database password',
    'HOST':'127.0.0.1',
    'PORT':'3306'
    }
}
```

## Run project
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py createsuperuser
```
```
python manage.py runserver
```

