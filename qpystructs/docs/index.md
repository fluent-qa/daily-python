# Index

Quick Introduction for PDM Pythong Depencincy Manager,and how to use pdm to init project from a github repo.

## PDM

- [PDM](./pdm/0-setup.md) PDM setup
- [PDM](./pdm/1-dependencies.md) PDM depenencies management
- [PDM](./pdm/2-pdm-script.md) PDM scripts

## Init Project Quickstart
Two ways to create a new python project:

- create project by copier:

```sh
copier copy --trust https://github.com/fluent-qa/fluentqa-pytpl.git my-project
```

- create project by pdm

```sh
mkdir my-project && cd my-project
pdm init https://github.com/fluent-qa/fluentqa-pytpl.git
```

Two ways to create a new python project:

- create project by copier:

```sh
copier copy --trust https://github.com/fluent-qa/fluentqa-pytpl.git my-project
```

- create project by pdm

```sh
mkdir my-project && cd my-project
pdm init https://github.com/fluent-qa/fluentqa-pytpl.git
```


## PDM as Pythong Depencincy Manager

- [PDM](https://pdm.fming.dev/)
- [PDM 中文文档](https://pdm.fming.dev/zh_CN/latest/index.html)

## Templates References

templates:
  - https://github.com/serious-scaffold/ss-python.git
  - https://github.com/TezRomacH/python-package-template.git
  - https://github.com/leynier/python-template.git
  - https://github.com/fpgmaas/cookiecutter-poetry.git
  - https://github.com/zillionare/cookiecutter-pypackage.git
  - https://github.com/rnag/cookiecutter-pypackage.git
  - https://github.com/yxtay/python-project-template.git
