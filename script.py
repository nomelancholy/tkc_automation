import os
import time
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
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920x1080")
# To - Do : time.sleep 들 다 특정 엘리먼트가 나오면 실행되게 변경 필요


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)
load_dotenv(find_dotenv())

# good condition : 3~5 / bad condition : 7~10
WAIT_TIME = 5

ARTIST = "Jedi Mind Tricks"
SONG_TITLE = "The Apostle's Creed"
YEAR = '2002'
COUNT = '2194'
# Take Knowledge's Choice #1832. J. Rawls - Blue #2 (2001) \
FULL_TITLE = f"Take Knowledge's Choice #{COUNT}. {ARTIST} - {SONG_TITLE} ({YEAR})"

FEATURING = ""
FEATURING_MESSAGE = '가 피쳐링한'

# audio | video
LINK_TYPE = 'audio'

YOUTUBE_LINK = 'https://youtu.be/YG-XrlclISs'
IFRAME_LINK = '<iframe width="560" height="315" src="https://www.youtube.com/embed/'+YOUTUBE_LINK.split(
    '/')[3]+'" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'


split_title = FULL_TITLE.split('.', maxsplit=1)
# Take Knowledge's Choice #1832
INDEX_TITLE = split_title[0]
# J. Rawls - Blue #2 (2001)
TITLE = split_title[1].lstrip()

CONTENT = f"{ARTIST}의 {YEAR}년 작 \n {SONG_TITLE}입니다 \n \n 즐감하세요! \n \n"

GUIDE = "그간 올린 곡들은 블로그와 \n 네이버 카페 '랩잡'의 'Take Knowledge' 카테고리에서도 만나 보실 수 있습니다. \n  \n http://blog.naver.com/starmekey \n https://cafe.naver.com/rapsup"

if FEATURING:
    CONTENT = FEATURING + FEATURING_MESSAGE + '\n' + CONTENT

split_content = (CONTENT + GUIDE).split('\n')
HTML_CONTENT = ['<br />' if line == '' else "<p>" +
                line+"</p>" for line in split_content]


def blog_process():
    driver.get('https://blog.naver.com/starmekey?Redirect=Write&categoryNo=24')

    # time.sleep(5)

    # iframes = driver.find_element(By.TAG_NAME('ifram'))

    # print(iframes)

    # for iframe in iframes:
    #     print(iframe)
    # webdriver(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'se-help-panel-close-button')))

    # popup_close_button = driver.find_element(
    #     by=By.CSS_SELECTOR, value='.se-help-panel-close-button')

    # WebDriverWait(driver, 20).until(
    #     EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='mainFrame']")))

    time.sleep(WAIT_TIME)
    driver.switch_to.frame('mainFrame')

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'se-popup-container'))
        )
        popup_cancel_button = driver.find_element(
            by=By.CLASS_NAME, value='se-popup-button-cancel')
        popup_cancel_button.send_keys(Keys.ENTER)

    except:
        print('작성중인 글 없음')

    popup_close_button = driver.find_element(
        by=By.CSS_SELECTOR, value='.se-help-panel-close-button')
    popup_close_button.click()
    time.sleep(WAIT_TIME)

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

    time.sleep(WAIT_TIME)

    time.sleep(WAIT_TIME)

    webdriver.ActionChains(driver=driver).send_keys(CONTENT).perform()

    posting_register_button = driver.find_element(
        by=By.XPATH, value='//span[contains(text(),"발행")]')
    posting_register_button.click()

    posting_confirm_button = driver.find_element(
        by=By.CLASS_NAME, value='confirm_btn__Dv9du')
    posting_confirm_button.click()

    time.sleep(WAIT_TIME)

    bean_popup = driver.find_element(by=By.ID, value='floatingda_content')

    webdriver.ActionChains(driver=driver).move_to_element(
        bean_popup).move_by_offset(5, 5).click().perform()

    print('네이버 블로그 업로드 완료')


