import asyncio
import sys

import aiohttp

npm_root = 'https://cdn.jsdelivr.net/npm/'
# npm_root = 'https://unpkg.com/'
# npm_root = 'https://npm.elemecdn.com/'
# npm_root = 'https://unpkg.zhimg.com/'
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
    'isplib': [
        {
            'weight': 5,
            'ver': ['0.0.15', '0.0.14', '0.0.13', '0.0.12', '0.0.11', '0.0.10', '0.0.9', '0.0.8', '0.0.8-beta', '0.0.7', '0.0.6-fix-1', '0.0.6-fix-0', '0.0.6', '0.0.5', '0.0.5-beta-fix-4', '0.0.5-beta', '0.0.4-fix-0', '0.0.4', '0.0.1'],
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
        {
            'weight': 10,
            'ver': ['latest', '0.1.0', '0.0.17', '0.0.17-beta', '0.0.17-alpha-fix-0', '0.0.16'],
            'file': [
                'loadImage.js',
                'loadImage/module.js',
                'loadImage/cacheToLocal.js',
                'loadImage/pinToCDN.js',
                'loadImage/search.js',
                'loadImage/style.css',
                'loadImage/withCache.js',
                'loadImage/withoutCache.js',
                'package.json',
            ]
        }
    ],
    'ispcdn': [
        {
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
    ]
}


def fill_list(pkg: str, ver: list, file: list, weight: int) -> list:
    res = []
    for v in ver:
        res.extend([f'{pkg}@{v}/{f}' for f in file])
    return res * weight


ping_list = []
for pkg, infos in zipped_list.items():
    for info in infos:
        if not 'weight' in info:
            info['weight'] = 1
        filled_list = fill_list(
            pkg=pkg,
            ver=info['ver'],
            file=info['file'],
            weight=info['weight'])
        ping_list.extend(filled_list)


async def fetch_all() -> None:
    conn = aiohttp.TCPConnector(limit=10)

    async def fetch(session: aiohttp.ClientSession, npm_relative_url: str) -> None:
        url = npm_root + npm_relative_url
        async with session.get(url) as r:
            if r.status == 200:
                sys.stdout.write(f'[INFO] Success: URL {url}\n')

    async with aiohttp.ClientSession(headers=header, connector=conn) as session:
        while True:
            tasks = [fetch(session, url) for url in ping_list]
            await asyncio.wait(tasks)
            await asyncio.sleep(5.0)


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(fetch_all())
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(e)
        input()


if __name__ == "__main__":
    main()
