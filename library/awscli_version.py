#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2021, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import absolute_import, division, print_function
import re

from ansible.module_utils.basic import AnsibleModule


class AwsCliVersion(object):
    """
      Main Class
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self.awscli = module.get_bin_path('aws', False)

    def run(self):
        """
          runner
        """
        result = dict(
            rc=127,
            failed=True,
            changed=False,
            full_version = "unknown"
        )

        if not self.awscli:
            result["msg"] = "no awscli installed"
            return result

        rc, out, err = self._exec(['--version'])

        if rc == 0:
            pattern = re.compile(r"^aws-cli\/(?P<version>(?P<major>\d+).(?P<minor>\d+).(?P<patch>\*|\d+)).*")
            version = re.search(pattern, out)
            if version:
                version_full_string = version.group('version')
                version_major_string = version.group("major")
                version_minor_string = version.group("minor")
                version_patch_string = version.group("patch")

            result = dict(
                failed = False,
                rc = 0,
                full_version = version_full_string,
                version = dict(
                    major = int(version_major_string),
                    minor = int(version_minor_string),
                    patch = int(version_patch_string)
                ),
                excutable = self.awscli
            )

        return result

    def _exec(self, args):
        '''   '''
        cmd = [self.awscli] + args

        rc, out, err = self.module.run_command(cmd, check_rc=True)
        # self.module.log(msg="  rc : '{}'".format(rc))
        # self.module.log(msg="  out: '{}' ({})".format(out, type(out)))
        # self.module.log(msg="  err: '{}'".format(err))
        return rc, out, err


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
        ),
        supports_check_mode=True,
    )

    icinga = AwsCliVersion(module)
    result = icinga.run()

    module.log(msg="= result: {}".format(result))

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