def cafe_process():
    driver.get(
        'https://cafe.naver.com/ca-fe/cafes/14371899/menus/571/articles/write?boardType=L')

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'textarea_input'))
        )
    except:
        driver.quit()

    cafe_title_field = driver.find_element(
        by=By.CLASS_NAME, value='textarea_input')
    cafe_title_field.click()
    cafe_title_field.send_keys(FULL_TITLE)

    time.sleep(WAIT_TIME)
    # 엔터를 한번 쳐줘야 하나..?
    
    webdriver.ActionChains(driver=driver).key_down(
        Keys.TAB).key_up(Keys.TAB).perform()

    time.sleep(WAIT_TIME)

    webdriver.ActionChains(driver=driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    # webdriver.ActionChains(driver=driver).key_down(
    #     Keys.TAB).key_up(Keys.TAB).perform()

    # time.sleep(WAIT_TIME)

    pyperclip.copy(YOUTUBE_LINK)

    webdriver.ActionChains(driver=driver).key_down(
        Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'se-section-oembed-video'))
        )
    except:
        driver.quit()

    pyperclip.copy(CONTENT)
    webdriver.ActionChains(driver=driver).key_down(
        Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    time.sleep(WAIT_TIME)

    cafe_register_button = driver.find_element(
        by=By.CLASS_NAME, value='BaseButton__txt')

    cafe_register_button.click()

    time.sleep(WAIT_TIME)

    bean_popup = driver.find_element(by=By.ID, value='floatingda_content')

    webdriver.ActionChains(driver=driver).move_to_element(
        bean_popup).move_by_offset(5, 5).click().perform()

    print('네이버 카페 업로드  완료')


def naver_process():
    driver.get("http://naver.com/")

    NAVER_ID = os.environ.get("NAVER_ID")
    NAVER_PW = os.environ.get("NAVER_PW")

    WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "link_login")))

    login_button = driver.find_element(by=By.CLASS_NAME, value="link_login")
    login_button.click()

    WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, "id")))

    id_field = driver.find_element(by=By.ID, value='id')

    pw_field = driver.find_element(by=By.ID, value='pw')

    id_field.click()
    pyperclip.copy(NAVER_ID)
    id_field.send_keys(Keys.CONTROL, 'v')
    time.sleep(WAIT_TIME)

    pw_field.click()
    pyperclip.copy(NAVER_PW)
    pw_field.send_keys(Keys.CONTROL, 'v')
    time.sleep(WAIT_TIME)

    submit_button = driver.find_element(by=By.ID, value="log.login")
    submit_button.click()

    # current_url = driver.current_url

    # try:
    #     element = WebDriverWait(driver, 5).until(
    #         EC.presence_of_element_located(
    #             (By.XPATH, '//*[@id="NM_FAVORITE"]/div[1]/ul[1]/li[3]/a'))
    #     )
    # except:
    #     print('실패')
    # driver.quit()

    # WebDriverWait(driver, 20).until(EC.url_changes(current_url))

    # 블로그
    blog_process()
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
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.ID, 'account'))
        )
    except:
        # driver.quit()
        print('실패')

    if LINK_TYPE == 'audio':
        driver.get("https://dctribe.com/0/zboard.php?id=audio")
    elif LINK_TYPE == 'video':
        driver.get("https://dctribe.com/0/zboard.php?id=video")

    time.sleep(WAIT_TIME)
    
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

    time.sleep(WAIT_TIME)

    upload_button = driver.find_element(by=By.XPATH, value='//*[@id="delete"]')
    upload_button.click()

    time.sleep(WAIT_TIME)

    print('dct 업로드 완료')


def hiphople_process():
    driver.get(url="https://hiphople.com/")

    HIPHOPLE_ID = os.environ.get("HIPHOPLE_ID")
    HIPHOPLE_PW = os.environ.get("HIPHOPLE_PW")

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'app-header__login'))
        )
    except:
        # driver.quit()
        print('실패')

    popup_load_btn = driver.find_element(by=By.CLASS_NAME, value='app-header__login')

    popup_load_btn.click()

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app-login-form"]/div[1]/div/div[2]/form/input[7]'))
        )
    except:
        # driver.quit()
        print('실패')

    id_field = driver.find_element(by=By.XPATH, value='//*[@id="app-login-form"]/div[1]/div/div[2]/form/input[7]')
    id_field.send_keys(HIPHOPLE_ID)

    pw_field = driver.find_element(by=By.XPATH, value='//*[@id="app-login-form"]/div[1]/div/div[2]/form/input[8]')
    pw_field.send_keys(HIPHOPLE_PW)

    login_btn = driver.find_element(by=By.XPATH, value='//*[@id="app-login-form"]/div[1]/div/div[2]/form/button')
    login_btn.click()

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'app-header-profile'))
        )
    except:
        # driver.quit()
        print('실패')

    try:
        noti_container = driver.find_element(by=By.ID, value='nc_container')
        print('hiphop le 댓글 달림. 확인 필요')
        close_btn = driver.find_element(by=By.CLASS_NAME, value='close')
        close_btn.click()
    except NoSuchElementException:
        print('Hiphop le 달린 댓글 없음')

    driver.get(url='https://hiphople.com/index.php?mid=fboard&act=dispBoardWrite')

    category_select = Select(driver.find_element(by=By.ID, value="category"))
    category_select.select_by_visible_text("음악")

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "wf-input"))
        )
    except:
        # driver.quit()
        print('실패')

    title_field = driver.find_element(
        by=By.CLASS_NAME, value="wf-input")
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

    time.sleep(WAIT_TIME)

    print('hiphop le 업로드 완료')


def o_u_process():
    driver.get(url="http://www.todayhumor.co.kr/")

    time.sleep(WAIT_TIME)

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="id"]'))
        )
    except:
        print('실패')
        # driver.quit()

    O_U_ID = os.environ.get("O_U_ID")
    O_U_PW = os.environ.get("O_U_PW")

    id_field = driver.find_element(by=By.XPATH, value='//*[@id="id"]')
    id_field.send_keys(O_U_ID)

    pw_field = driver.find_element(by=By.ID, value="passwd")
    pw_field.send_keys(O_U_PW)

    login_button = driver.find_element(by=By.CLASS_NAME, value="login_btn")
    login_button.click()

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="login_user_menu"]/span'))
        )
    except:
        print('실패')
        # driver.quit()

    driver.get("http://www.todayhumor.co.kr/board/write.php?table=music")

    title_field = driver.find_element(by=By.ID, value='subject')
    title_field.send_keys(INDEX_TITLE)

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'cheditor-tab-code-off'))
        )
    except:
        print('실패')
        # driver.quit()

    frame_change_to_html_button = driver.find_element(
        by=By.CLASS_NAME, value='cheditor-tab-code-off')
    frame_change_to_html_button.click()

    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'cheditor-editarea-text-content'))
        )
    except:
        print('실패')
        # driver.quit()

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

    time.sleep(WAIT_TIME)

    print('오유 업로드 완료')


naver_process()
dct_process()
o_u_process()
hiphople_process()
driver.quit()
