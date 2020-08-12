





#  	[Jupyter/JupyterLab安装使用]

(https://www.cnblogs.com/ssooking/p/9165560.htm



## 一.介绍

[Jupyther notebook](https://github.com/jupyter/notebook)（曾经的Ipython notebook），是一个可以把代码、图像、注释、公式和作图集于一处，实现可读性及可视化分析的工具，支持多种编程语言。[官方使用手册](http://jupyter.readthedocs.io/en/latest/)。

安装前，你需要装好python环境，并且安装pip包管理器。

## 二. 安装

### 使用pip安装jupyter notebook

#### Python2

```
pip install --upgrade pip
sudo pip install jupyter notebook
```

或者

```
python -m pip install jupyter
```

#### Python3

```
pip3 install --upgrade pip
sudo pip3 install jupyter notebook
```

或者

```
python3 -m pip install jupyter
```

### 运行jupyter notebook

```
jupyter notebook
```

或者

```
ipython notebook
```

## 三.必要环境配置

```
ipython profile create
```

此时会在你的家目录生成配置文件`.ipython/profile_default/ipython_kernel_config.py`

### 运行代码后自动显示变量值

直接在该文件的头部添加代码

```
c = get_config()
c.InteractiveShell.ast_node_interactivity = "all"
```

### ipython中文编码问题

```
vi ~/.ipython/ipythonrc
readline_parse_and_bind "\M-i": "    "
readline_parse_and_bind "\M-o": "\d\d\d\d"
readline_parse_and_bind "\M-I": "\d\d\d\d
```

注释掉这3行

### 使用matplotlib作图显示中文

需要设置中文字体，否则中文会乱码。

```
import matplotlib.pyplot as plt  
plt.rc('font', family='Microsoft YaHei Mono', size=12)
```

## 四.基本使用

#### 常用快捷键

- 在当前cell的上一层添加cell：A
- 在当前cell的下一蹭添加cell：B
- 双击d：删除当前cell
- 撤销对某个cell的删除：z
- 当前的cell进入编辑模式：Enter
- 退出当前cell的编辑模式：Esc
- 执行当前cell并跳到下一个cell：Shift Enter
- 执行当前cell执行后不调到下一个cell：Ctrl Enter
- 向下选择多个cell:Shift + J 或 Shift + Down
- 向上选择多个cell：Shift + K 或 Shift + Up
- 合并cell：Shift + M
- 在代码中查找、替换，忽略输出：Esc + F
- 在cell和输出结果间切换：Esc + O
- 快速跳转到首个cell：Crtl Home
- 快速跳转到最后一个cell：Crtl End
- m：进入markdown模式，编写md的文档进行描述说明
- 为当前的cell加入line number：单L
- 将当前的cell转化为具有一级标题的maskdown：单1
- 将当前的cell转化为具有二级标题的maskdown：单2
- 将当前的cell转化为具有三级标题的maskdown：单3
- 为一行或者多行添加/取消注释：Crtl /
- 在浏览器的各个Tab之间切换：Crtl PgUp和Crtl PgDn

## 参考

<https://www.zybuluo.com/hanxiaoyang/note/534296>

<https://zhuanlan.zhihu.com/p/26739300?group_id=843868091631955968>

<https://www.cnblogs.com/Sinte-Beuve/p/5148108.html>

<https://www.zhihu.com/question/59392251>

<http://www.jianshu.com/p/2f3be7781451> Anaconda使用总结

# JupyterLab安装使用

JupyterLab是Jupyter Notebook的增强版本，看起来更像是一个IDE。

```
pip install jupyterlab
```

#### 安装早版本的Jupyter Notebook

如果你使用的Jupyter版本早于5.3，那么你还需要运行以下命令来启动JupyterLab服务组件。

```
jupyter serverextension enable --py jupyterlab --sys-prefix
```

### 运行

使用以下命令运行JupyterLab:

```
jupyter lab
```

JupyterLab 会在自动在浏览器中打开. See our [documentation](http://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html) for additional details.

查看令牌

```
jupyter notebook list
```

输出

```
http://localhost:8888/?token=c8de56fa... :: /Users/you/notebooks
```

您可以通过运行以下命令列出当前安装的扩展：

```
jupyter labextension list
```

通过运行以下命令卸载扩展：

```
jupyter labextension uninstall my-extension
```

其中`my-extension`是扩展名列表中的打印名称。您也可以使用此命令卸载核心扩展（以后可以随时重新安装核心扩展）。

### 参考

<https://jupyterlab.readthedocs.io/en/latest/user/extensions.html>
 <https://github.com/jupyterlab/jupyterlab#getting-help>
 <https://gitter.im/jupyterlab/jupyterlab>
 <http://jupyterlab.github.io/jupyterlab/>