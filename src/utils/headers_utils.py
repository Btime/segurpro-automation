from src.config.configuration import AUTHORIZATION

def get_headers():
    return {
            "authority": "api.btime.io",
            "accept": "*/*",
            "accept-language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": AUTHORIZATION,
            "content-type": "application/json",
            "origin": "https://julia.btime.io",
            "projectid": "1",
            "referer": "https://julia.btime.io/",
            "requestid": "oZe9oYkM3L",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "workspace": "julia",
    }