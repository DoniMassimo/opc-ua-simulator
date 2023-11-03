class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print('data change')

    # def event_notification(self, event):
    #     _logger.warning("Python: New event %s", event)
