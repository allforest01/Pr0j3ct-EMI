import os, requests, pickle, random, time, json, shutil, subprocess, platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class DriverOptions(object):
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--start-maximized")
        # self.options.add_argument('--start-fullscreen')
        self.options.add_argument("--single-process")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--incognito")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("disable-infobars")


class WebDriver(DriverOptions):
    def __init__(self, path=""):
        DriverOptions.__init__(self)
        self.driver_instance = self.get_driver()

    def get_driver(self):
        webdriver.DesiredCapabilities.CHROME["acceptSslCerts"] = True
        driver = webdriver.Chrome(options=self.options)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
            },
        )
        return driver

# GLOBAL VARIBLE -------------
users_dir = "./users/"
shop_id = item_id = model_id = selected_number = ""
# model_list = []
item_link = ""
# ----------------------------

random.seed(time.time())
seed = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

user_agents = [line.decode("utf-8")[:-1] for line in open("user_agents", "rb")]


def randstr(len):
    ret = ""
    for i in range(len):
        ret += seed[random.randint(0, 61)]
    return ret


def show_list():
    print("--------------------------------")
    print("Danh sach tai khoan:")
    cnt = 0
    for username in os.listdir("users"):
        if username == ".DS_Store" or username == "old":
            continue
        cnt += 1
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": user_agents[random.randint(0, 29)],
                "x-csrftoken": randstr(32),
                "x-api-source": "pc",
                "x-cv-id": "106",
                "Connection": "keep-alive",
            }
        )
        cookies = {}
        error = 0
        try:
            for cookie in pickle.load(open(users_dir + username, "rb")):
                cookies[cookie["name"]] = cookie["value"]
        except:
            error = 1
        else:
            response = session.get(
                "https://shopee.vn/api/v2/user/login_status", cookies=cookies
            )
            error = response.json()["error"]
        print(
            "[" + str(cnt) + "]",
            username,
            "(" + ("active" if error == 0 else "expired") + ")",
        )


def add_user():
    print("--------------------------------")
    username = input("username: ")
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": user_agents[random.randint(0, 29)],
            "x-csrftoken": randstr(32),
            "x-api-source": "pc",
            "x-cv-id": "106",
            "Connection": "keep-alive",
        }
    )
    driver = WebDriver().driver_instance
    driver.get("https://shopee.vn/buyer/login")
    cookies = {}
    time.sleep(5)
    if username != "":
        try:
            for cookie in pickle.load(open(users_dir + "old/" + username, "rb")):
                driver.add_cookie(cookie)
        except:
            print("Co loi xay ra! [Err Code: 0]")
            return 0
    cnt = 0
    while True:
        time.sleep(5)
        cookies = {}
        try:
            for cookie in driver.get_cookies():
                cookies[cookie["name"]] = cookie["value"]
            try:
                response = session.get(
                    "https://shopee.vn/api/v2/user/login_status", cookies=cookies
                )
            except:
                print("Co loi . . .")
                continue
        except:
            print("Co loi get_cookies . . .")
            continue
        if response.json()["error"] == 0:
            print("Dang nhap thanh cong!       ")
            username = response.json()["data"]["username"]
            print("username:", username)
            pickle.dump(driver.get_cookies(), open(users_dir + username, "wb"))
            break
        else:
            print("Dang cho ban dang nhap ", end="")
            for i in range(4):
                print(" ."[i < cnt % 4], end="")
            print("\r", end="")
            cnt += 1
        time.sleep(1)


def rem_user():
    print("--------------------------------")
    username = input("Nhap username muon xoa: ")
    try:
        shutil.move(users_dir + username, users_dir + "old/" + username)
    except:
        print("Xoa tai khoan khong thanh cong!")
    else:
        print("Xoa tai khoan thanh cong!")


