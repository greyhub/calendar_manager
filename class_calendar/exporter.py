from crawler import Crawler
from database import Database

crawler = Crawler(hide=True)
database = Database(url='mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
# class_schedule = {'_id': 20173261,
#                   'class': crawler.login('mung.vt173261@sis.hust.edu.vn', 'qyi617))!')
#                   }
# database.insert_class_schedule(class_schedule)
print(database.get_class_schedule(20173261))
