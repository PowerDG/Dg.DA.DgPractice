# 《从0到1学习spark》-- spark前世今生

https://www.jianshu.com/p/93548cc25a9f

###     spark的前世今生



![img](https:////upload-images.jianshu.io/upload_images/7187100-aa2f4f78fcf1b329?imageMogr2/auto-orient/strip%7CimageView2/2/w/554)

image

Spark是一个快速的，通用的，大数据规模的运算引擎。

- 2009年诞生于加州大学伯克利分校AMPLab
- 2010年开源
- 2013年6月成为Apache孵化项目
- 2014年2月成为Apache顶级项目

目前，Spark生态系统已经发展成为一个包含多个子项目的集合，其中包含SparkSQL、Spark Streaming、GraphX、MLib、SparkR等子项目，Spark是基于内存计算的大数据并行计算框架。除了扩展了广泛使用的 MapReduce 计算模型，而且高效地支持更多计算模式，包括交互式查询和流处理。

Spark 适用于各种各样原先需要多种不同的分布式平台的场景，包括批处理、迭代算法、交互式查询、流处理。通过在一个统一的框架下支持这些不同的计算。

Spark 使我们可以简单而低耗地把各种处理流程整合在一起，在实际的数据分析过程中是很有意义的，不仅如此，Spark 的这种特性还大大减轻了原先需要对各种平台分 别管理的负担。

###     spark技术栈

Spark大一统的软件栈，各个组件关系密切并且可以相互调用，这种设计有几个好处：

1、软件栈中所有的程序库和高级组件都可以从下层的改进中获益。

2、运行整个软件栈的代价变小了。不需要运 行 5 到 10 套独立的软件系统了，一个机构只需要运行一套软件系统即可。系统的部署、维护、测试、支持等大大缩减。

3、能够构建出无缝整合不同处理模型的应用。

Spark的内置项目如下：



![img](https:////upload-images.jianshu.io/upload_images/7187100-0923d3c54d197c58?imageMogr2/auto-orient/strip%7CimageView2/2/w/543)

image

Spark **Core**：实现了 Spark 的**基本功能，包含任务调度、内存管理、错误恢复、与存储系统 交互等模块**。Spark Core 中还包含了对**弹性分布式数据集(resilient distributed dataset，简称RDD)**的 API 定义。

Spark SQL：是 Spark 用来**操作结构化数据**的程序包。通过 Spark SQL，我们可以使用 SQL 或者 Apache Hive 版本的 SQL 方言(HQL)来查询数据。Spark SQL 支持多种数据源，比 如 Hive 表、Parquet 以及 JSON 等。

Spark **Streaming**：是 Spark 提供的对**实时数据进行流式计算**的组件。提供了用来操作数据流的 API，并且与 Spark Core 中的 RDD API 高度对应。

Spark MLlib：提供常见的机器学习(ML)功能的程序库。包括分类、回归、聚类、协同过滤等，还提供了模型评估、数据 导入等额外的支持功能。

集群管理器：Spark 设计为可以高效地在一个计算节点到数千个计算节点之间伸缩计 算。为了实现这样的要求，同时获得最大灵活性，Spark 支持在各种**集群管理器(cluster manager)**上运行，包括 Hadoop YARN、Apache Mesos，以及 Spark 自带的一个简易调度 器，叫作独立调度器。

> Spark得到了众多大数据公司的支持， 
> 当前百度的Spark已应用于**凤巢**、大搜索、直达号、百度大数据等业务； 
> 阿里利用**GraphX**构建了大规模的**图计算和图挖掘系统**，实现了很多生产系统的**推荐算法**； 
> 腾讯**Spark集群**达到8000台的规模，是当前已知的世界上最大的Spark集群。

###     spark的特点

#####      快：

与Hadoop的MapReduce相比，Spark基于内存的运算要快100倍以上，基于硬盘的运算也要快10倍以上。Spark实现了高效的**DAG**执行引擎，可以通过基于内存来高效处理数据流。计算的中间结果是存在于内存中的。



![img](https:////upload-images.jianshu.io/upload_images/7187100-43c4a3b2a6112dd9?imageMogr2/auto-orient/strip%7CimageView2/2/w/554)

image

#####      易用：

Spark支持Java、Python和Scala的API，还支持超过80种高级算法，使用户可以快速构建不同的应用。而且Spark支持交互式的Python和Scala的shell，可以非常方便地在这些shell中使用Spark集群来验证解决问题的方法。



![img](https:////upload-images.jianshu.io/upload_images/7187100-581f9f46f5679f9f?imageMogr2/auto-orient/strip%7CimageView2/2/w/554)

image

#####      通用：

Spark提供了统一的解决方案。Spark可以用于**批处理****、交互式查询（Spark SQL）**、**实时流处理（Spark Streaming）**、机器学习（Spark MLlib）和**图计算（GraphX）**。这些不同类型的处理都可以在同一个应用中无缝使用。Spark统一的解决方案非常具有吸引力，毕竟任何公司都想用统一的平台去处理遇到的问题，减少开发和维护的人力成本和部署平台的物力成本。

#####      **兼容性：**

Spark可以非常方便地与其他的开源产品进行融合。比如，Spark可以使用Hadoop的**YARN**和Apache **Mesos**作为它的**资源管理和调度器**，并且可以处理所有Hadoop支持的数据，包括HDFS、HBase和**Cassandra**等。这对于已经部署Hadoop集群的用户特别重要，因为不需要做任何数据迁移就可以使用Spark的强大处理能力。Spark也可以不依赖于第三方的资源管理和调度器，它实现了Standalone作为其内置的资源管理和调度框架，这样进一步降低了Spark的使用门槛，使得所有人都可以非常容易地部署和使用Spark。此外，Spark还提供了在EC2上部署Standalone的Spark集群的工具。



![img](https:////upload-images.jianshu.io/upload_images/7187100-cff504efa2558737?imageMogr2/auto-orient/strip%7CimageView2/2/w/554)

image

###     Spark的用户和用途

我们大致把Spark的用例分为两类：数据科学应用和数据处理应用。也就对应的有两种人群：数据科学家和工程师。

**数据科学任务：**

主要是数据分析领域，数据科学家要负责分析数据并建模，具备 SQL、统计、预测建模(机器学习)等方面的经验，以及一定的使用 Python、 Matlab 或 R 语言进行编程的能力。

**数据处理应用：**

工程师定义为使用 Spark 开发 生产环境中的数据处理应用的软件开发者，通过对接Spark的API实现对处理的处理和转换等任务。

后续小强会重点从spark实践来总结，快来和小强一起学习spark！

近期热文：

- [比hive快500倍！大数据实时分析领域的黑马](https://mp.weixin.qq.com/s?__biz=MzU3NDc5NzMzNw==&mid=2247483747&idx=1&sn=a400e237db73862540cdecb39cc80d40&scene=21#wechat_redirect)
- [Java中的List你真的会用吗？](http://mp.weixin.qq.com/s?__biz=MzU3NDc5NzMzNw==&mid=2247483755&idx=1&sn=983ee7fe8bf9540e7beb976956b2a58a&chksm=fd2da21dca5a2b0b4105cc3f2292d3386e6358ef3276387935e23206ec7b4fd0f6c33a83ae87&scene=21#wechat_redirect)
- [那些年应该相识的线程安全集合们](http://mp.weixin.qq.com/s?__biz=MzU3NDc5NzMzNw==&mid=2247483759&idx=1&sn=e4e9bc0da8ebc1b0fdd373a50acaa598&chksm=fd2da219ca5a2b0f0e9f9096ab57102500ed570a78fa3d1846c09e0eb2db5198b5a7dbb35104&scene=21#wechat_redirect)
- [互联网JAVA面试常问问题（六）](http://mp.weixin.qq.com/s?__biz=MzU3NDc5NzMzNw==&mid=2247483735&idx=1&sn=10b0f3f3bc8d2869c776f7b151069e81&chksm=fd2da221ca5a2b37e8cdd1352ee0b19fc407fbaf4062b89f4914a0839d8fa58011232d31bc48&scene=21#wechat_redirect)
- [互联网JAVA面试常问问题（七）- 带你走入AQS同步器源码](http://mp.weixin.qq.com/s?__biz=MzU3NDc5NzMzNw==&mid=2247483752&idx=1&sn=ee07bc876930c2e850ad5d27c01f91dc&chksm=fd2da21eca5a2b0800c170f83a7996e43518c5b90300ff4947236283a5c5a247c9d78caf4473&scene=21#wechat_redirect)



![img](https:////upload-images.jianshu.io/upload_images/7187100-22d9b7412025ccf4?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000)

image