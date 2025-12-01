#!/usr/bin/python3
# -*- coding: utf-8 -*-

# (c) 2021-2025, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import absolute_import, division, print_function

import re

from ansible.module_utils.basic import AnsibleModule


class AwsCliVersion(object):
    """
    """

    module = None

    def __init__(self, module):
        """
        Initialize all needed Variables
        """
        self.module = module

        self.validate_version = module.params.get("validate_version")
        self.excutable = module.params.get("excutable")
        if self.excutable:
            self.awscli = module.get_bin_path(self.excutable, False)
        else:
            self.awscli = module.get_bin_path("aws", False)

    def run(self):
        """
        """
        result = dict(rc=127, failed=True, changed=False, full_version="unknown")

        if not self.awscli:
            return dict(rc=2, failed=False, changed=False, msg="no awscli installed")

        rc, out, err = self._exec(["--version"])

        if rc == 0:
            _failed = False
            msg = ""

            pattern = re.compile(
                r"^aws-cli\/(?P<version>(?P<major>\d+).(?P<minor>\d+).(?P<patch>\*|\d+)).*"
            )
            version = re.search(pattern, out)
            if version:
                version_full_string = version.group("version")
                version_major_string = version.group("major")
                version_minor_string = version.group("minor")
                version_patch_string = version.group("patch")

            if self.validate_version:
                if version_full_string == self.validate_version:
                    _failed = False
                    msg = f"version {self.validate_version} successful installed."
                else:
                    _failed = True
                    msg = f"version {self.validate_version} not installed."

            result = dict(
                failed=_failed,
                rc=0,
                msg=msg,
                full_version=version_full_string,
                version=dict(
                    major=int(version_major_string),
                    minor=int(version_minor_string),
                    patch=int(version_patch_string),
                ),
                excutable=self.awscli,
            )

        return result

    def _exec(self, args):
        """ """
        cmd = [self.awscli] + args

        rc, out, err = self.module.run_command(cmd, check_rc=True)
        # self.module.log(msg="  rc : '{}'".format(rc))
        # self.module.log(msg="  out: '{}' ({})".format(out, type(out)))
        # self.module.log(msg="  err: '{}'".format(err))
        return rc, out, err


def main():

    module = AnsibleModule(
        argument_spec=dict(
            validate_version=dict(required=False, type="str"),
            excutable=dict(required=False, type="str"),
        ),
        supports_check_mode=True,
    )

    aws = AwsCliVersion(module)
    result = aws.run()

    module.log(f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == "__main__":
    main()
