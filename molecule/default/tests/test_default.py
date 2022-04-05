
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
import pytest
import os
import testinfra.utils.ansible_runner

import pprint
pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def base_directory():
    cwd = os.getcwd()

    if('group_vars' in os.listdir(cwd)):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = "molecule/{}".format(os.environ.get('MOLECULE_SCENARIO_NAME'))

    return directory, molecule_directory


@pytest.fixture()
def get_vars(host):
    """

    """
    base_dir, molecule_dir = base_directory()

    file_defaults = "file={}/defaults/main.yml name=role_defaults".format(base_dir)
    file_vars = "file={}/vars/main.yml name=role_vars".format(base_dir)
    file_molecule = "file={}/group_vars/all/vars.yml name=test_vars".format(molecule_dir)

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


@pytest.mark.parametrize("files", [
    "/usr/local/bin/aws",
    "/usr/local/bin/aws_completer",
    "/usr/local/aws-cli/v2/current/bin/aws",
    "/usr/local/aws-cli/v2/current/bin/aws_completer"
])
def test_files(host, files):

    d = host.file(files)
    assert d.is_file


@pytest.mark.parametrize("dirs", [
    "/usr/local/aws-cli",
    "/usr/local/aws-cli/v2/current/bin",
    "/usr/local/aws-cli/v2/current/dist"
])
def test_directories(host, dirs):

    d = host.file(dirs)
    assert d.is_directory


def test_user_configs(host, get_vars):
    """
    """
    users = get_vars.get('awscli_users')

    for u, values in users.items():
        """
        """
        aws_profiles = values.get("profiles", {})

        if len(aws_profiles) > 0:
            """
            """
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
