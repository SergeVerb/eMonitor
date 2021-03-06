import os
import imp
from flask import current_app
from emonitor.widget.monitorwidget import MonitorWidget
import emonitor.modules.messages


class MessageType:
    """MessageType class"""

    def __init__(self, **params):
        self.name = "prototype"
        self.params = params

    def __repr__(self):
        return "prototype"

    @staticmethod
    def getMessageTypes():
        """
        load all message types. internal types from directory 'emonitor/modules/messages/' and
        external types added to the message module variable 'exttypes'

        :return: list of message types
        """
        impl = []  # load implementations of MessageTypes with widgets

        def getName(implementation):
            return str(implementation[1])

        for f in [f for f in os.listdir('%s/emonitor/modules/messages/' % current_app.config.get('PROJECT_ROOT')) if f.endswith('.py')]:
            if not f.startswith('__'):
                cls = imp.load_source('emonitor.modules.messages.%s' % f[:-3], 'emonitor/modules/messages/%s' % f)
                if hasattr(cls, '__all__') and isinstance(getattr(cls, cls.__all__[0])(f[:-3]), MonitorWidget):
                    impl.append((f[:-3], getattr(cls, cls.__all__[0])(f[:-3])))

        for item in emonitor.modules.messages.exttypes:  # add external types
            impl.append(('message_%s' % item.name, item))
        return sorted(impl, key=getName)
