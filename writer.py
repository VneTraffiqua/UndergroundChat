import asyncio
import argparse
import logging
from environs import Env

logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO,
    filename=u'underground_chat_log.log'
)

async def main(host, port, token, message):
    reader, writer = await asyncio.open_connection(host=host, port=port)
    sent_messages = [token, message]
    for message in sent_messages:
        data = await reader.readline()
        logging.info(msg=f'{data.decode()}')
        writer.write(f'{message}\n\n'.encode())
        logging.info(msg=f'Sent: {message}')
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

    asyncio.run(main(host=args.host, port=args.port, token=args.token, message=args.your_message))
