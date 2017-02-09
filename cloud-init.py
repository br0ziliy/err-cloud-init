# -*- coding: utf8 -*-

from errbot import BotPlugin, webhook, re_botcmd
from bottle import abort

class CloudInit(BotPlugin):
    """
    Err plugin to send messages to chats/users through webhooks
    """

    def activate(self):

        super(CloudInit, self).activate()
        if not 'notify' in self.keys():
            self.log.info("Initializing 'notify' storage")
            self['notify'] = []

    @webhook('/cloud_init/<instance_id>',raw=True)
    def cloud_init(self, request, instance_id):
        self.log.info("Instace {} is calling home...".format(instance_id))
        for e in request.forms:
            self.log.debug(repr(e))
        self.log.debug(request.body)
