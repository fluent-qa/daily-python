DEFAULT_HEADERS = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://www.bilibili.com',
    'priority': 'u=1, i',
    'referer': 'https://www.bilibili.com/video/BV1Qb421Y7SV/?vd_source=c668c05f4b5039b3290cec826cf03f14',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}

DEFAULT_COOKIES = {
    'buvid3': '0C25C8A6-EA71-F822-F8E0-D989C2DE341079944infoc',
    # 'b_nut': '1740392079',
    # '_uuid': '9CDA82F10-3A85-696B-12EF-F7B110DFAF731080098infoc',
    # 'enable_web_push': 'DISABLE',
    # 'enable_feed_channel': 'DISABLE',
    # 'buvid4': '7B80DD12-10E3-9840-42AC-D6AF2434DC8A80488-025022410-CvOVun1%2BX15dfH4%2ByQODmg%3D%3D',
    # 'rpdid': '|(J~lkk|kkk|0J\'u~R|Jmku)l',
    # 'header_theme_version': 'CLOSE',
    # 'hit-dyn-v2': '1',
    # 'fingerprint': '26b9a5c72e7e719ce17094db143e7b87',
    # 'buvid_fp_plain': 'undefined',
    # 'buvid_fp': 'c1c5a9ace7d054c6d980668a8287e8ec',
    # 'b_lsid': '982F4621_195418713FC',
    # 'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDA4MjAzMzQsImlhdCI6MTc0MDU2MTA3NCwicGx0IjotMX0.kSm556YWR09NRAVgoilHdFMr19tpUlNe7IkIiyhCA3c',
    # 'bili_ticket_expires': '1740820274',
    # 'bp_t_offset_608721975': '1038191353193824256',
    'SESSDATA': 'ca456f57%2C1756113344%2C6b3cf*22CjDoIx2OyeG8Wt8dbXVwBEAYdEe5EEUviWR90Z6QtwR9ag0uEFL-uTOTZl8vhIbUaXQSVklwb1pyTXRQaERLY3NVSlVJR2hBTGR6TGpVUVJSY3NYTXJISnV5U3ZmQkkzQlRvU3liWTBVY1hqWWczcXQ2SXN3aVdUbDV1bmpzV01vdWs5MG53d3Z3IIEC',
    'bili_jct': '38028b3b1efc816095eba45955763581',
    # 'DedeUserID': '3546803955829068',
    # 'DedeUserID__ckMd5': '9ceb6008f1060048',
    # 'sid': '6stk7ud6',
    # 'home_feed_column': '4',
    # 'browser_resolution': '150-895',
    # 'CURRENT_FNVAL': '4048'
}

view_url = 'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
wbi_url = 'https://api.bilibili.com/x/player/wbi/v2'