import asyncio
import sys

import aiohttp

npm_root = 'https://cdn.jsdelivr.net/npm/'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'dnt': '1',
    'accept': '*/*',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'script',
    'referer': 'https://www.isab.top/tools/deqrcode.php',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

zipped_list = {
    'isplib': {
        'ver': [
            'latest',
            '0.0.6-fix-0',
            '0.0.6',
            '0.0.5',
            '0.0.5-beta-fix-4',
            '0.0.5-beta',
            '0.0.4-fix-0',
            '0.0.4',
            '0.0.1',
        ],
        'file': [
            'loadBackground.js',
            'loadBackground/module.js',
            'loadBackground/pinToCDN.js',
            'loadBackground/search.js',
            'loadBackground/style.css',
            'loadBackground/withCache.js',
            'loadBackground/withoutCache.js',
            'package.json',
            'README.md'
        ]
    },
    'ispcdn': {
        'ver': [
            'latest',
            '0.0.2',
            '0.0.1',
            '0.0.0-fix-1'
        ],
        'file': [
            'imgList.json',
            'package.json',
            'README.md'
        ]
    }
}


def fill_list(pkg: str, ver: list, file: list) -> list:
    res = []
    for v in ver:
        res.extend([f'{pkg}@{v}/{f}' for f in file])
    return res


ping_list = []
for pkg, info in zipped_list.items():
    ping_list.extend(fill_list(pkg, info['ver'], info['file']))


async def fetch(session: aiohttp.ClientSession, npm_relative_url: str) -> None:
    url = npm_root + npm_relative_url
    async with session.get(url) as r:
        if r.status == 200:
            sys.stdout.write(f'[INFO] Success: URL {url}\n')
        else:
            sys.stdout.write(f'[ERROR] Failure: URL {url}\n')


async def fetch_all() -> None:
    async with aiohttp.ClientSession(headers=header) as session:
        tasks = [fetch(session, url) for url in ping_list]
        await asyncio.wait(tasks)


def main():
    loop = asyncio.get_event_loop()
    try:
        while True:
            loop.run_until_complete(fetch_all())
            loop.run_until_complete(asyncio.sleep(5.0))
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
