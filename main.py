import asyncio
import aiofiles
import datetime


async def main():
    reader, writer = await asyncio.open_connection(host='minechat.dvmn.org', port='5000')

    while True:
        line = await reader.readline()
        chat_with_time = datetime.datetime.now().strftime('%Y-%m-%d | %H.%M.%S || ') + line.decode("utf-8")
        print(chat_with_time)
        async with aiofiles.open(file='chat.txt', mode='a') as file:
            await file.write(chat_with_time)

if __name__ == '__main__':
    asyncio.run(main())