def model_info():
    for username in os.listdir("users"):
        if username == ".DS_Store" or username == "old":
            continue
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": user_agents[random.randint(0, 29)],
                "x-csrftoken": randstr(32),
                "x-api-source": "pc",
                "x-cv-id": "106",
                "Connection": "keep-alive",
            }
        )
        cookies = {}
        try:
            for cookie in pickle.load(open(users_dir + username, "rb")):
                cookies[cookie["name"]] = cookie["value"]
        except:
            print("Co loi xay ra! [Err Code: 0]")
            return 0
    session.cookies.update(cookies)
    item_info = json.loads(open("item_data", "r").read())
    global item_id, shop_id
    item_id = item_info["data"]["item"]["item_id"]
    shop_id = item_info["data"]["item"]["shop_id"]
    print("Ten item:", item_info["data"]["item"]["title"])
    print("Ten shop:", item_info["data"]["shop_detailed"]["name"])
    models = item_info["data"]["item"]["models"]
    number = 0
    for model in models:
        print("> So thu tu:", "[" + str(number) + "]")
        print("> Loai hang:", model["name"])
        print("> Gia tien:", f"{model['price'] // 100000:,}")
        print("> So luong:", model["stock"])
        print("--------------------------------")
        number = number + 1
    # global model_list
    # model_list = []
    # options_selected = []
    # while True:
    # 	selected_number = int(input('Chon so thu tu: '))
    # 	if selected_number == -1:
    # 		break
    # 	model_id = models[selected_number]['model_id']
    # 	name = models[selected_number]['name']
    # 	model_list.append(model_id)
    # 	options_selected.append(name)
    # print(model_list)
    # print('--------------------------------')
    # print('Danh sach loai hang da chon:')
    # for name in options_selected:
    # 	print('[', name, ']')
    global model_id
    selected_number = int(input("Chon so thu tu: "))
    model_id = models[selected_number]["model_id"]
    name = models[selected_number]["name"]
    print("Ban da chon:", name)
    input("Nhan enter de bat dau dat hang!")


def cute_checkout():
    print("--------------------------------")
    model_info()

    global model_list
    for username in os.listdir("users"):
        if username == ".DS_Store" or username == "old":
            continue
        # cmd = 'cd ' + os.getcwd() + ' && python3 MAGIC.py ' + username + ' ' + str(shop_id) + ' ' + str(item_id) + ' ' + str(len(model_list))
        # for model in model_list:
        # 	cmd += ' ' + str(model)
        cmd = ' '.join(["cd", os.getcwd(), "&&", "python3", "MAGIC.py", username, str(shop_id), str(item_id), str(model_id)])
        if platform.system() == "Windows":
            cmd = ['start', 'cmd', '/k', cmd]
        elif platform.system() == "Linux":
            cmd = ['gnome-terminal', '--', 'bash', '-c', cmd]
        elif platform.system() == "Darwin":
            cmd = ['osascript', '-e', f'tell app "Terminal" to do script "{cmd}"']
        # print(cmd)
        subprocess.run(cmd)


def login():
    print("--------------------------------")
    username = input("Nhap username: ")

    driver = WebDriver().driver_instance
    driver.get("https://shopee.vn/buyer/login")
    for cookie in pickle.load(open(users_dir + username, "rb")):
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.get("https://shopee.vn/user/purchase/?type=9")
    input("Bam phim bat ky de tiep tuc . . .")


if __name__ == "__main__":

	os.system("clear")

	while True:
		print("\n--------[Pr0j3ct-EMI]--------")
		print("[1] Hien thi danh sach tai khoan")
		print("[2] Them tai khoan")
		print("[3] Xoa tai khoan")
		print("[4] Tu dong dat hang")
		print("[5] Dang nhap tai khoan")
		print("[-] Thoat chuong trinh")

		try:
			opt = int(input("Nhap lua chon: "))
		except:
			break

		if opt == 1:
			show_list()
		elif opt == 2:
			add_user()
		elif opt == 3:
			rem_user()
		elif opt == 4:
			cute_checkout()
		elif opt == 5:
			login()
		else:
			break
