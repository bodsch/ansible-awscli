
# Ansible Role:  `awscli`

Ansible role to setup aws-cli tools.


[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-awscli/main.yml?logo=github&branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-awscli?logo=github)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-awscli?logo=github)][releases]
[![Ansible Downloads](https://img.shields.io/ansible/role/d/bodsch/awscli?logo=ansible)][galaxy]

[ci]: https://github.com/bodsch/ansible-awscli/actions
[issues]: https://github.com/bodsch/ansible-awscli/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-awscli/releases
[galaxy]: https://galaxy.ansible.com/ui/standalone/roles/bodsch/awscli/

If `latest` is set for `awscli_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/bin/aws_${awscli_version}` and later linked to `/usr/local/bin/aws`. 
This should make it possible to downgrade relatively safely.

The AWSCLI archive is stored on the Ansible controller and is later copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/awscli`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `awscli_direct_download` to `true`.


## Requirements & Dependencies

Ansible Collections

- [bodsch.core](https://github.com/bodsch/ansible-collection-core)
- [bodsch.scm](https://github.com/bodsch/ansible-collection-scm)

```bash
ansible-galaxy collection install bodsch.core
ansible-galaxy collection install bodsch.scm
```
or
```bash
ansible-galaxy collection install --requirements-file collections.yml
```

## Latest `awscli` Version

Currently there is only one old (2.0.0) release.  
But current tags can be verified at [GitHub](https://github.com/aws/aws-cli/tags).


### Operating systems

Tested on

* Arch Linux
* Artix Linux
* Debian based
    - Debian 10 / 11 / 12
    - Ubuntu 20.10 / 22.04

> **RedHat-based systems are no longer officially supported! May work, but does not have to.**


## usage

```yaml
awscli_version: 2.2.33

awscli_download_url: "https://awscli.amazonaws.com/awscli-exe-linux-x86_64{{ '' if awscli_version == 'latest' else '-' + awscli_version }}.zip"
awscli_archiv: "aws-cli{{ '' if awscli_version == 'latest' else '-' + awscli_version }}.zip"

awscli_direct_download: false

awscli_config: "config.j2"
awscli_credentials: "credentials.j2"

awscli_users: {}
```

### AWS credentials

Support multiple credentials per user.

Every user can hold more than one profile.

Each profile, which is not `default`, gets a corresponding profile prefix.

The example below creates these config and credentials files:

```bash
cat /var/lib/jenkins/.aws/config
[default]
region = eu-central-1
output = json

[profile us-west]
region = us-west-1
output = text
```

```bash
cat /var/lib/jenkins/.aws/credentials
[default]
aws_access_key_id = molecule-aws-access-key-id
aws_secret_access_key = molecule-aws-secret-access-key

[us-west]
aws_access_key_id = molecule-aws-access-key-id_2
aws_secret_access_key = molecule-aws-secret-access-key_2
```

```yaml
awscli_users:
  jenkins:
    profiles:
      default:
        region: "eu-central-1"
        output: "json"
        access_key_id: "molecule-aws-access-key-id"
        secret_access_key: "molecule-aws-secret-access-key"
      us-west:
        region: "us-west-1"
        access_key_id: "molecule-aws-access-key-id_2"
        secret_access_key: "molecule-aws-secret-access-key_2"
    home: "/var/lib"
    group: "jenkins"
```

[Howto use AWS Named Profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-awscli/tags)!


## Author

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
