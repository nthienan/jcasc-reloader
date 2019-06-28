import logging
import logging.handlers
import os
import time
import pyinotify
import functools
from .reloader import reload_jcasc


class Application:
    def __init__(self, **cfg):
        self.cfg = cfg
        self.is_running = False
        self.init_logger(**self.cfg)
        self.wm = pyinotify.WatchManager()
        mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO
        self.wm.add_watch(self.cfg['jcascDir'], mask, rec=True)


    def run(self):
        self.is_running = True
        logging.info("jcasc-reloader is running...")
        try:
            jcasc_handler = functools.partial(reload_jcasc, jenkins_url=self.cfg["jenkins_url"], token=self.cfg["token"], verify=self.cfg["verify"])
            self.notifier = pyinotify.Notifier(self.wm)
            self.notifier.loop(callback=jcasc_handler)
        except pyinotify.NotifierError as err:
            logging.error('%s' % err)

    def stop(self):
        self.is_running = False
        logging.info("Stopping...")
        self.notifier.stop()
        logging.info("Stopped")

    @classmethod
    def init_logger(cls, **cfg):
        logger = logging.getLogger()
        logger.setLevel(cfg['logging']['level'])
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if 'logging' in cfg and 'file' in cfg['logging'] and 'path' in cfg['logging']['file']:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=cfg['logging']['file']['path'],
                maxBytes=cfg['logging']['file']['maxbytes'],
                backupCount=cfg['logging']['file']['backupCount'])
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
