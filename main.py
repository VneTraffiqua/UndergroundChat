import asyncio
import aiofiles
import datetime
import argparse


async def main():
    reader, writer = await asyncio.open_connection(host='minechat.dvmn.org', port='5000')

    while True:
        line = await reader.readline()
        chat_with_time = datetime.datetime.now().strftime('%Y-%m-%d | %H.%M.%S || ') + line.decode("utf-8")
        print(chat_with_time)
        async with aiofiles.open(file='chat.txt', mode='a') as file:
            await file.write(chat_with_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='UndergroundChat',
        description='Chat',
        add_help=True
    )

    parser.add_argument('-ht', '--host', type=str, default='minechat.dvmn.org', help='Connection host used')
    parser.add_argument('-pt', '--port', type=int, default=5000, help='Connection port used')
    parser.add_argument('-p', '--path', type=str, default='./', help='Path to the saved chat history')
    args = parser.parse_args()

    asyncio.run(main())
