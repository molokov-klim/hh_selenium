from selenium import webdriver
from selenium.common import exceptions, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pickle


class MyChromeWebdriver:
    def __init__(self):
        pass

    # options
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("user-data-dir=/home/hash/Projects/Python/hh_selenium/browser/session-data")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no--sandbox")
    options.headless = True

    service = Service("/home/hash/Projects/Python/hh_selenium/browser/chromedriver")

    def if_login(self):
        """
        check login status from hh.ru
        return True or False
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.options
        )
        # wait = WebDriverWait(driver, 5)
        try:
            print("[SYS] hh.ru check login status...")
            driver.get("https://hh.ru/applicant/settings?from=header_new&hhtmFromLabel=header_new&hhtmFrom=main")
            if driver.find_element("xpath", "//div[@data-template-name='fio']"):
                time.sleep(5)
                return True
            else:
                time.sleep(5)
                return False
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def get_hh_cookies(self):
        """
        get cookies from hh.ru by input login and code
        save in file: ./{login}_cookies
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.options
        )
        print("[SYS] Delete cookies")
        driver.delete_all_cookies()
        try:
            print("[SYS] Инициализирована авторизация на сайте hh.ru...")
            hh_login = input("[SYS] Введите логин hh.ru (почта или номер телефона): ")
            hh_login_url = 'https://hh.ru/account/login?backurl=%2F&hhtmFrom=main'
            driver.get(hh_login_url)
            print("Passing authentication hh.ru... login")
            login_input = driver.find_element("name", "login")
            login_input.clear()
            login_input.send_keys(hh_login)
            print("click...")
            login_input.submit()

            hh_code = input("hh.ru отправил код, введите его: ")
            code_input = driver.find_element("name", "otp-code-input")
            code_input.clear()
            code_input.send_keys(hh_code)
            print("click...")
            code_input.submit()

            print("dump cookies...")
            pickle.dump(driver.get_cookies(), open(f"{hh_login}_cookies", "wb"))

            time.sleep(5)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def who_am_i(self):
        """
        print authorized username from hh.ru
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.options
        )
        try:
            driver.get("https://hh.ru/applicant/settings?from=header_new&hhtmFromLabel=header_new&hhtmFrom=main")
            print("[SYS] hh.ru logged by: ", driver.find_element("xpath", "//div[@data-template-name='fio']").text)
            time.sleep(5)

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def get_list_cv(self):
        """
        print cv's from hh.ru
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.options
        )
        try:
            driver.get("https://hh.ru/applicant/resumes?hhtmFromLabel=header&hhtmFrom=main")
            cv = driver.find_elements("xpath", "//div[@data-qa='resume']")
            list_cv = []
            for i in cv:
                list_cv.append(i.get_attribute("data-qa-title"))
            time.sleep(5)
            return list_cv

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def get_recommendations_from_cv(self, cv_title):
        """Get recommendation link from cv

        Returns:
          Link
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.options
        )
        try:
            link = ""
            driver.get("https://hh.ru/applicant/resumes?hhtmFromLabel=header&hhtmFrom=main")
            cv = driver.find_element("xpath", f"//div[@data-qa-title='{cv_title}']")

#            buttons_block = cv.find_elements("xpath", "//div[@class='applicant-resumes-recommendations-buttons']")
#            for y in buttons_block:
#                print(y)
#                link = y.find_element("tag name", "a").get_attribute("href")
            buttons = cv.find_elements("xpath", "//div[@class='applicant-resumes-recommendations-button']")
            for y in buttons:
                temp_link = y.find_element("tag name", "a").get_attribute("href")
                if (temp_link.__contains__("/search/")):
                    link = temp_link

            
            time.sleep(5)
            return link

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def get_vacancy_links(self, link, qty):
        """
        Description
        """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.options
        )
        try:
            vacancy_links = []
            driver.get(link)
            page_qty = int(driver.find_elements("xpath", "//a[@data-qa='pager-page']")[-1].text)
            # resp_buttons = driver.find_elements("xpath", "//a[@data-qa='vacancy-serp__vacancy_response']")

            for page in range(page_qty):
                print("Страница ", page)
                link = link + f"&page={page}"
                driver.get(link)
                resp_buttons = driver.find_elements("xpath", "//a[@data-qa='vacancy-serp__vacancy_response']")
                for y in resp_buttons:
                    print("Ссылок собрано: ", len(vacancy_links))
                    if len(vacancy_links) >= qty:
                        return vacancy_links
                    vacancy_links.append(y.get_attribute("href"))
            return vacancy_links
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def apply_for_a_job(self, vacancy_links, letter):
        # """Make apply for a jobs
        # Params:
        #   link: Link for resume recommendations
        #   letter: Transmittal letter
        #   qty: Quantity of replies
        # """
        driver = webdriver.Chrome(
            service=self.service,
            options=self.options
        )
        try:
            for vacancy_link in vacancy_links:
                print(vacancy_links.index(vacancy_link), " of ", len(vacancy_links))
                print("vacancy_link: ", vacancy_link)
                driver.get(vacancy_link)
                time.sleep(5)
                try:
                    driver.find_element("xpath", "//button[@data-qa='vacancy-response-letter-toggle']").click()
                    letter_input = driver.find_element("xpath", "//textarea[@placeholder='Напишите, почему именно ваша кандидатура должна заинтересовать работодателя']")
                    letter_input.clear()
                    letter_input.send_keys(letter)
                    letter_input.send_keys(Keys.ENTER)
                    letter_input.submit()
                    print("submit letter")
                except NoSuchElementException:
                    #ЗДЕСЬ НУЖНО ПОДБИРАТЬ ССЫЛКУ И ПОТОМ ОТПРАВИТЬ ИХ В ТЕЛЕГРАМ
                    print("pass")
                    continue

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()


if __name__ == "__main__":
    my_driver = MyChromeWebdriver()

    if not my_driver.if_login():
        my_driver.get_hh_cookies()
    else:
        my_driver.who_am_i()
    try:
        list_cv = my_driver.get_list_cv()
        print("Доступные резюме: ")
        for i in list_cv:
            print(i)
        # cv_name = input("Пожалуйста введите название резюме: ") 
        cv_name = "QA Engineer"
        print("Поиск по резюме: ", cv_name)
        href = my_driver.get_recommendations_from_cv(cv_name)
        print("Ссылка на рекомендованные вакансии: ", href)
        # transmittal_letter = input("Введите сопроводительное письмо: ")
        transmittal_letter = "Добрый день!\nПрошу рассмотреть мою кандидатуру на должность: Тестировщик / QA Engineer (manual / automation).\n\nХард скилы:\nPython (pytest, psycopg2, django rest framework + orm, beautiful soup, selenium, aiogram, asyncio, openxlsx).\nJavaScript (jQuery, postman scripts) + HTML\CSS.\nJava (Android), C++ (Qt).\n\nИструменты:\nGit, bash, postman, jmeter, dbeaver, devtools, docker.\n\nGits:\nhttps://gitlab.com/molokov-klim/\nhttps://github.com/molokov-klim/"
        # resp_qty = int(input("Введите количество откликов (максимум 200): "))
        resp_qty = 200
        if resp_qty > 200:
            resp_qty = 200
        list_vacancy_links = my_driver.get_vacancy_links(href, resp_qty)
        print("Список ссылок на вакансии: ", len(list_vacancy_links), "шт")
        #print(list_vacancy_links)
        my_driver.apply_for_a_job(list_vacancy_links, transmittal_letter)


    except Exception as ex:
        print(ex)




# .get_attribute('innerHTML')
