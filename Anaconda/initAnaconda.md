

## Anaconda  常用命令

### 境变量生效

```text
$ source ~/.bash_profile
```

###  Mac常用的命令

- 查看conda版本

```
$ conda --version
```

- 更新conda版本

```
$ conda update conda
```

- 查看都安装了那些依赖库

```
$ conda list
```

- 创建新的python环境

```
$ conda create --name myenv
```

并且还可以指定python的版本

```
$ conda create -n myenv python=3.7
```

- 创建新环境并指定包含的库

```
$ conda create -n myenv scipy
```

并且还可以指定库的版本

```
$ conda create -n myenv scipy=0.15.0
```

##### 复制环境

```
$ conda create --name myclone --clone myenv
```

查看是不是复制成功了

```
$ conda info --envs
```

- 激活、进入某个环境

```
$ source activate myenv
```

- 退出环境

```
$ source deactivate
```

- 删除环境

```
$ conda remove --name myenv --all
```

### 查看当前的环境列表

```
$ conda info --envs   or   $ conda env list
```

### 查看某个环境下安装的库

```
$ conda list -n myenv
```

### 查找包

```
$ conda search XXX
```

### 安装包

```
$ conda install XXX
```

### 更新包

```
$ conda update XXX
```

- 删除包

```
$ conda remove XXX
```

### 安装到指定环境

```
$ conda install -n myenv XXX
```

好以上就是Anaconda的安装和基本的使用了。









###   install清单: 

1.conda list  #查看安装的包

2.conda list -n environment_name  #查看指定环境下的包

3.conda install -n environment_name XXX  #在指定环境中安装包

\# 如果不用-n指定环境名称，则被安装在当前活跃环境

\# 也可以通过-c指定通过某个channel安装

 

##### **# 更新package**

4.conda update -n environment_name numpy

 

##### **# 删除package**

5.conda remove -n environment_name numpy

 

##### 6.conda info -e  

查看当前已配置的环境









### 管理conda：

##### 检查conda版本:

```bash
conda --version
```



------

##### 升级当前版本的conda

```bash
conda update conda
```



### 操作环境



  Anaconda常用命令大全

https://blog.csdn.net/fyuanfena/article/details/52080270

##### 激活 环境

8.activate environment_name  #激活进入名为environment_name的环境（windows）

​     \# linux为：source activate environment_name

- ##### Linux，OS X:

```bash
conda activate dgdata
source activate snowflakes1
```

- ##### Windows：

```bash
activate snowflake
```



#####  退出/ **取消**环境

conda deactivate 

9.deactivate environment_name  #退出环境

​     \# linux为：source deactivate environment_name

****

##### 创建环境

7.conda create --name environment_name python=3.4

\#创建一个名字为environment_name，python版本为3.4的环境

eg：conda create -n environment_name python=3.4





#####  删除环境

10.conda remove --name environment_name --all  #删除环境



```bash
# 创建环境
# 我conda版本=4.6.4 似乎新建环境默认不带py解释器，需要显式指定 python
conda create -n 名字 [软件包=version]
# 列出所有环境
conda env list
# 切换环境
activate 名字 # linux及bash下要加 source 前缀
# 删除环境
conda remove -n 名字 --all
# 导出环境
conda env export > environment.yml
# 导入环境
conda env create -f environment.yml
# 安装包
conda install 名字[=version]
# 查看包列表
conda list
# 删除包
conda remove 名字
```





\# 修改路径

11.cd +path；cmd 命令：cd D:/path，#不同环境的路径相同的情况注意

12.控制面板---系统---高级系统设置---环境变量中进行添加新的路径

 

### Tensorboard命令

https://blog.csdn.net/qq_41997920/article/details/85217189

13.Tensorboard --logdir=（路径名logs）

tensorboard 运行

TensorBoard是TensorFlow下的一个可视化的工具，能够帮助我们在训练大规模神经网络过程中出现的复杂且不好理解的运算。TensorBoard能展示你训练过程中绘制的图像、网络结构等。

