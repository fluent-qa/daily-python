# README

Daily Python Practice Libs.

## ```uv``` for mono  python repo

use ```uv``` to manage the project. superfast than pdm and poetry.

[uv reference](https://docs.astral.sh/uv/), why use uv? Two key points:

1. Fast,really fast

![uv](https://github.com/astral-sh/uv/assets/1309177/03aa9163-1c79-4a87-a31d-7a9311ed9310#only-dark)

2. easy to manage mono python repo, no need to worry about the dependency conflict

And also similar to pdm and poetry, easy to migrate and understand the concepts.

## Project/Lib Structure and Usage

**shared folder**:

```
shared
├── qpy-tpl: template project
├── qpyci： ci helper project
├── qpyconf: configuration project
├── qpydao: dao project
├── qpyhelper: helper project to capture api request
└── qpystructs: structures project
```

## Agent

Crew only works for python3.11 right now.
