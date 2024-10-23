from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import textwrap
import random


driver = webdriver.Chrome()
url = 'https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'


def questioning():
    answer = input("Выберите дальнейшее действие:\n"
                      "1. Листаем параграфы выбранной статьи;\n"
                      "2. Переходим на одну из связанных страниц;\n"
                      "3. Выйти из программы.\n"
                      "Введите 1, 2 или 3: ")
    return answer


def check_answer(driver, answer):
    if answer == '1':
        try:
            browse_paragraphs(driver)
        except Exception as e:
            print(f"Ошибка в функции browse_paragraphs - {e}")
    elif answer == '2':
        try:
            browse_links(driver)
        except Exception as e:
            print(f"Ошибка в функции browse_links - {e}")
    elif answer == '3':
        print('Процесс остановлен пользователем.')
        driver.quit()
        return
    else:
        print('Ошибка ввода, выберите один из предложенных вариантов действий.')
        new_answer = questioning()
        check_answer(driver, new_answer)


def browse_paragraphs(driver):
    try:
        count = 0
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        for paragraph in paragraphs:
            # Приводим однострочный вывод в удобоваримый вид:
            wrapped_paragraph = textwrap.fill(paragraph.text, width=80)
            print(wrapped_paragraph)
            input()
            count += 1

            if count % 3 == 0:
                print("Желаете продолжить листать параграфы статьи?")
                counter = input("д/н: ")
                if counter == 'д':
                    print(wrapped_paragraph)
                    input()
                    count += 1
                else:
                    answer = questioning()
                    check_answer(driver, answer)
    except Exception as e:
        print(f"Ошибка в ходе выполнения browse_paragraphs - {e}")


def browse_links(driver):
    links_list = []
    try:
        all_the_links = driver.find_elements(By.TAG_NAME, 'a')
        for link in all_the_links:
            links_list.append(link.get_attribute('href'))

        random_link = random.choice(links_list)
        driver.get(random_link)
        browse_paragraphs(driver)
    except Exception as e:
        print(f"Ошибка в функции browse_links - {e}")


def main(driver):
    driver.get(url=url)
    assert 'Википедия' in driver.title
    time.sleep(3)
    user_topic = input('Введите тему для поиска на Вики: ')

    try:
        search_box = driver.find_element(By.CLASS_NAME, 'vector-search-box-input')
        search_box.send_keys(user_topic)
        search_box.send_keys(Keys.ENTER)

        search_article = driver.find_element(By.LINK_TEXT, user_topic.title())
        search_article.click()
        time.sleep(5)

        print("Для вывода каждого следующего параграфа жмите 'Enter'.\n")
        browse_paragraphs(driver)

    except Exception as e:
        print(f"Ошибка в функции main - {e}.")

    finally:
        print("\nЗавершение процесса по сценарию finally.")
        if driver:
            driver.quit()


if __name__ == "__main__":
    main(driver)
