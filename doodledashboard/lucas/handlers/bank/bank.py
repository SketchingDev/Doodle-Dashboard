# coding=utf-8
import os
from os import path
from doodledashboard.lucas.handlers.handler import MessageHandler

""" Demonstration handler for MiniMaker Fayre """


class BankHandler(MessageHandler):
    _FONT_FILENAME = "Noteworthy.ttc"

    def __init__(self, shelve):
        MessageHandler.__init__(self, shelve)

        current_dir = self._get_current_directory()
        self._font_full_path = path.join(current_dir, BankHandler._FONT_FILENAME)

    def get_tag(self):
        return '#bank'

    def draw(self, display, messages):
        display.write_text('Bank Accounts', 5, -15, 43, self._font_full_path)
        display.write_text(u'Main: \u00A312', 50, 50, 38, self._font_full_path)
        display.write_text(u"Savings: \u00A353", 10, 100, 38, self._font_full_path)
        display.flush()

    def _get_current_directory(self):
        return os.path.dirname(os.path.realpath(__file__))