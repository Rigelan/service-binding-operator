import re

from command import Command


class Namespace():
    def __init__(self, name):
        self.name = name
        self.cmd = Command()

    def create(self):
        create_namespace_output, exit_code = self.cmd.run("oc new-project {}".format(self.name))
        if re.search(r'Now using project \"%s\"\son\sserver' % self.name, create_namespace_output) or \
                re.search(r'.*Already\son\sproject\s\"%s\"\son\sserver.*' % self.name, create_namespace_output):
            return True
        elif re.search(r'.*project.project.openshift.io\s\"%s\"\salready exists' % self.name, create_namespace_output):
            return self.switch_to()
        else:
            print("Returned a different value {}".format(create_namespace_output))
        return False

    def is_present(self):
        output, exit_code = self.cmd.run('oc get ns {}'.format(self.name))
        return exit_code == 0

    def switch_to(self):
        create_namespace_output, exit_code = self.cmd.run('oc project {}'.format(self.name))
        if re.search(r'Now using project \"%s\"\son\sserver' % self.name, create_namespace_output):
            return True
        elif re.search(r'.*Already\son\sproject\s\"%s\"\son\sserver.*' % self.name, create_namespace_output):
            return True
        else:
            return False
