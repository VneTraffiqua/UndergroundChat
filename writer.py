import asyncio
import argparse
import logging
import aiofiles
import json
from environs import Env
from contextlib import asynccontextmanager

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO,
    filename='underground_chat_log.log'
)

@asynccontextmanager
async def connection_manager(host, port):
    reader, writer = await asyncio.open_connection(host=host, port=port)
    try:
        yield reader, writer
    finally:
        writer.close()
        await writer.wait_closed()

async def submit_message(writer, message):
    message = message.replace('\n', '').strip()
    writer.write(f'{message}\n\n'.encode())
    logging.info(msg=f'Sent message: "{message}"')

async def registration(host, port, nickname):
    async with connection_manager(host, port) as (reader, writer):
        await reader.readline()
        writer.write('\n'.encode())
        await reader.readline()
        nickname = nickname.replace('\n', '').strip()
        writer.write(f'{nickname}\n'.encode())
        data = await reader.readline()
        response = json.loads(data.decode())
        async with aiofiles.open(file='.env', mode='a') as file:
            await file.write(f'\nTOKEN={response["account_hash"]}')
            logging.info(msg=f'create account hash - {response["account_hash"]} in .env file')
        writer.close()
        await writer.wait_closed()

async def authorise(host, port, token, message):
    async with connection_manager(host, port) as (reader, writer):
        data = await reader.readline()
        logging.info(msg=f'{data.decode()}')
        writer.write(f'{token}\n'.encode())
        data = await reader.readline()
        response = json.loads(data.decode())
        if response:
            logging.info(msg=f'{data.decode()}')
            await submit_message(writer, message)
        else:
            logging.critical(msg=f'{token} - неизвестный токен. Проверьте его или зарегистрируйте заново.')
        await writer.drain()
        logging.info(msg=f'Close the connection')
        writer.close()
        await writer.wait_closed()

if __name__ == '__main__':
    env = Env()
    env.read_env()

    connection_host = env.str('HOST')
    connection_port = env.str('WRITER_PORT')
    connection_token = env.str('TOKEN')

    parser = argparse.ArgumentParser(
        prog='UndergroundChat',
        description='Chat',
        add_help=True
    )
    parser.add_argument('your_message', type=str, help='Your message')
    parser.add_argument('-ht', '--host', type=str, default=connection_host, help='Connection host used')
    parser.add_argument('-pt', '--port', type=int, default=connection_port, help='Connection port used')
    parser.add_argument('-t', '--token', type=str, default=connection_token, help='Your personal hash')
    parser.add_argument('-n', '--nickname', type=str, default='Anonymous', help='Your nickname in chat')

    args = parser.parse_args()
    if connection_token:
        asyncio.run(authorise(host=args.host, port=args.port, token=args.token, message=args.your_message))
    else:
        asyncio.run(registration(host=args.host, port=args.port, nickname=args.nickname))
