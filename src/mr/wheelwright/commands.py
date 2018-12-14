import subprocess
import os
import sys
try:
    import queue
except ImportError:
    import Queue as queue
from mr.developer.commands import Command
from mr.developer.common import WorkingCopies
from zc.buildout.buildout import Buildout


def make_buildout(config):
    buildout = Buildout(config.buildout_settings['config_file'],
                        config.buildout_options,
                        config.buildout_settings['user_defaults'],
                        config.buildout_settings['windows_restart'])
    return buildout


class CmdBuildWheels(Command):
    def __init__(self, develop):
        super(CmdBuildWheels, self).__init__(develop)
        description = "build wheels"
        self.parser = self.develop.parsers.add_parser(
            "wheels",
            description=description)
        self.parser.add_argument(
            "package-regexp", nargs="+",
            help="A regular expression to match package names.")
        self.parser.set_defaults(func=self)

    def __call__(self, args):
        versions = make_buildout(self.develop.config).get('versions', {})
        packages = self.get_packages(getattr(args, 'package-regexp'))
        try:
            workingcopies = self.get_workingcopies(self.develop.sources)
            wwc = WheelWorkingCopies(workingcopies)
            wwc.build_wheel(sorted(packages), versions=versions)
        except (ValueError, KeyError):
            logger.error(sys.exc_info()[1])
            sys.exit(1)


class WheelWorkingCopies(object):

    def __init__(self, workingcopies):
        self.workingcopies = workingcopies

    def build_wheel(self, packages, **kwargs):
        versions = kwargs.get('versions', {})
        the_queue = queue.Queue()
        for name in packages:
            if name not in self.workingcopies.sources:
                logger.error("wheels failed. no source defined for '%s'." % name)
                sys.exit(1)
            if name not in versions:
                logger.error("wheels failed. no version defined for '%s'." % name)
                sys.exit(1)
            source = self.workingcopies.sources[name]
            if not source.exists():
                print "The package [%s] is not checked out." % source['name']
                sys.exit(1)
            wc = self.workingcopies.workingcopytypes.get(source['kind'])(source)
            wb = WheelBuilder(source, wc)
            the_queue.put_nowait((wb, wb.build, dict(version=versions[name])))
        self.workingcopies.process(the_queue)


class WheelBuilder(object):

    def __init__(self, source, wc):
        self.source = source
        self.wc = wc
        self._output = []

    def build(self, **kwargs):
        version = kwargs['version']
        self.checkout(version)
        self.bdist_wheel()

    def bdist_wheel(self):
        path = self.source['path']
        cmd = subprocess.Popen(
            [sys.executable, "setup.py", "bdist_wheel"],
            stdout=subprocess.PIPE,
            cwd=path
        )
        stdout, stderr = cmd.communicate()
        if cmd.returncode != 0:
            print "Bad bdist_wheel"
            print stdout, stderr
    
    def checkout(self, version):
        path = self.source['path']
        kind = self.source['kind']
        if self.source['kind'] != "git":
            print "Unsupported wc type [%s]." % kind
        cmd = self.wc.run_git(['checkout', version], cwd=path)
        stdout, stderr = cmd.communicate()
        if cmd.returncode != 0:
            print "Bad checkout"
            print stdout, stderr

