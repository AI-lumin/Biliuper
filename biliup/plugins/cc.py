import json
import re

import requests

from ..engine.decorators import Plugin
from . import logger, fake_headers
from ..engine.download import DownloadBase


@Plugin.download(regexp=r'(?:https?://)?cc\.163\.com')
class CC(DownloadBase):
    def __init__(self, fname, url, suffix='flv'):
        super().__init__(fname, url, suffix)

    def check_stream(self):
        logger.debug(self.fname)
        rid = re.search(r"[0-9]{4,}", self.url).group(0)
        res = requests.get(
            f"https://api.cc.163.com/v1/activitylives/anchor/lives?anchor_ccid={rid}",
            timeout=5,
            headers=fake_headers
        )
        res.close()
        jsons = json.loads(res.text)
        if jsons["data"]:
            channel_id = jsons["data"][rid]["channel_id"]
            res = requests.get(
                f"https://cc.163.com/live/channel/?channelids={channel_id}",
                timeout=5,
                headers=fake_headers
            )
            res.close()
            jsons = json.loads(res.text)
            self.raw_stream_url = jsons["data"][0]["sharefile"]
            return True
