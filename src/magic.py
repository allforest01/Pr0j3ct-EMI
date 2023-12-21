import os, requests, pickle, random, time, json, sys

# GLOBAL VARIBLE -------------
users_dir = "./users/"
username = sys.argv[1]
shopid = int(sys.argv[2])
itemid = int(sys.argv[3])
# models_len = int(sys.argv[4])
# model_list = []
# for i in range(models_len):
# 	model_list.append(int(sys.argv[5 + i]))
modelid = int(sys.argv[4])
# ----------------------------

random.seed(int(time.time()) * len(username) * ord(username[0]) * ord(username[1]))
seed = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

# device_sz_fingerprints = [line.decode('utf-8')[:-1] for line in open('device_sz_fingerprints', 'rb')]
user_agents = [line.decode("utf-8")[:-1] for line in open("user_agents", "rb")]


def randstr(len):
    ret = ""
    for i in range(len):
        ret += seed[random.randint(0, 61)]
    return ret


os.system("clear")
print("\n--------[Pr0j3ct-EMI]--------")
print("[ username:", username, "]")

# Dang nhap bang cookies
session = requests.Session()
session.headers.update(
    {
        "User-Agent": user_agents[random.randint(0, 29)],
        "x-csrftoken": randstr(32),
        "x-api-source": "rn",
        "x-cv-id": "106",
        "Connection": "keep-alive",
        "if-none-match-": "55b03-" + randstr(32),
        "Content-Type": "application/json",
    }
)

cookies = {}
for cookie in pickle.load(open(users_dir + username, "rb")):
    cookies[cookie["name"]] = cookie["value"]

session.cookies.update(cookies)

validate_checkout = json.dumps(
    {
        "shop_orders": [
            {
                "shop_info": {"shop_id": shopid},
                "item_infos": [{"item_id": itemid, "model_id": modelid, "quantity": 1}],
            }
        ]
    }
)

checkout_get_data = {
    "cart_type": 1,
    "client_id": 5,
    "shoporders": [
        {
            "shop": {"shopid": shopid},
            "items": [
                {
                    "itemid": itemid,
                    "modelid": modelid,
                    "quantity": 1,
                }
            ],
        }
    ]
    # ,
    # 'promotion_data' : {
    # 	'free_shipping_voucher_info' : {}
    # }
}

# for model in model_list:
# 	checkout_get_data['shoporders'][0]['items'].append(
# 		{
# 			'itemid' : itemid,
# 			'modelid' : model,
# 			'quantity' : 1,
# 		}
# 	)

# get_vouchers_data = {
# 	'orders' : json.dumps(
# 		[
# 			{
# 				'iteminfos' : checkout_get_data['shoporders'][0]['items']
# 			}
# 		]
# 	)
# }

# Ap ma voucher dau tien dung duoc
# vouchers = session.post('https://shopee.vn/api/v2/voucher_wallet/get_recommend_platform_vouchers', data=json.dumps(get_vouchers_data)).json()['data']['freeshipping_vouchers']
# for voucher in vouchers:
# 	checkout_get_data['promotion_data']['free_shipping_voucher_info'] = {
# 		'free_shipping_voucher_id' : voucher['promotionid'],
# 		'free_shipping_voucher_code' : voucher['voucher_code']
# 	}
# 	break

checkout_get_data_dumped = json.dumps(checkout_get_data)

# Dat hang thong qua api
while True:
    start_time = time.time()

    cnt = 0
    while True:
        try:
            validation_error = session.post(
                "https://mall.shopee.vn/api/v4/pdp/buy_now/validate_checkout",
                data=validate_checkout,
            ).json()["data"]["validation_error"]
        except:
            print("error")
            continue
        if validation_error == 0:
            break
        cnt += 1
        print(cnt)

    place_order_data_dumped = session.post(
        "https://shopee.vn/api/v4/checkout/get", data=checkout_get_data_dumped
    ).content
    # del place_order_data['shoporders'][0]['logistics']
    # del place_order_data['shipping_orders'][0]['logistics']
    # del place_order_data['payment_channel_info']
    # place_order_data['headers'] = {
    # 	"map" : {
    # 		"set-cookie": session.cookies.get_dict()
    # 	}
    # }
    # place_order_data['promotion_data']['shop_voucher_entrances'] = [
    # 	{
    # 		"shopid": shopid,
    # 		"status": False
    # 	}
    # ]
    # place_order_data['device_info'] = {
    # 	"device_sz_fingerprint": device_sz_fingerprints[random.randint(0, 11)]
    # }
    response = session.post(
        "https://shopee.vn/api/v4/checkout/place_order", data=place_order_data_dumped
    )

    end_time = time.time()

    if "error" in response.json():
        print("Dat hang that bai!")
    else:
        print("Dat hang thanh cong!")
        print("Tong thoi gian dat hang:", end_time - start_time)

        # driver = WebDriver().driver_instance
        # driver.get("https://shopee.vn/buyer/login")
        # cookies = {}
        # for cookie in pickle.load(open(users_dir + username, "rb")):
        #     driver.add_cookie(cookie)
        # driver.get("https://shopee.vn/user/purchase/?type=9")
		
        break
