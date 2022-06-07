# Starred

Fork of [`maguowei/starred`](https://github.com/maguowei/starred)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Installation

```bash
$ pip install git+https://github.com/NiNiyas/starred
$ starred --username NiNiyas --token=xxxxxxxx --sort
```

## Usage

```
$ starred

Usage: starred [OPTIONS]

  Create an awesome list of your starred repos.

Options:
  --sort                 Sort by category[language/topic] name alphabetically.
  --topic                Categorize by topic, default is by language.
  --private              Include private repos in your list.
  --collapse             Collapsible content list.
  --username TEXT        GitHub username.  [required]
  --token TEXT           GitHub token.  [required]
  --topic_limit INTEGER  Topic limit, increase to reduce topics number. [default: 500]
  --repository TEXT      Repository name.
  --filename TEXT        Filename. [default: README.md]
  --message TEXT         Commit message. [default: Update by starred]
  --license_name TEXT    Footer license name.
  --license_badge TEXT   Footer license badge.
  --license_link TEXT    Footer license link.
  --version              Show the version and exit.
  --help                 Show this message and exit.
```

## Demo
- [`NiNiyas/awesome-stars`](https://github.com/NiNiyas/awesome-stars)

## Changes from [`maguowei/starred`](https://github.com/maguowei/starred)
- Fixed [#20](https://github.com/maguowei/starred/issues/20). Thanks to [1132719438/starred](https://github.com/1132719438/starred).
- Fixed `UnicodeEncodeError` when trying to write to a file on Windows platforms.
- Added last commit date, stars and license details.
- Added a back to top button. Thanks to [awesome-selfhosted/awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted).
- Added the ability to change footer license. Thanks to [#87](https://github.com/maguowei/starred/issues/87). For available names, badges and links, see this [gist](https://gist.github.com/lukas-h/2a5d00690736b4c3a7ba).
- Added collapsible content list. Thanks to [#47](https://github.com/maguowei/starred/issues/47).
- Changed folder structure of the project.
- Changed license from `MIT` to `GNU General Public License v3.0`.
- Updated requirements.