启动TensorBoard的方法：

1.定位到你训练后log文件保存的位置；

2.cd 到log文件的上一级目录；

  eg：H:\tmp\tensorflow/mnis/

3.键入命令行，启动TensorBoard；
   \>>命令行是： tensorboard --logdir=（log下一级文件名） 
   \#linux 247服务器上输入（tensorboard --logdir=/home/huoo/tensorflow-api-liulina/Object-Detector-App1/data/）

  回车，就自动加载。复制网址到Chrome浏览器中就可以打开TensorBoard。

4.把服务器的ip地址输入到Chrome浏览器中就会看到TensorBoard的页面了。





## 镜像源

### Anaconda 镜像源操作(查看配置删除)

https://www.cnblogs.com/yirufeng/p/12242290.html



##### OTHERS 



###### Anaconda [查看、添加、删除 安装源](https://blog.csdn.net/David_jiahuan/article/details/104544957)

###### [anaconda查看删除增加镜像源](https://www.cnblogs.com/jeshy/p/10532983.html)

https://www.cnblogs.com/jeshy/p/10532983.html

[最省心的安装配置操作](https://zhuanlan.zhihu.com/p/25198543)
 [配置增加删除](https://www.cnblogs.com/jeshy/p/10532983.html)
 [增加Conda镜像源](https://blog.csdn.net/just_h/article/details/90451935)



##### \# 查看显示原来的镜像源

```bash

 conda config --show-sources
```

`conda config --show` 将会显示conda的配置信息，找到channel, 对应的就是我们的镜像配置



```bash
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - defaults
```





conda config --show

(base) [jiangshan@localhost ~]$ conda config --show

##### \# 添加新镜像源

  

```bash
 conda config --add channels 
 
 conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/


conda config --set show_channel_urls yes
```





```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
 conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ 
 conda config --set show_channel_urls yes
```





conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/



(base) [jiangshan@localhost ~]$ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/tensorflow/linux/cpu/



#####  # 配置第三方源



```bash
Conda Forge
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/

msys2
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/

bioconda
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/

menpo
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/menpo/

pytorch
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
```



#####  # 删除旧镜像源



conda config --remove channels  



```bash
conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/


(base) [jiangshan@localhost ~]$ conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/tensorflow/linux/cpu/
```





##### \# 设置搜索时显示通道地址

conda config --set show_channel_urls yes

(base) [jiangshan@localhost ~]$ conda config --set show_channel_urls yes





## PIP

###   python pip ,安装，卸载，查看等命令，不同版本

https://blog.csdn.net/u013258415/article/details/78974665

 

 转载于：https://www.cnblogs.com/xiexiaoxiao/p/7147920.html



##### pip升级包

命令：

pip install --upgrade packagename

pip install --upgrade pip

```python
pip install --upgrade pip
python -m pip install --upgrade pip
```



```html
conda install mingw libpython
```



##### pip	Win	使用

在pyhton/scripts文件下，pip.exe pipx.exe是存在的，在CMD命令行下，pip --version 无法参看版本号，这是因为没有配置环境变量的原因。将pip.exe所在的目录配置到环境变量就OK了

 

##### 使用pip安装python包

 不同版本：前面加python版本号 -m 

如：python3 -m pip install Django==1.10.7

 



命令：

 pip install SomePackage      # latest version

 pipinstall SomePackage==1.0.4   # specificversion

 pipinstall 'SomePackage>=1.0.4'   #minimum version

 

##### pip查看已安装的包

 

-  命令：pip show packagename

 

功能：查看指定的安装包信息



- 命令：pip list



功能：列出所有的安装包

 

##### pip检测更新

 

命令：pip list –outdated

 



 

##### pip卸载包

命令：pip uninstall packagename

 

PS：

经笔者[测试](http://lib.csdn.net/base/softwaretest)，使用pip卸载使用pip安装的python包时，可以完全卸载干净，但是在使用pip卸载使用python setup.py install安装的python包时，并不能卸载干净，仍然需要手动删除先关文件。





# END