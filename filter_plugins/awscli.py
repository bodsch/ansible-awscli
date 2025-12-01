# python 3 headers, required if submitting to Ansible

from __future__ import absolute_import, print_function

__metaclass__ = type

from ansible.utils.display import Display

# from packaging.version import parse as parseVersion

display = Display()


class FilterModule(object):
    """ """

    def filters(self):
        return {
            # "awscli_version": self.awscli_version,
            "report": self.report,
        }

    # def awscli_version(self, data):
    #     """ """
    #     versions = []
    #
    #     if isinstance(data, list):
    #         """ """
    #         for x in data:
    #             versions.append(x.get("name", None))
    #
    #     versions = self.__version_sort(versions)
    #
    #     # display.v(f"= versions: {versions}")
    #
    #     return versions

    def report(self, data):
        """ """
        result = []

        if isinstance(data, list):
            # display.v(f"data: {data}")
            result = [
                f"{x.get('dest')} changed" for x in data if x.get("changed", False)
            ]

        return result

    # def __version_sort(self, versions_list):
    #     """ """
    #     versions_list.sort(key=parseVersion)
    #
    #     return versions_list
