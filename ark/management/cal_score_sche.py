# -*- coding: utf-8
import os
import time

from flask.ext.script import Command

from ark.exts import db
from ark.account.models import Account
from ark.goal.models import Goal


class ScoreSaver(object):

    def __init__(self):
        self.interval = 10

    def refresh_account_score(self):
        all_accounts = Account.query.filter(
            Account.state=='normal', Account.is_ban==False).all()
        for each in all_accounts:
            each.score = each.cal_score()
            db.session.add(each)
            print 'Saved Account %s (%s), Score: %s' % (
                each.username, each.id, each.score)

    def refresh_goal_score(self):
        all_goals = Goal.query.filter(
            Goal.is_ban==False, Goal.is_deleted==False).all()
        for each in all_goals:
            each.score = each.cal_score()
            db.session.add(each)
            print 'Saved Goal %s (%s), Score: %s' % (
                each.title, each.id, each.score)

    def start(self):
        while(True):
            time.sleep(self.interval / 2)
            self.refresh_account_score()
            self.refresh_goal_score()
            db.session.commit()
            time.sleep(self.interval / 2)


class ScoreCommand(Command):

    def run(self):
        saver = ScoreSaver()
        saver.start()
