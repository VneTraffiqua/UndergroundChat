import asyncio
import aiofiles
import datetime
import argparse
from environs import Env


async def main(host, port, file_path):
    reader, writer = await asyncio.open_connection(host=host, port=port)

    while True:
        line = await reader.readline()
        chat_with_time = datetime.datetime.now().strftime('%Y-%m-%d | %H.%M.%S || ') + line.decode("utf-8")
        print(chat_with_time)
        async with aiofiles.open(file=file_path, mode='a') as file:
            await file.write(chat_with_time)

if __name__ == '__main__':
    env = Env()
    env.read_env()

    HOST = env.str('HOST')
    PORT = env.str('CHAT_PORT')
    FILE_PATH = env.str('FILE_PATH')

    parser = argparse.ArgumentParser(
        prog='UndergroundChat',
        description='Chat',
        add_help=True
    )

    parser.add_argument('-ht', '--host', type=str, default=HOST, help='Connection host used')
    parser.add_argument('-pt', '--port', type=int, default=PORT, help='Connection port used')
    parser.add_argument('-p', '--path', type=str, default=FILE_PATH, help='Path to the file saved chat history')
    args = parser.parse_args()

    asyncio.run(main(host=args.host, port=args.port, file_path=args.path))
