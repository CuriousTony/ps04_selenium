from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import textwrap


def get_url():
    driver = webdriver.Chrome()
    try:
        driver.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
        assert 'Википедия' in driver.title
        time.sleep(3)

        user_choice = input("Введите интересующую Вас тему: ")
        search_box = driver.find_element(By.CLASS_NAME, 'vector-search-box-input')
        search_box.send_keys(user_choice)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)
        link = driver.find_element(By.LINK_TEXT, user_choice.title())
        link.click()
        time.sleep(5)

        user_pick = input("Выберите дальнейшее действие:\n"
                          "1. Листаем параграфы выбранной статьи;\n"
                          "2. Переходим на одну из связанных страниц;\n"
                          "3. Выйти из программы.\n"
                          "Введите 1. 2 или 3: ")
        if user_pick == '1':
            paragraphs = driver.find_elements(By.TAG_NAME, 'p')
            for paragraph in paragraphs:
                # приводим вывод в читаемый многострочный вид
                wrapped_paragraph = textwrap.fill(paragraph.text, width=80)
                print(wrapped_paragraph)
                input()
        # TODO сделать выход из листания параграфов
        if user_pick == '2':
            pass

        if user_pick == '3':
            print("Selenium остановлен пользователем.")
            driver.quit()

    except KeyboardInterrupt:
        print("Selenium остановлен пользователем.")

    finally:
        driver.quit()


get_url()
