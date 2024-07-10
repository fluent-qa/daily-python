# PDM Dependencies

PDM 依赖管理工具，用于管理项目依赖。

### 添加依赖

```bash
pdm add requests
```

### 更新依赖

```bash
pdm update requests
```

### 删除依赖

```bash
pdm remove requests
```
### 本地+url依赖

```bash
pdm add ./sub-package
pdm add ./first-1.0.0-py2.py3-none-any.whl
pdm add "https://github.com/numpy/numpy/releases/download/v1.20.0/numpy-1.20.0.tar.gz"
pdm add "https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.5.0/en_core_web_trf-3.5.0-py3-none-any.whl"
# A relative path to the directory
pdm add -e ./sub-package --dev
# A file URL to a local directory
pdm add -e file:///path/to/sub-package --dev
# A VCS URL
pdm add -e git+https://github.com/pallets/click.git@main#egg=click --dev
```
在pyproject.toml文件中的展示:

```toml
[project]
dependencies = [
    "sub-package @ file:///${PROJECT_ROOT}/sub-package",
    "first @ file:///${PROJECT_ROOT}/first-1.0.0-py2.py3-none-any.whl",
]
```

### VCS dependencies

```bash
# Install pip repo on tag `22.0`
pdm add "git+https://github.com/pypa/pip.git@22.0"
# Provide credentials in the URL
pdm add "git+https://username:password@github.com/username/private-repo.git@master"
pdm add "wheel @ git+ssh://git@github.com/pypa/wheel.git@main"
# Give a name to the dependency
pdm add "pip @ git+https://github.com/pypa/pip.git@22.0"
# Or use the #egg fragment
pdm add "git+https://github.com/pypa/pip.git@22.0#egg=pip"
# Install from a subdirectory
pdm add "git+https://github.com/owner/repo.git@master#egg=pkg&subdirectory=subpackage"
```


### 安装依赖-分组

添加分组： ```-dG```

```bash
pdm add -dG test pytest
```

## 依赖树:Show the dependency tree#

```bash
pdm list --tree
pdm list --tree --reverse certifi
```

## Manage global project#
