import time
from pprint import pprint

import regex as re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Crawler:
    def __init__(self, hide=True):
        options = Options()
        options.add_argument("--headless")
        if hide:
            self.driver = webdriver.Firefox(executable_path='geckodriver', options=options)
        else:
            self.driver = webdriver.Firefox(executable_path='geckodriver')

    def get_soup(self, url):
        self.driver.get(url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # driver.close()
        return soup

    def get_driver(self, url):
        self.driver.get(url)
        return self.driver

    def get_login_link(self):
        home_page_soup = self.get_soup('https://ctt.hust.edu.vn/')
        login_button_tag = home_page_soup.find('div', {'class': 'logIn'})
        login_link_tag = login_button_tag.find('a', {'id': 'loginLink'})
        login_link = login_link_tag.get_attribute_list('href')
        login_link = login_link[0]
        return login_link

    def login(self, user_name, password):
        login_page = self.get_driver('https://dt-ctt.hust.edu.vn/Students/Timetables.aspx')
        username_text_area = login_page.find_element_by_id('userNameInput')
        username_text_area.send_keys(user_name)
        next_button = login_page.find_element_by_id('nextButton')
        next_button.click()
        password_text_area = login_page.find_element_by_id('passwordInput')
        password_text_area.send_keys(password)
        submit_button = login_page.find_element_by_id('submitButton')
        submit_button.click()
        time.sleep(5)
        html = login_page.page_source
        timetables_page_soup = BeautifulSoup(html, "html.parser")
        table_tag = timetables_page_soup.find('table', {'class': 'dxgvTable_Mulberry'})
        col_names = ['time', 'week', 'class room', 'class code', 'class type', 'group', 'subject code', 'class name',
                     'note', 'teaching prototype', 'teacher', 'link online', 'team code']

        row_tags = table_tag.find_all('tr', 'dxgvDataRow_Mulberry')
        time_table = list()
        for row in row_tags:
            subject = dict()
            col_tag = row.find_all('td')
            count = 0
            for col in col_tag:
                content = 'NULL'
                contents = col.contents
                if contents:
                    content = str(contents[0])
                    if 'href' in content:
                        parser = re.findall(r'"([^"]*)"', content)
                        content = parser[-1]
                    if content == '\xa0':
                        content = 'NULL'
                subject[col_names[count]] = content
                count += 1
            time_table.append(subject)
        # pprint(time_table)

        login_page.close()
        return time_table


# if __name__ == '__main__':
#     crawler = Crawler()
#
#     a = crawler.login('mung.vt173261@sis.hust.edu.vn', 'qyi617))!')
#     pprint(a)
