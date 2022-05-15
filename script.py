import os
import time
from turtle import title
import pyperclip

from selenium import webdriver
from dotenv import load_dotenv, find_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# chrome driver setup

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument('headless')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
load_dotenv(find_dotenv())

ARTIST = 'Declaime'
SONG_TITLE = "Exclaim The Name"
YEAR = '2001'
# Take Knowledge's Choice #1832. J. Rawls - Blue #2 (2001) \
FULL_TITLE = f"Take Knowledge's Choice #1929. {ARTIST} - {SONG_TITLE} ({YEAR})"
split_title = FULL_TITLE.split('.', maxsplit=1)
# Take Knowledge's Choice #1832
INDEX_TITLE = split_title[0]
# J. Rawls - Blue #2 (2001)
TITLE = split_title[1].lstrip()

FEATURING = ''

CONTENT = f"{ARTIST}의 {YEAR}년 작 \n {SONG_TITLE}입니다 \n \n 즐감하세요! \n \n"

GUIDE = "그간 올린 곡들은 블로그와 \n 네이버 카페 '랩잡'의 'Take Knowledge' 카테고리에서도 만나 보실 수 있습니다. \n  \n http://blog.naver.com/starmekey \n https://cafe.naver.com/rapsup"

if FEATURING:
    CONTENT = FEATURING + '\n' + CONTENT

split_content = (CONTENT + GUIDE).split('\n')
HTML_CONTENT = ['<br />' if line == '' else "<p>" +
                line+"</p>" for line in split_content]
# audio | video
LINK_TYPE = 'audio'

YOUTUBE_LINK = 'https://youtu.be/RnDbYLRGIkI'
IFRAME_LINK = '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+YOUTUBE_LINK.split(
    '/')[3]+'" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

def blog_process():
    driver.get('https://blog.naver.com/starmekey?Redirect=Write&categoryNo=24')


    time.sleep(3)
    driver.switch_to.frame('mainFrame')

    time.sleep(2)

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'se-popup-container'))
        )
        popup_cancel_button = driver.find_element(by=By.CLASS_NAME, value='se-popup-button-cancel')
        popup_cancel_button.send_keys(Keys.ENTER)

    except:
        print('작성중인 글 없음')

    popup_close_button = driver.find_element(
        by=By.CSS_SELECTOR, value='.se-help-panel-close-button')
    popup_close_button.click()
    time.sleep(2)

    # title_field = driver.find_element(
    # by=By.CSS_SELECTOR, value='span.se-ff-nanumgothic.se-fs32.__se-node')

    blog_title_field = driver.find_element(
        by=By.XPATH, value='//span[contains(text(),"제목")]')

    blog_title_field.click()

    webdriver.ActionChains(driver=driver).send_keys(TITLE).perform()

    blog_content_field = driver.find_element(
        by=By.XPATH, value='//span[contains(text(),"본문에")]')

    blog_content_field.click()

    pyperclip.copy(YOUTUBE_LINK)
    webdriver.ActionChains(driver=driver).key_down(
        Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    time.sleep(5)

    webdriver.ActionChains(driver=driver).send_keys(CONTENT).perform()

    posting_register_button = driver.find_element(
        by=By.XPATH, value='//span[contains(text(),"발행")]')
    posting_register_button.click()

    posting_confirm_button = driver.find_element(by=By.CLASS_NAME, value='confirm_btn__Dv9du')
    posting_confirm_button.click()

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'floatingda_content'))
        )

        receive_bean_button = driver.find_element(
        by=By.XPATH, value='//span[contains(text(),"기부콩")]')

        receive_bean_button.click()
        print('네이버 블로그 완료')
    except:
        print('네이버 블로그 완료 (콩 받기는 실패)')
        driver.quit()
    

