import asyncio
import argparse
import logging
import aiofiles
import json
from environs import Env

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO,
    filename=u'underground_chat_log.log'
)

async def registration(host, port, nickname):
    reader, writer = await asyncio.open_connection(host=host, port=port)
    await reader.readline()
    writer.write('\n'.encode())
    await reader.readline()
    writer.write(f'{nickname}\n'.encode())
    data = await reader.readline()
    response = json.loads(data.decode())
    async with aiofiles.open(file='account_hash.txt', mode='w') as file:
        await file.write(response['account_hash'])
        logging.info(msg=f'create hash - {response["account_hash"]}')
    writer.close()
    await writer.wait_closed()

async def main(host, port, token, message):
    reader, writer = await asyncio.open_connection(host=host, port=port)
    data = await reader.readline()
    logging.info(msg=f'{data.decode()}')
    writer.write(f'{token}\n'.encode())
    data = await reader.readline()
    response = json.loads(data.decode())
    if response:
        logging.info(msg=f'{data.decode()}')
        writer.write(f'{message}\n\n'.encode())
        logging.info(msg=f'Sent message: "{message}"')
    else:
        logging.critical(msg=f'{token} - неизвестный токен. Проверьте его или зарегистрируйте заново.')
    await writer.drain()
    logging.info(msg=f'Close the connection')
    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':
    env = Env()
    env.read_env()

    HOST = env.str('HOST')
    PORT = env.str('WRITER_PORT')
    TOKEN = env.str('TOKEN')

    parser = argparse.ArgumentParser(
        prog='UndergroundChat',
        description='Chat',
        add_help=True
    )
    parser.add_argument('your_message', type=str, help='Your message')
    parser.add_argument('-ht', '--host', type=str, default=HOST, help='Connection host used')
    parser.add_argument('-pt', '--port', type=int, default=PORT, help='Connection port used')
    parser.add_argument('-t', '--token', type=str, default=TOKEN, help='Your personal hash')

    args = parser.parse_args()

    # asyncio.run(main(host=args.host, port=args.port, token=args.token, message=args.your_message))
    asyncio.run(registration(host=args.host, port=args.port, nickname='akooola'))
