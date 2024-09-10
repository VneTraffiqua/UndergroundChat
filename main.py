import asyncio


async def main():
    reader, writer = await asyncio.open_connection(host='minechat.dvmn.org', port='5000')
    while True:
        line = await reader.readline()
        print(line.decode("utf-8"))

if __name__ == '__main__':
    asyncio.run(main())
