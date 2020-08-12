





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