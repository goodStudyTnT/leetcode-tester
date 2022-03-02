from requests import Request, Session

host = "leetcode-cn.com"
def login(username, password):
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    with Session() as s:
        s.headers.update({"User-Agent": ua})
        csrf_token_url = f"https://{host}/graphql/"
        print(csrf_token_url)
        resp = s.post(csrf_token_url, data={
            "operationName": "GlobalData",
            "query": "query nojGlobalData {\n  siteRegion\n  chinaHost\n  websocketUrl\n}\n",
        })
        # resp.ok
        print(resp.status_code)




if __name__ == "__main__":
    login("goodstudyqaq", "woshiGS#3#")