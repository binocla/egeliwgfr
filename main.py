import requests
from bs4 import BeautifulSoup
import vk_api
from vk_api import VkApi
import time
import uuid
from selenium import webdriver
from vk_api import VkUpload


def russk(rus):
    if rus == 0:
        return 'Нет результата'
    else:
        return 'Есть результат!'


def mathh(math):
    if math == 0:
        return 'Нет результата'
    else:
        return 'Есть результат!'


def obsh(obs):
    if obs == 0:
        return 'Нет результата'
    else:
        return 'Есть результат!'


vk: VkApi = vk_api.VkApi(token="9408bb3dbb78b015651dfa7ca880d63d3a17d2a5c579ccc95afca318d4ec870cd4cad5583f99447e687a0")
vk._auth_token()

group_id = 173120410

longPoll = vk.method("groups.getLongPollServer", {"group_id": group_id})
server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']

while True:
    try:

        longPoll = requests.post('%s' % server, data={'act': 'a_check',
                                                      'key': key,
                                                      'ts': ts,
                                                      'wait': 25}).json()
        if longPoll['updates'] and len(longPoll['updates']) != 0:
            for update in longPoll['updates']:
                if update['type'] == 'message_new':
                    print(update)
                    id = update['object']['peer_id']
                    body = update['object']['text']
                    if body:
                        cookies = {
                            'Participant': 'FA063F04A162AABBB2D68C6D6FF917B0AECADC5BD5C42223C6A13BBD8FBF0BCC08EDDC41F1DA2789DD3EC905EC00C19FBF3C9836CEAD42FDD7C93777446EDB83817E58A2547B13A40BC3D3103AB91F048848B9F27A144A0749B8DE221B908DBF018C5627'}

                        urlm = 'http://check.ege.edu.ru/exams/24'
                        rm = requests.get(urlm, cookies=cookies)
                        soupm = BeautifulSoup(rm.text)

                        math = soupm.find('div', {'id': 'notice-1'})['class'][0]

                        urlr = 'http://check.ege.edu.ru/exams/21'
                        rr = requests.get(urlr, cookies=cookies)
                        soupr = BeautifulSoup(rm.text)

                        print(soupr)
                        rus = soupr.find('div', {'id': 'notice-1'})['class'][0]

                        urlo = 'http://check.ege.edu.ru/exams/29'
                        ro = requests.get(urlo, cookies=cookies)
                        soupo = BeautifulSoup(ro.text)

                        obs = soupo.find('div', {'id': 'notice-1'})['class'][0]

                        if rus == 'hidden':
                            rus = 0
                        else:
                            rus = 1
                        if math == 'hidden':
                            math = 0
                        else:
                            math = 1
                        if obs == 'hidden':
                            obs = 0
                        else:
                            obs = 1

                        driver = webdriver.Chrome('chromedriver.exe')
                        driver.set_window_size(1600, 1000)
                        cookie = {
                            'name': 'Participant',
                            'value': 'FA063F04A162AABBB2D68C6D6FF917B0AECADC5BD5C42223C6A13BBD8FBF0BCC08EDDC41F1DA2789DD3EC905EC00C19FBF3C9836CEAD42FDD7C93777446EDB83817E58A2547B13A40BC3D3103AB91F048848B9F27A144A0749B8DE221B908DBF018C5627'}

                        driver.get('http://check.ege.edu.ru/exams')
                        driver.add_cookie(cookie)
                        driver.get('http://check.ege.edu.ru/exams')
                        driver.save_screenshot("screenshot.png")
                        driver.quit()
                        upload = VkUpload(vk)
                        attachments = []
                        photo = upload.photo_messages('screenshot.png')[0]
                        attachments.append(
                            'photo{}_{}'.format(photo['owner_id'], photo['id'])
                        )
                        print(photo)
                        print(attachments)
                        vk.method("messages.send",
                                  {"peer_id": id, "attachment": attachments,
                                   "message": 'Математика: ' + mathh(math) + '\nРусский язык: ' + russk(
                                       rus) + '\nОбществознание: ' + obsh(
                                       obs) + '\n\nСайт ЕГЭ http://check.ege.edu.ru/exams',
                                   "random_id": uuid.uuid4().int})
                ts = longPoll['ts']
                time.sleep(1)
    except Exception as E:
        print(E)
        longPoll = vk.method("groups.getLongPollServer", {"group_id": group_id})
        server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']
        time.sleep(1)
