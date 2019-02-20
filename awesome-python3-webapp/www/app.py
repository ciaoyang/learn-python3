import logging;logging.basicConfig(level=logging.INFO)
import asyncio,os,json,time
from datetime import datetime
from aiohttp import web
import aiomysql

def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')

@asyncio.coroutine
def init(loop):
    app=web.Application(loop=loop)
    app.router.add_route('GET','/',index)
    srv=yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
    logging.info('server starter at http://127.0.0.1:9000...')
    return srv

loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()


# 创建连接池，使其不必频繁打开和关闭数据库链接，尽量复用
@asyncio.coroutine
def create_pool(loop,**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool=yield from aiomysql.create_pool(
        host=kw.get('host','localhost'),
        port=kw.get('port',3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utr-8'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.ger('minsize',1),
        loop=loop
    )


