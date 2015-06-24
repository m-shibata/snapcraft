# -*- Mode:Python; indent-tabs-mode:t; tab-width:4 -*-

import os
import snapcraft
import sys

class AutotoolsHandler(snapcraft.BaseHandler):
	def __init__(self, name, options):
		super().__init__(name, options)
		if self.options.configflags is None:
			self.options.configflags = ''
	def pull(self):
		self.pullBranch(self.options.source)
	def build(self):
		if not os.path.exists(os.path.join(self.builddir, "configure")):
			self.run("env NOCONFIGURE=1 ./autogen.sh")
		self.run("./configure --prefix= " + self.options.configflags)
		self.run("make all")
	def stage(self):
		self.run("make install DESTDIR=" + self.stagedir)
	def deploy(self):
		self.doDeploy(["bin", "share", "lib"]) # not "include"
	def test(self):
		self.run("make check")


if __name__ == "__main__":
	class Options:
		source = "git://git.sv.gnu.org/readline.git"
		configflags = ""
	handler = AutotoolsHandler("readline", Options())
	getattr(handler, sys.argv[1])()