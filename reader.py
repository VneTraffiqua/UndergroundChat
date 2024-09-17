import asyncio
import aiofiles
import datetime
import argparse
from contextlib import asynccontextmanager
from environs import Env


@asynccontextmanager
async def connection_manager(host, port):
    reader, writer = await asyncio.open_connection(host=host, port=port)
    try:
        yield reader, writer
    finally:
        writer.close()
        await writer.wait_closed()

async def main(host, port, file_path):
    async with connection_manager(host, port) as (reader, writer):
        while True:
            line = await reader.readline()
            chat_with_time = datetime.datetime.now().strftime('%Y-%m-%d | %H.%M.%S || ') + line.decode("utf-8")
            print(chat_with_time)
            async with aiofiles.open(file=file_path, mode='a') as file:
                await file.write(chat_with_time)

if __name__ == '__main__':
    env = Env()
    env.read_env()

    connection_host = env.str('HOST')
    connection_port = env.str('CHAT_PORT')
    output_file = env.str('FILE_PATH')

    parser = argparse.ArgumentParser(
        prog='UndergroundChat',
        description='Chat',
        add_help=True
    )

    parser.add_argument('-ht', '--host', type=str, default=connection_host, help='Connection host used')
    parser.add_argument('-pt', '--port', type=int, default=connection_port, help='Connection port used')
    parser.add_argument('-p', '--path', type=str, default=output_file, help='Path to the file saved chat history')
    args = parser.parse_args()

    asyncio.run(main(host=args.host, port=args.port, file_path=args.path))
