## README
安装：使用python uv 安装所有依赖
```shell
uv sync 
```
配置：
1. setting.toml  文件：REWORKSPACE 这个配置到本地目录
2. 代码运行主要在： [test_standard_process.py](tests%2Floc_gov_bonds%2Ftest_standard_process.py) 这个文件 

## 代码运行步骤:

1. ```test_download_all_bonds``` 这个函数用来下载pdf文件
修改年份范围和省份范围，可以指定某个省某个年份范围下载PDF,下载完成之后的文件目录结构：{REWORKSPACE}/<省份>/<年份>
![download-pdf.png](download-pdf.png)

2```test_unzip_all_files``` 这个用来unzip下载的所有zip包里面的文件到指定目录all_files目录,修改省份和年份就可以
![img_1.png](img_1.png)

3```test_import_project_detail_data``` 用来将csv数据数据清洗，结构化，导入数据句，修改年份和省份，
从 **<年份>-<省份名>.csv** 文件中读取数据，清洗结果的文件是 ***cleanup-<年份>-<省份名>.csv***
![img_1.png](img_1.png)
![img_2.png](img_2.png)

4.```test_cleanup_import`` 直接从清洗过的文件中导入数据库,使用基本同第三步骤，主要发现有些原始文件保存数据库出错，然后修改
一下清洗文件之后，直接导入

## 数据从哪里来

pdf文件下载完成之后,
1. 通过***WPS*** 的 ***PDF转换成EXCEL功能*** 批量转换PDF成EXCEL文件
2. 从EXCEL文件中获取到相关的债券信息表格，复制到<年份>-<省份名>.csv 中间中
3. 复制过程中尽可能的对齐数据，有偏差问题不大，但是取的值的列数需要对上，比如
![img_3.png](img_3.png)
1，2，3，4是需要的数据，每行不对齐没有问题，
但是每行有数据的1，2，3，4顺序的值需要是正确对应的，中间有多少空行是可以在清洗时候处理的
具体就是每行的：第1有数字的列代表了债券名称，第2个有值的列代表了项目名称，第4个有值的列代表了发行金额，
1和2，3和4中间有空列，每行都有不一样数量的空列都问题不大可以清洗