def cafe_process():
    driver.get(
        'https://cafe.naver.com/ca-fe/cafes/14371899/menus/571/articles/write?boardType=L')

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'textarea_input'))
        )
    except:
        driver.quit()

    cafe_title_field = driver.find_element(
        by=By.CLASS_NAME, value='textarea_input')
    cafe_title_field.click()
    cafe_title_field.send_keys(FULL_TITLE)

    cafe_content_field = driver.find_element(
        by=By.XPATH, value='//span[contains(text(),"내용을")]')

    cafe_content_field.click()

    pyperclip.copy(YOUTUBE_LINK)
    webdriver.ActionChains(driver=driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    try:
        element = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'se-section-oembed-video'))
        )
    except:
        driver.quit()

    pyperclip.copy(CONTENT)
    webdriver.ActionChains(driver=driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    cafe_register_button = driver.find_element(
        by=By.CLASS_NAME, value='BaseButton__txt')

    cafe_register_button.click()

    time.sleep(3)
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'floatingda_content'))
        )

        receive_bean_button = driver.find_element(
        by=By.XPATH, value='//span[contains(text(),"기부콩")]')

        receive_bean_button.click()
    except:
        driver.quit()

def naver_process():
    driver.get("http://naver.com/")

    NAVER_ID = os.environ.get("NAVER_ID")
    NAVER_PW = os.environ.get("NAVER_PW")

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'link_login'))
        )
    except:
        driver.quit()

    # login_button = driver.find_element_by_css_selector(".link_login")
    login_button = driver.find_element(by=By.CLASS_NAME, value="link_login")
    login_button.click()

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'id'))
        )
    except:
        driver.quit()

    # id_field = driver.find_element_by_id('id')
    id_field = driver.find_element(by=By.ID, value='id')

    # pw_field = driver.find_element_by_id('pw')
    pw_field = driver.find_element(by=By.ID, value='pw')

    id_field.click()
    pyperclip.copy(NAVER_ID)
    id_field.send_keys(Keys.CONTROL, 'v')
    time.sleep(2)

    pw_field.click()
    pyperclip.copy(NAVER_PW)
    pw_field.send_keys(Keys.CONTROL, 'v')
    time.sleep(2)

    # submit_button = driver.find_element_by_id("log.login")
    submit_button = driver.find_element(by=By.ID, value="log.login")
    submit_button.click()

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="NM_FAVORITE"]/div[1]/ul[1]/li[3]/a'))
        )
    except:
        driver.quit()

    # 블로그
    # blog_process()
    # 까페
    cafe_process()

def dct_process():
    driver.get("https://dctribe.com/")

    DCT_ID = os.environ.get("DCT_ID")
    DCT_PW = os.environ.get("DCT_PW")

    id_field = driver.find_element(by=By.ID, value="user_id")
    id_field.send_keys(DCT_ID)

    pw_field = driver.find_element(by=By.ID, value="passwd")
    pw_field.send_keys(DCT_PW)

    login_button = driver.find_element(
        by=By.XPATH, value='//*[@id="login"]/form/div[3]/input')
    login_button.click()

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'account'))
        )
    except:
        driver.quit()

    if LINK_TYPE == 'audio':
        driver.get("https://dctribe.com/0/zboard.php?id=audio")
    elif LINK_TYPE == 'video':
        driver.get("https://dctribe.com/0/zboard.php?id=video")

    write_button = driver.find_element(
        by=By.XPATH, value='//*[@id="bottom"]/div[2]/a')
    write_button.click()

    category_select = Select(driver.find_element(
        by=By.XPATH, value='//*[@id="post"]/form/div[1]/select'))
    category_select.select_by_visible_text("foreign")

    title_field = driver.find_element(by=By.CLASS_NAME, value='post_input')
    title_field.send_keys(FULL_TITLE)

    iframe = driver.find_element(
        by=By.XPATH, value='//*[@id="cke_1_contents"]/iframe')
    driver.switch_to.frame(iframe)

    editor = driver.find_element(by=By.XPATH, value='/html/body')
    editor.send_keys(CONTENT + GUIDE)

    driver.switch_to.default_content()

    link_field = driver.find_element(
        by=By.XPATH, value='//*[@id="post"]/form/div[8]/input')
    link_field.send_keys(YOUTUBE_LINK)

    time.sleep(2)

    upload_button = driver.find_element(by=By.XPATH, value='//*[@id="delete"]')
    upload_button.click()

    time.sleep(2)

    print('dct 업로드 완료')


