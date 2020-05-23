from selenium import webdriver
import chromedriver_binary
from time import sleep
import datetime

def dating(hoge):
    k = hoge.split('/')
    return datetime.date(int(k[0]),int(k[1]),int(k[2]))

def make_datetime(hoge,fuga):
    k = fuga.split(':')
    l = hoge.split('/')
    return datetime.datetime(int(l[0]),int(l[1]),int(l[2]),int(k[0]),int(k[1]))


#ブラウザはchrome,あえてブラウザは表示させました。

browser = webdriver.Chrome()
browser.get("https://panda.ecs.kyoto-u.ac.jp/portal/")

lgin = browser.find_element_by_id("loginLink1")
lgin.click()

#usernameとpasswordは自分がいつも使ってる奴にしてください。

userid = browser.find_element_by_id("username")
userid.send_keys("YOUR_OWN_USERNAME")

password = browser.find_element_by_id("password")
password.send_keys("YOUR_OWN_PASSWORD")

sleep(1)

login = browser.find_element_by_name("submit")
login.click()
#ここまででログインをします
browser.implicitly_wait(3)

dashboard = browser.find_element_by_link_text("サイトセットアップ")
dashboard.click()

print("login ok")

sleep(2)

iframe = browser.find_element_by_id("your_iframe_1")
# 上について:ここのiframeのidが人によって異なるかもしれないので変えておきました。
browser.switch_to_frame(iframe)

cources = browser.find_elements_by_tag_name("tr")

url_list = []
for cource in cources:
    urls = cource.find_elements_by_tag_name('a')
    for a in urls:
        url = a.get_attribute("href")

        """
        下のif文の意図を書きます。
        urlsに入っているaタグのhrefは二つあります。
        1つは講義のURLでもう1つはhref="#"です。
        href="#"が講義のURLリストに入るのは避けたいので下のif文を書きました。
        """

        if url == "#_URL": #urlsには講義のURLともう一つ別のURLが入っています。後者を避けるためのif文です。
            continue
        url_list.append(url)

"""
この下、urls_2020の所は自分専用の形になってます。公開するとは思っていなかったので。
上のforループでpandaにある全ての講義のurlを取得しました。
しかし私のpandaには2019年の講義のURLやら教職関連のURLやらがあったので除去しなくてはいけません。
その作業を下で行っています。
もしこれを利用するのであれば、どうかご自分に合った形に変形してください。
よろしくお願い致します。
"""

urls = url_list[6:] #2019年度の除去
address = urls[:-2] #教職関連の除去
urls_2020 = address[7:] #ここゴチャっとしてるんですけど、2020前期の講義だけ集めてます

today = datetime.date.today()
assignment_lists = []
for c in urls_2020:
    browser.get(c)
    sleep(2)
    assignment = browser.find_element_by_partial_link_text("課題")
    # 上について:課題/assignment　っていう形をした講義があったので。partialにしました。
    assignment.click() #自分用なので、テスト/クイズには対応していません。
    sleep(2)
    iframe = browser.find_element_by_class_name("portletMainIframe")
    # 多分こっちのiframeのclass_nameはみんな同じだと思います。
    browser.switch_to_frame(iframe)
    tt = browser.title
    try:
        table = browser.find_element_by_xpath('/html/body/div/form/table')
        ass = table.find_elements_by_tag_name("tr")
        li = []
        for i in ass:
            li.append(i.text)
        n = len(li)
        for i in range(n):
            k = li[i].split()
            if k[1] == "未開始":
                deadline = dating(k[4])
                dt = deadline - today
                if dt.days >= 0:
                    duetime = make_datetime(k[4],k[5])
                    asi_title = tt + ":" + k[0]
                    assignment_lists.append((asi_title,duetime))
    except Exception as e:
        continue #そもそもテーブルが用意されていない講義もあります。（民俗学とか）

print("get assignment data collectly")

browser.quit()

"""
この下からはほぼgoogleカレンダーAPIの話です。
credentials.jsonファイルとAPIの準備が必要です。
カレンダーIDは簡単に調べられます。
"""

# 必要なモジュールをインポート
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

    # カレンダーAPIで操作できる範囲を設定（今回は読み書き）
SCOPES = ['https://www.googleapis.com/auth/calendar']

    # Google にcalendarへのアクセストークンを要求してcredsに格納します。
creds = None

    # 有効なトークンをすでに持っているかチェック（２回目以降の実行時に認証を省略するため） 
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    # 期限切れのトークンを持っているかチェック（認証を省略するため）
if not creds or not creds.valid:
    if creds and creds.expired and creds.refrestoken:
        creds.refresh(Request())
        # アクセストークンを要求
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # アクセストークン保存（２回目以降の実行時に認証を省略するため）
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

N = len(assignment_lists)

for i in range(N):
    flag = 0
    deadline = assignment_lists[i][1]
    td = datetime.timedelta(days=1)
    dd = deadline - td
    timefrom = dd.isoformat() + 'Z'
    events_result = service.events().list(calendarId="YOUR_OWN_CALENDARID",timeMin=timefrom,maxResults=7,singleEvents=True,orderBy='startTime').execute()
    eves = events_result.get('items',[])
    #毎回全部データを取得するので、すでにカレンダーに書き込まれていないかチェックします。
    for eve in eves:
        if eve["summary"] == assignment_lists[i][0]:
            flag = 1
            break
    if flag == 1:
        continue

    event = {
        'summary' : assignment_lists[i][0],
        'start': {
            "dateTime":deadline.isoformat(),
            "timeZone":"Japan"
        },
        "end":{
            "dateTime":deadline.isoformat(),
            "timeZone":"Japan"
        }
    }
    event = service.events().insert(calendarId="YOUR_OWN_CALENDAR_ID",body=event).execute()

print("complete!!")