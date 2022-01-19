# Time Management System integrated Google Calendar

    @author: Luong Nguyen, Dat Dinh, Mung Vu
    @release: 20/01/2022 (v1)
    @license: MIT license

## Main Components
- [Time Management System](#)
- [Class-Activities System](https://github.com/greyhub/calendar_manager/tree/main/class_calendar)
- [Google Calendar](https://calendar.google.com)

## Setup

- Install Conda:
[phoenixNAP](https://phoenixnap.com/kb/how-to-install-anaconda-ubuntu-18-04-or-20-04)
- Create environment
```
conda create -n jobCenter python=3.6
conda activate jobCenter
```

- Install requirements
```
pip install -r requirements.txt
```

- Change the default DATABASE in `calendar_manager/setting.py`
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

## How to Run
```
cd calendar_manager
```

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

## Generate token from Google Calendar

[Google Calendar API in Python| How to Get Started](https://www.youtube.com/watch?v=eRHvfNKcwMQ&t=575s&ab_channel=Cndro)

## References

[Django](https://www.djangoproject.com/)

[Google OR-Tools](https://developers.google.com/optimization)

[Google Cloud Platform - APIs](https://console.cloud.google.com/apis/dashboard?project=abiding-circle-319707)