def hiphople_process():
    driver.get(url="https://hiphople.com/")

    HIPHOPLE_ID = os.environ.get("HIPHOPLE_ID")
    HIPHOPLE_PW = os.environ.get("HIPHOPLE_PW")

    popup_load_btn = driver.find_element(by=By.CLASS_NAME, value='tg_btn')

    popup_load_btn.click()

    id_field = driver.find_element(by=By.ID, value="uid")
    id_field.send_keys(HIPHOPLE_ID)

    pw_field = driver.find_element(by=By.ID, value="upw")
    pw_field.send_keys(HIPHOPLE_PW)

    login_btn = driver.find_element(by=By.CLASS_NAME, value='login_btn')
    login_btn.click()

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'LOGOUT'))
        )
    except:
        driver.quit()

    try:
        noti_container = driver.find_element(by=By.ID, value='nc_container')
        print('hiphop le 댓글 달림. 확인 필요')
        close_btn = driver.find_element(by=By.CLASS_NAME, value='close')
        close_btn.click()
    except NoSuchElementException:
        print('달린 댓글 없음')

    driver.get(url='https://hiphople.com/index.php?mid=fboard&act=dispBoardWrite')

    category_select = Select(driver.find_element(by=By.ID, value="category"))
    category_select.select_by_visible_text("음악")

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id=\"gap\"]/div/div/form/div[2]/div[2]/input"))
        )
    except:
        driver.quit()

    title_field = driver.find_element(
        by=By.XPATH, value="//*[@id=\"gap\"]/div/div/form/div[2]/div[2]/input")
    title_field.send_keys(FULL_TITLE)

    html_code_button = driver.find_element(by=By.ID, value='cke_40')
    html_code_button.click()

    html_editor = driver.find_element(
        by=By.XPATH, value='//*[@id="cke_1_contents"]/textarea')
    html_editor.send_keys(IFRAME_LINK)

    disable_code = driver.find_element(by=By.XPATH, value='//*[@id="cke_40"]')
    disable_code.click()

    iframe = driver.find_element(
        by=By.XPATH, value='//*[@id="cke_1_contents"]/iframe')
    driver.switch_to.frame(iframe)

    editor = driver.find_element(by=By.XPATH, value='/html/body/p')
    editor.send_keys('\n\n')
    editor.send_keys(CONTENT + GUIDE)

    driver.switch_to.default_content()

    reg_btn = driver.find_element(by=By.ID, value='cmd_reg')
    reg_btn.click()

    time.sleep(2)

    print('hiphop le 업로드 완료')


def o_u_process():
    driver.get(url="http://www.todayhumor.co.kr/")

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="id"]'))
        )
    except:
        driver.quit()

    O_U_ID = os.environ.get("O_U_ID")
    O_U_PW = os.environ.get("O_U_PW")

    id_field = driver.find_element(by=By.XPATH, value='//*[@id="id"]')
    id_field.send_keys(O_U_ID)

    pw_field = driver.find_element(by=By.ID, value="passwd")
    pw_field.send_keys(O_U_PW)

    login_button = driver.find_element(by=By.CLASS_NAME, value="login_btn")
    login_button.click()

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="login_user_menu"]/span'))
        )
    except:
        driver.quit()

    driver.get("http://www.todayhumor.co.kr/board/write.php?table=music")

    title_field = driver.find_element(by=By.ID, value='subject')
    title_field.send_keys(INDEX_TITLE)

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'cheditor-tab-code-off'))
        )
    except:
        driver.quit()

    frame_change_to_html_button = driver.find_element(
        by=By.CLASS_NAME, value='cheditor-tab-code-off')
    frame_change_to_html_button.click()

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'cheditor-editarea-text-content'))
        )
    except:
        driver.quit()

    html_area = driver.find_element(
        by=By.CLASS_NAME, value='cheditor-editarea-text-content')
    html_area.send_keys(IFRAME_LINK)
    html_area.send_keys(HTML_CONTENT)

    frame_change_to_editor_button = driver.find_element(
        by=By.CLASS_NAME, value='cheditor-tab-rich-off')
    frame_change_to_editor_button.click()

    submit_button = driver.find_element(
        by=By.XPATH, value='//*[@id="write_form"]/table/tbody/tr[2]/td/table/tbody/tr[8]/td/div/input')
    submit_button.click()

    time.sleep(2)

    print('오유 업로드 완료')


naver_process()
# dct_process()
# o_u_process()
# hiphople_process()
# driver.quit()
