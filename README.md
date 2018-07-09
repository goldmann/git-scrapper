# Git scrapper utility

This tool was cretated to generate reports based on commits to Git
repositories.

## Configuration file

You need to prepare a configuration file in YAML format. Example
configuration file can be found below:

```yaml
name: Marek Goldmann
repos:
  - https://github.com/jboss-container-images/redhat-sso-7-openshift-image.git
  - https://github.com/jboss-container-images/redhat-sso-7-image.git
emails:
  - EMAIL@gmail.com
  - SECOND_EMAIL@gmail.com
```

All keys are required.

## Installation

```
$ dnf -y install git python python2-pip cairo pango
$ pip install -U --user -r requirements.txt
```

## Usage

```
$ python scrapper.py --help
usage: scrapper.py [-h] --config CONFIG --after AFTER --before BEFORE
                   [--pdf PDF] [--csv CSV]

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Path to configuration file
  --after AFTER    Start date in format: 2017-12-20
  --before BEFORE  End date in format: 2017-12-20
  --pdf PDF        Path where the generated PDF is saved, default is
                   report.pdf in current directory
  --csv CSV        Path where the generated CSV is saved, default is
                   report.csv in current directory
```

Example:


```
$ python scrapper.py --config config.yml --after 2018-01-01 --before 2018-07-01 --pdf report.pdf
```
