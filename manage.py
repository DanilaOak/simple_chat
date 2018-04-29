import logging

from aiohttp import web
from aio_manager import Manager, Command
from aio_manager.commands.runserver import RunServer as BaseRunServer

from chat.app import create_app

app = create_app()
manager = Manager(app)


class RunServer(BaseRunServer):
    def run(self, app, args):
        logging.basicConfig(level=args.level)
        logging.getLogger().setLevel(args.level)
        web.run_app(app, host=args.hostname, port=5004, access_log=None)


manager.add_command(RunServer(app))


if __name__ == '__main__':
    manager.run()
