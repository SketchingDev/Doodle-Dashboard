# coding=utf-8
from doodledashboard.lucas.handlers.handler import MessageHandler

""" Demonstration handler for MiniMaker Fayre """


class BankHandler(MessageHandler):
    def __init__(self, shelve):
        MessageHandler.__init__(self, shelve)

    def get_tag(self):
        return '#bank'

    def draw(self, display, messages):
        display.write_text('Main account', 0, 0)
        display.write_text('-£100', 0, 0)
        display.write_text('Savings account', 0, 0)
        display.write_text('£10', 0, 0)
        display.flush()
