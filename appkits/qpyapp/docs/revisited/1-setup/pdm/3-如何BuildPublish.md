---
prompt: 文档地址为https://pdm-project.org/latest/,请为一个初学者总结,PDM如何Build和Publish,并用markdown 返回
---

PDM（Python Dependency Manager）是一个现代的Python包和依赖管理工具。以下是如何使用PDM构建和发布项目的简要指南。

## 构建和发布项目

### 构建项目

1. **初始化项目**：
   - 在项目根目录下运行以下命令来初始化项目：
     ```bash
     pdm init
     ```
   - 这将创建一个`pyproject.toml`文件，用于存储项目的配置信息。

2. **添加依赖**：
   - 使用以下命令添加依赖包：
     ```bash
     pdm add <package_name>
     ```
   - 例如，添加`requests`包：
     ```bash
     pdm add requests
     ```

3. **构建项目**：
   - 使用以下命令构建项目：
     ```bash
     pdm build
     ```
   - 这将生成一个`wheel`和一个源代码分发包（`sdist`），并将它们存储在`dist/`目录中。

### 发布项目

1. **发布到PyPI**：
   - 使用以下命令将构建的包发布到PyPI：
     ```bash
     pdm publish
     ```
   - 这将自动构建并上传包到PyPI索引。

2. **指定其他仓库**：
   - 如果需要发布到其他仓库，可以使用`--repository`选项：
     ```bash
     pdm publish --repository <repository_url>
     ```
   - 例如，发布到自定义仓库：
     ```bash
     pdm publish --repository https://example.com/repository
     ```

3. **分步构建和发布**：
   - 你也可以分两步进行构建和发布，以便在上传之前检查构建的工件：
     ```bash
     pdm build
     pdm publish
     ```

### 示例

#### 构建项目

```bash
# 初始化项目
pdm init

# 添加requests包
pdm add requests

# 构建项目
pdm build
```

#### 发布项目

```bash
# 发布到PyPI
pdm publish

# 发布到自定义仓库
pdm publish --repository https://example.com/repository
```

通过以上步骤，你可以使用PDM轻松地构建和发布Python项目。更多详细信息可以参考PDM的官方文档：[PDM文档](https://pdm-project.org/latest/)[1][3][4]。

Citations:
[1] https://pdm-project.org/latest/
[2] https://juejin.cn/post/7066326746412351519
[3] https://pdm-project.org/latest/usage/publish/
[4] https://pdm-project.org/latest/reference/build/
[5] https://github.com/pdm-project/pdm-build-locked
