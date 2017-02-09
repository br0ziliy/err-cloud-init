# -*- coding: utf8 -*-

from errbot import BotPlugin, webhook, re_botcmd
from bottle import abort

CONFIG_TEMPLATE = {'notify': []}

class CloudInit(BotPlugin):
    """
    Err plugin to send messages to chats/users through webhooks
    """

     def configure(self, configuration):
        """
        Creates a Python dictionary object which contains all the values from our
        CONFIG_TEMPLATE and then updates that dictionary with the configuration
        received when calling the "!plugin config" command.
        """

        if configuration is not None and configuration != {}:
            config = dict(chain(CONFIG_TEMPLATE.items(),
                                configuration.items()))
        else:
            config = CONFIG_TEMPLATE
        super(CloudInit, self).configure(config)

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports
        """
        return CONFIG_TEMPLATE

    @webhook('/cloud_init/<instance_id>',raw=True)
    def cloud_init(self, request, instance_id):
        self.log.info("Instace {} is calling home...".format(instance_id))
        host = request.forms.get('hostname', instance_id)
        message = "Yay, {} reports itself ready!".format(host)
        notify = self.config['notify']
        if len(notify) > 0:
            for dest in notify:
                self.build_identifier(dest)
                self.send(dest, message)
                return None # HTTP 200
        else:
            self.warn_admins(message)
            return None # HTTP 200
        abort('500', 'Internal Server Error')

