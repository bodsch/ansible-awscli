
from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------




@pytest.mark.parametrize(
    "files",
    [
        "/usr/local/bin/aws",
        "/usr/local/bin/aws_completer",
        "/usr/local/aws-cli/v2/current/bin/aws",
        "/usr/local/aws-cli/v2/current/bin/aws_completer",
    ],
)
def test_files(host, files):

    d = host.file(files)
    assert d.is_file


@pytest.mark.parametrize(
    "dirs",
    [
        "/usr/local/aws-cli",
        "/usr/local/aws-cli/v2/current/bin",
        "/usr/local/aws-cli/v2/current/dist",
    ],
)
def test_directories(host, dirs):

    d = host.file(dirs)
    assert d.is_directory


def test_user_configs(host, get_vars):
    """ """
    users = get_vars.get("awscli_users")

    for u, values in users.items():
        """ """
        aws_profiles = values.get("profiles", {})

        if len(aws_profiles) > 0:
            """ """
            home_dir = "/home/{}".format(u)

            if values.get("home"):
                home_dir = "{}/{}".format(values.get("home"), u)

            config_dir = "{}/.aws".format(home_dir)

            assert host.file(home_dir).is_directory
            assert host.file(config_dir).is_directory

            config_file = "{}/config".format(config_dir)
            credentials_file = "{}/credentials".format(config_dir)

            assert host.file(config_file).is_file
            assert host.file(credentials_file).is_file


def test_version(host, get_vars):
    """ """
    _facts = local_facts(host=host, fact="aws_cli")
    version = _facts.get("version")

    version_dir = f"/usr/local/aws-cli/v2/{version}"
    current_link = "/usr/local/aws-cli/v2/current"

    print(version_dir)

    directory = host.file(version_dir)
    assert directory.is_directory

    link = host.file(current_link)
    assert link.is_symlink
    assert link.linked_to == version_dir
