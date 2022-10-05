# python 3 headers, required if submitting to Ansible

from __future__ import (absolute_import, print_function)
__metaclass__ = type

from packaging.version import parse as parseVersion

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'awscli_version': self.awscli_version,
        }

    def awscli_version(self, data):
        """
        """
        versions = []

        if isinstance(data, list):
            """
            """
            for x in data:
                versions.append(x.get('name', None))

        versions = self.__version_sort(versions)

        # display.v(f"= versions: {versions}")

        return versions

    def __version_sort(self, versions_list):
        """
        """
        versions_list.sort(key = parseVersion)

        return versions_list
