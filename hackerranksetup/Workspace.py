# coding=utf-8
from hackerranksetup import Readme, Challenge


class Workspace(object):
    def __init__(self, root, workspace, assets):
        self.root = root
        self.workspace = workspace
        self.assets = assets

    def new(self, url):
        challenge = Challenge.Challenge(url)
        readme = Readme.Readme(challenge, self.workspace, self.assets)
        readme.save()

    def publish(self):
        pass
