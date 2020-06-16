import asyncio
import json
import re
import aiohttp


async def get_token(session):
    url = "https://upload-ugc.bz.mgtv.com/upload/image/getStsToken"

    querystring = {
        "uuid": "2c9ce736a2694b5b8dd4cf309b677a2f",
        "ticket": "BRAEK1IU3DU717N47ANG",
        "biz": "1",
        "num": "1",
        "callback": "jQuery182005832266842939937_1591011852911",
        "_support": "10000000",
        "_": "1591011884333",
    }

    headers = {
        "authority": "upload-ugc.bz.mgtv.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "accept": "*/*",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-dest": "script",
        "referer": "https://www.mgtv.com/b/338408/8231766.html?fpa=se&lastp=so_result",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7",
        "cookie": "__STKUUID=56977c5b-7bb9-4dce-9bfb-4504d3b03b35; mba_deviceid=d5de0866-2126-36b1-d6bc-d81dc685a555; MQGUID=1263467303526383616; __MQGUID=1263467303526383616; pc_v6=v6; _source_=C; PLANB_FREQUENCY=XsaHekEI7nBda-UG; __random_seed=0.09710746912465718; __gads=ID=5a426adf65fcb414:T=1590069115:S=ALNI_MbjtIzVPfp7KjnKslTuXdr6aWe8yw; PM_CHKID=a344546caaf6da69; sessionid=1591011742282; mba_sessionid=f8cd99a8-42ef-7ee8-6e6f-ed46a85ab06c; beta_timer=1591011743950; id=63530547; rnd=rnd; seqid=braek1sr1q1gmk1e4egg; uuid=2c9ce736a2694b5b8dd4cf309b677a2f; vipStatus=3; wei=1a119c627f24dd8ab8bad24e573cb744; wei2=5c14DHntEgaWKDdjHc6c62QLi8HGYlktLJSLQ8abWHVGt91Nqo13SLrvaW%2B9H07trkaV3NRRBy30j1CX0NQ7kJl2JJm0ZS4ck0sVgT9EWndzBVNl4tRlOkfSh0wosk3tIXn%2BjEqTxCfBLH%2BGDPe%2Fw2Slb12JjW3xLubeJaXTE6J6bD6f9WakDdLUIG6xbkT0OqpbMqPOC4Lrhv3R0td%2B0HHSKzo; HDCN=BRAEK1IU3DU717N47ANG-248244420; mba_last_action_time=1591011860129; lastActionTime=1591011881735",
    }

    async with session.get(url, headers=headers, params=querystring) as resp:
        return await resp.text()

    # response = requests.request("GET", url, headers=headers, params=querystring)
    # return response.text


async def upload_img(item):
    async with aiohttp.ClientSession() as session:
        res = await get_token(session)

        # res = get_token()
        _str = re.search(".*?\((.*?)\);", res, re.S)
        json_res = json.loads(_str.group(1))["data"]
        accessKeyId = json_res["stsToken"]["accessKeyId"]
        accessKeySecret = json_res["stsToken"]["accessKeySecret"]
        securityToken = json_res["stsToken"]["securityToken"]
        keys = json_res["bucketInfo"]["keys"][0]

        data = {
            "accessKeyId": accessKeyId,
            "accessKeySecret": accessKeySecret,
            "securityToken": securityToken,
            "keys": keys,
        }

        async with session.post("http://localhost:3000/getsign", data=data) as resp:
            auths = await resp.json()
            # res = requests.post("http://localhost:3000/getsign", data=data).json()

            auth = auths["auth"]
            date = auths["date"]

        # img_url = data_dict["v_pic"]
        img_url = item[1].replace("\n", "")
        try:
            async with session.get(img_url, timeout=10) as resp:
                payload = await resp.read()
        except:
            print(str(item[0]) + " 失效:" + item[1])
            new_item = (
                "https://mgtv-bbqn.oss-cn-beijing.aliyuncs.com/1/2005261946330861/21340.jpeg",
                item[0],
            )
            return new_item

        # payload = requests.get(img_url).content

        # with open("./test.png", "rb") as f:
        #     payload = f.read()

        headers = {
            "connection": "keep-alive",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "x-oss-user-agent": "aliyun-sdk-js/5.2.0 Chrome 81.0.4044.122 on OS X 10.15.5 64-bit",
            "authorization": auth,
            "x-oss-date": date,
            "x-oss-security-token": securityToken,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
            "content-type": "image/jpeg",
            "accept": "*/*",
            "origin": "https://www.mgtv.com",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.mgtv.com/b/316458/3998946.html",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,la;q=0.7",
        }

        url = f"https://mgtv-bbqn.oss-cn-beijing.aliyuncs.com/{keys}.jpeg"

        # print(payload)
        # response = requests.request("PUT", url, headers=headers, data=payload)
        async with session.request("PUT", url, headers=headers, data=payload) as resp:
            res = await resp.text()
            # print(f"res: {res}")

        # data_dict["v_pic"] = url
        new_item = (url, item[0])
        return new_item


if __name__ == "__main__":
    url = "https://www.op811.com/wp-content/uploads/2020/05/sp200523224456.jpg"
    asyncio.run(upload_img(url))
