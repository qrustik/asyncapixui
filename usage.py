import asyncio
import random
import string
from datetime import datetime, timedelta
from logging import DEBUG, getLogger, basicConfig
from uuid import uuid4

from asycnapixui import Client, ExpiryTime
from asycnapixui import Api


def ran_gen(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


async def main():
    async with Api(url="https://example.com:port/path/", login="admin", password="admin", token="") as api:
        await api.post_login()
        inbounds = await api.get_inbounds()
        clients = []
        inbound_id = inbounds[1].id
        print(await api.get_inbound(inbound_id))
        for i in range(1):
            key = str(uuid4())
            clients.append(Client(id=key, email=ran_gen(5), subId=key))
        await api.post_add_client_inbound(clients, inbound_id)
        for client in clients:
            client_traffic = await api.get_client_traffics(email=client.email)
            print(client_traffic)
            client.enable = True
            client.expiryTime = ExpiryTime(date=datetime.now() + timedelta(days=10)).expiryTime
            res = await api.post_update_client(client, inbound_id, client.id)
            print(res)


logger = getLogger()
basicConfig(level=DEBUG, format='%(asctime)s : %(levelname)s:%(name)s : %(funcName)s:%(message)s')


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())