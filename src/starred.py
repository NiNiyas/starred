#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import sys
from io import BytesIO
from collections import OrderedDict
import click
from github3 import GitHub
from github3.exceptions import NotFoundError
from .githubgql import GitHubGQL
from . import VERSION

DEFAULT_CATEGORY = 'Others'
TEXT_LENGTH_LIMIT = 200

desc = '''<!--lint disable awesome-contributing awesome-license awesome-list-item match-punctuation no-repeat-punctuation no-undefined-references awesome-spell-check-->
# Awesome Stars [![Awesome](https://awesome.re/badge.svg)](https://github.com/sindresorhus/awesome)

> A curated list of my GitHub stars! Generated using [starred](https://github.com/NiNiyas/starred).

## Contents
'''

license_ = '''
## License

[![{license_name}]({license_badge})]({license_link})

To the extent possible under law, [{username}](https://github.com/{username})\
 has waived all copyright and related or neighboring rights to this work.
'''

html_escape_table = {
    ">": "&gt;",
    "<": "&lt;",
}


def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c, c) for c in text)


def title2url(title):
    """Markdown title to url"""
    table = str.maketrans('', '', '~`!@#$%^&*()+=[]{}:;\'"<>,.?/\\|')

    title_url = '-'.join(title.lower().split())
    return title_url.translate(table)


@click.command(no_args_is_help=True)
@click.option('--sort', is_flag=True, show_default=True, help='Sort by category[language/topic] name alphabetically.')
@click.option('--topic', is_flag=True, show_default=True, help='Categorize by topic, default is by language.')
@click.option('--private', is_flag=True, default=False, show_default=True, help='Include private repos in your list.')
@click.option('--collapse', is_flag=True, show_default=True, type=bool, help='Collapsible content list.')
@click.option('--username', envvar='USER', required=True, help='GitHub username.')
@click.option('--token', envvar='GITHUB_TOKEN', required=True, help='GitHub token.')
@click.option('--topic_limit', default=500, show_default=True, type=int,
              help='Topic limit, increase to reduce topics number.')
@click.option('--repository', default='', show_default=True, help='Repository name.')
@click.option('--filename', default='README.md', show_default=True, help='Filename.')
@click.option('--message', default='Update by starred', show_default=True, type=str, help='Commit message.')
@click.option('--license_name', is_flag=False, show_default=False, type=str, help='Footer license name.', default="CC0")
@click.option('--license_badge', is_flag=False, show_default=False, type=str, help='Footer license badge.',
              default="http://mirrors.creativecommons.org/presskit/buttons/88x31/svg/cc-zero.svg")
@click.option('--license_link', is_flag=False, show_default=False, type=str, help='Footer license link.',
              default="https://creativecommons.org/publicdomain/zero/1.0/")
@click.version_option(version=VERSION, prog_name='starred')
def starred(username, token, sort, topic, repository, filename, message, private, topic_limit, collapse, license_name,
            license_badge, license_link):
    """
    Create an awesome list of your starred repos.
    """
    gh = GitHubGQL(token)
    try:
        stars = gh.get_user_starred_by_username(username, topic_stargazer_count_limit=topic_limit)
    except Exception as e:
        click.secho(f'Error: {e}', fg='red')
        return

    if repository:
        file = BytesIO()
        sys.stdout = file
    else:
        file = None

    if collapse:
        click.echo(str(desc + "<details>\n<summary>Click to expand!</summary> \n").encode('utf-8'))
    else:
        click.echo(desc.encode('utf-8'))

    repo_dict = {}

    for s in stars:
        # skip private repos if --private is not set
        if s.is_private and not private:
            continue

        description = html_escape(s.description).replace('\n', '').strip()[:TEXT_LENGTH_LIMIT] if s.description else ''
        if not description.endswith("."):
            description += "."
        date_format = datetime.datetime.strptime(s.commit_date, "%Y-%m-%dT%H:%M:%SZ")
        date = date_format.strftime("%a %d %B %Y at %I:%M %p")

        if topic:
            for category in s.topics or [DEFAULT_CATEGORY.lower()]:
                if category not in repo_dict:
                    repo_dict[category] = []
                repo_dict[category].append([s.name, s.url, description, date, s.stargazer_count, s.licenseinfo])
        else:
            category = s.language or DEFAULT_CATEGORY
            if category not in repo_dict:
                repo_dict[category] = []
            repo_dict[category].append([s.name, s.url, description, date, s.stargazer_count, s.licenseinfo])

    if sort:
        repo_dict = OrderedDict(sorted(repo_dict.items(), key=lambda l: l[0]))

    title_dict = {}
    for category in repo_dict.keys():
        # data = f'- [{category}](#{"-".join(title2url(category).lower().split())})'
        title = f'{category}'
        title_url = title2url(category)
        if title_url not in title_dict:
            title_dict[title_url] = 1
        else:
            cnt = title_dict[title_url]
            title_dict[title_url] += 1
            title_url = title_url + '-' + str(cnt)

        data = f'  - [{title}](#{title_url.lower()})'
        click.echo(data.encode('utf-8'))
    click.echo('')
    if collapse:
        click.echo("</details> \n")

    for category in repo_dict:
        click.echo(f'## {category} \n'.encode('utf-8'))
        for repo in repo_dict[category]:
            data = u'- [{}]({}) - {}'.format(*repo[:3])
            details = u'   - Updated on `{}` | {}⭐ | `{}`'.format(*repo[3:])
            click.echo(data.encode('utf-8'))
            click.echo(details.encode('utf-8'))
        click.echo(' \n**[`^        back to top        ^`](#)**')
        click.echo('')

    click.echo(license_.format(username=username, license_name=license_name, license_badge=license_badge,
                               license_link=license_link).encode('utf-8'))

    if file:
        gh = GitHub(token=token)
        try:
            rep = gh.repository(username, repository)
            try:
                rep.file_contents(f'/{filename}').update(message, file.getvalue())
            except NotFoundError:
                rep.create_file(filename, message, file.getvalue())
        except NotFoundError:
            rep = gh.create_repository(repository, 'A curated list of my GitHub stars!')
            rep.create_file(filename, 'Initial commit', file.getvalue())
        click.launch(rep.html_url)


if __name__ == '__main__':
    starred()
