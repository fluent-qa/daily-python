## Tutorials

- ## Overview:

- For Basic Python:
![img](./qa-daily-utils.png)

- [Python Tutorials: 30 minutes Per Day](https://github.com/fluent-qa/fluent-qa/pyqa-30min.git)

## one-python

We don't need [a lot of libraries](https://github.com/vinta/awesome-python). We just need the best ones.

-----
## Libraries

## Utilities

#### Interactive Interpreter
* [IPython](https://github.com/ipython/ipython) - A rich toolkit to help you make the most out of using Python interactively.

#### Environment
* [poetry](https://python-poetry.org/) - A tool to create isolated Python environments and manage poetry project

#### IDE
* [PyCharm](https://www.jetbrains.com/pycharm/) - Commercial Python IDE based on the IntelliJ platform by JetBrains. Free community edition available.


#### General Machine Learning
* [scikit-learn](http://scikit-learn.org/) - Simple and efficient tools for data mining and data analysis.

#### Machine Learning > Deep Learning
* [TensorFlow](https://www.tensorflow.org/) - Low-level (configurations over conventions) library for building deep learning data flow graphs.

#### Machine Learning > Deep Learning + Computer Vision
* [caffe](http://caffe.berkeleyvision.org/) - Deep learning framework made with expression, speed, and modularity in mind.

#### Optical Character Recognition (OCR)
* [pytesseract](https://github.com/madmaze/pytesseract) - A wrapper for Google Tesseract OCR.

#### Chinese Word Segmentation
* [jieba](https://github.com/fxsjy/jieba) - Chinese Words Segmentation Utilities.

#### Concurrency and Networking
* [gevent](http://www.gevent.org/) - A coroutine-based Python networking library that uses [greenlet](https://github.com/python-greenlet/greenlet).

#### HTTP Request
* [requests](https://github.com/kennethreitz/requests) - Python HTTP requests for humans.

#### Web Crawling
* [Scrapy](http://scrapy.org/) - A fast high-level screen scraping and web crawling framework.

#### Web Content Extracting
* [newspaper](https://github.com/codelucas/newspaper) - News extraction, article extraction and content curation in Python.

#### Scientific Computing
* [scipy](https://github.com/scipy/scipy) - An open-source software for mathematics, science, and engineering. statistics, optimization, integration, linear algebra, Fourier transforms, signal and image processing, ODE solvers, and more.

#### Natural Language
* [nltk](http://www.nltk.org/) - A suite of libraries and programs for symbolic and statistical natural language processing.

#### Markdown
* [mistune](https://github.com/lepture/mistune) - The fastest markdown parser in pure Python with renderer features, inspired by marked.

#### Data Analysis
* [pandas](http://pandas.pydata.org/) - A software library for data manipulation and analysis. In particular, it offers data structures and operations for manipulating numerical tables and time series.

-----

## Frameworks

* [Django](https://www.djangoproject.com/) - The most popular full featured web framework in Python.
    * [djangopackages](https://www.djangopackages.com/) - Excellent 3rd party django package collections.



## Issues
### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

### Makefile usage

[`Makefile`](https://github.com/{{ cookiecutter.github_name }}/{{ cookiecutter.project_name }}/blob/master/Makefile) contains a lot of functions for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort` and `black`.

```bash
make codestyle

# or use synonym
make formatting
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `isort`, `black` and `darglint` library

Update all dev libraries to the latest version using one comand

```bash
make update-dev-deps
```

</p>
</details>

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

<details>
<summary>5. Type checks</summary>
<p>

Run `mypy` static type checker

```bash
make mypy
```

</p>
</details>

<details>
<summary>6. Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

the same as:

```bash
make test && make check-codestyle && make mypy && make check-safety
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

```bash
make docker-build
```

which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with

```bash
make docker-remove
```

More information [about docker](https://github.com/{{ cookiecutter.github_name }}/{{ cookiecutter.project_name }}/tree/master/docker).

</p>
</details>

<details>
<summary>9. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>


## 🎯 What's next

- [`Typer`](https://github.com/tiangolo/typer) is great for creating CLI applications.
- [`Rich`](https://github.com/willmcgugan/rich) makes it easy to add beautiful formatting in the terminal.
- [`Pydantic`](https://github.com/samuelcolvin/pydantic/) – data validation and settings management using Python type hinting.
- [`Loguru`](https://github.com/Delgan/loguru) makes logging (stupidly) simple.
- [`tqdm`](https://github.com/tqdm/tqdm) – fast, extensible progress bar for Python and CLI.
- [`IceCream`](https://github.com/gruns/icecream) is a little library for sweet and creamy debugging.
- [`orjson`](https://github.com/ijl/orjson) – ultra fast JSON parsing library.
- [`Returns`](https://github.com/dry-python/returns) makes you function's output meaningful, typed, and safe!
- [`Hydra`](https://github.com/facebookresearch/hydra) is a framework for elegantly configuring complex applications.
- [`FastAPI`](https://github.com/tiangolo/fastapi) is a type-driven asynchronous web framework.



# Todo App

Todo App is a **hobby project** that is primarily focused around being a playground for experimenting with different technologies.

## Application Architecture

![Todo App Architecture](doc/architecture.svg)

## Secrets Management

This repository uses [SOPS](https://github.com/mozilla/sops) with [age](https://github.com/mozilla/sops#22encrypting-using-age) for managing secrets.

See [Configuration and Secrets Management](config/) for details.

## Reverse Proxy

- [Caddy](https://caddyserver.com/)

## Real-Time Messaging

- [Centrifugo](https://centrifugal.dev/)
  - URL: http://centrifugo.todo-app.com
  - password: `S3c_r3t!`

## Workflow Engine

- [Temporal](https://temporal.io/)
  - URL: http://temporal.todo-app.com

## Monitoring Stack

- [Grafana](https://grafana.com/oss/grafana/)
  - URL: http://grafana.todo-app.com
  - username: `admin`
  - password: `S3c_r3t!`
- [Loki](https://grafana.com/oss/loki/)
- [Promtail](https://grafana.com/docs/loki/latest/clients/promtail/)
- [MinIO](https://min.io/)
  - URL: http://minio.todo-app.com
  - username: `console`
  - password: `S3c_r3t!`

## Identity and Access Management

- [Keycloak](https://www.keycloak.org/)
  - URL: http://auth.todo-app.com
  - username: `admin`
  - password: `S3c_r3t!`

## Running the App Locally

1. Add the following entries to your `/etc/hosts` file:

```
127.0.0.1    todo-app.com
127.0.0.1    auth.todo-app.com
127.0.0.1    centrifugo.todo-app.com
127.0.0.1    temporal.todo-app.com
127.0.0.1    grafana.todo-app.com
127.0.0.1    minio.todo-app.com
```

2. Make sure you have the unencrypted secrets in the `env` directory. See [Configuration and Secrets Management](config/) for details.

3. Run Docker Compose

```bash
> docker compose up --build -d
```

4. Import the Keycloak realm. See [Configuring Keycloak](backend/keycloak/) for details.

5. Open the App in browser: http://todo-app.com
   - Normal user:
     - username: `demouser`
     - password: `S3c_r3t!`
   - Viewer (read-only) user:
     - username: `demoviewer`
     - password: `S3c_r3t!`

## Tools

### JSON Schema Generator

The app uses [JSON Schema](https://json-schema.org/) for message validation. See [json-schema-generator](tools/json-schema-generator) for details.


## one-python

We don't need [a lot of libraries](https://github.com/vinta/awesome-python). We just need the best ones.

-----

#### Interactive Interpreter
* [IPython](https://github.com/ipython/ipython) - A rich toolkit to help you make the most out of using Python interactively.

#### Environment
* [poetry](https://python-poetry.org/) - A tool to create isolated Python environments and manage poetry project

#### IDE
* [PyCharm](https://www.jetbrains.com/pycharm/) - Commercial Python IDE based on the IntelliJ platform by JetBrains. Free community edition available.


#### General Machine Learning
* [scikit-learn](http://scikit-learn.org/) - Simple and efficient tools for data mining and data analysis.

#### Machine Learning > Deep Learning
* [TensorFlow](https://www.tensorflow.org/) - Low-level (configurations over conventions) library for building deep learning data flow graphs.

#### Machine Learning > Deep Learning + Computer Vision
* [caffe](http://caffe.berkeleyvision.org/) - Deep learning framework made with expression, speed, and modularity in mind.

#### Optical Character Recognition (OCR)
* [pytesseract](https://github.com/madmaze/pytesseract) - A wrapper for Google Tesseract OCR.

#### Chinese Word Segmentation
* [jieba](https://github.com/fxsjy/jieba) - Chinese Words Segmentation Utilities.

#### Concurrency and Networking
* [gevent](http://www.gevent.org/) - A coroutine-based Python networking library that uses [greenlet](https://github.com/python-greenlet/greenlet).

#### HTTP Request
* [requests](https://github.com/kennethreitz/requests) - Python HTTP requests for humans.

#### Web Crawling
* [Scrapy](http://scrapy.org/) - A fast high-level screen scraping and web crawling framework.

#### Web Content Extracting
* [newspaper](https://github.com/codelucas/newspaper) - News extraction, article extraction and content curation in Python.

#### Scientific Computing
* [scipy](https://github.com/scipy/scipy) - An open-source software for mathematics, science, and engineering. statistics, optimization, integration, linear algebra, Fourier transforms, signal and image processing, ODE solvers, and more.

#### Natural Language
* [nltk](http://www.nltk.org/) - A suite of libraries and programs for symbolic and statistical natural language processing.

#### Markdown
* [mistune](https://github.com/lepture/mistune) - The fastest markdown parser in pure Python with renderer features, inspired by marked.

#### Data Analysis
* [pandas](http://pandas.pydata.org/) - A software library for data manipulation and analysis. In particular, it offers data structures and operations for manipulating numerical tables and time series.

-----

## Frameworks

* [Django](https://www.djangoproject.com/) - The most popular full featured web framework in Python.
    * [djangopackages](https://www.djangopackages.com/) - Excellent 3rd party django package collections.



