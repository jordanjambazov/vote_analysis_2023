import requests
from time import sleep

def download_file(number):
    formatted_number = f'{number:04}'
    url = f'https://results.cik.bg/mi2023/tur1/protokoli/1/{formatted_number}/ik.html'
    
    headers = {
        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        "Accept-Language": "en",
        "Cache-Control": "no-cache",
        "Cookie": "__utmc=162382894; __utma=162382894.1341936597.1695854798.1698445891.1698794737.3; __utmz=162382894.1698794737.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)",
        "Pragma": "no-cache",
        "Sec-Ch-Ua":  '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        "Sec-Ch-Ua-Mobile": '?0',
        "Sec-Ch-Ua-Platform": "macOS",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": 'none',
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": '1',
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    response = requests.head(url, headers=headers)

    if response.status_code != 404:
        # Downloading the content
        content_response = requests.get(url, headers=headers)
        if content_response.status_code == 200:
            file_name = f'raw/1_{formatted_number}_ik.html'
            with open(file_name, 'wb') as file:
                file.write(content_response.content)
            print(f'Downloaded: {file_name}')
        else:
            print(f'Error accessing: {url} {content_response.status_code} {content_response.text}')
            breakpoint()
            pass
    else:
        print(f'Not found: {url}')

for i in range(100, 10000):
    download_file(i)
    sleep(0.1)  # Sleep for 100 milliseconds to be gentle on the server
