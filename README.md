
# Ansible Role:  `awscli`

Ansible role to setup aws-cli tools.


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-awscli/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-awscli)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-awscli)][releases]
[![Ansible Quality Score](https://img.shields.io/ansible/quality/50067?label=role%20quality)][quality]

[ci]: https://github.com/bodsch/ansible-awscli/actions
[issues]: https://github.com/bodsch/ansible-awscli/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-awscli/releases
[quality]: https://galaxy.ansible.com/bodsch/awscli


## Requirements & Dependencies

There are no known dependencies.

## Latest `awscli` Version

Currently there is only one old (2.0.0) release.  
But current tags can be verified at [GitHub](https://github.com/aws/aws-cli/tags).



### Operating systems

Tested on

* Arch Linux
* Artix Linux
* Debian based
    - Debian 10 / 11
    - Ubuntu 20.10
* RedHat based
    - ? CentOS 8 (**not longer supported**)
    - ? Alma Linux 8
    - ? Rocky Linux 8
    - ? Oracle Linux 8

## usage


```yaml
awscli_version: 2.2.33

awscli_download_url: "https://awscli.amazonaws.com/awscli-exe-linux-x86_64{{ '' if awscli_version == 'latest' else '-' + awscli_version }}.zip"
awscli_archiv: "aws-cli{{ '' if awscli_version == 'latest' else '-' + awscli_version }}.zip"

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

If you want to use something stable, please use a [Tagged Version](https://gitlab.com/bodsch/ansible-awscli/-/tags)!


## Author

- Bodo Schulz

## License

[Apache](LICENSE)

`FREE SOFTWARE, HELL YEAH!`
