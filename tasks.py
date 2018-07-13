from invoke import task

@task
def lint_js(c):
    c.run("node_modules/.bin/eslint django_emoji/static/emoji/js/emoji.js")