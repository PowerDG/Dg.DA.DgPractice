# 《从0到1学习Spark》--DataFrame和Dataset探秘

https://www.jianshu.com/p/cf5ba55d75e2



昨天小强带着大家了解了Spark SQL的由来、Spark SQL的架构和SparkSQL四大组件：Spark SQL、DataSource Api、DataFrame Api和Dataset Api。今天小强和大家一起揭开Spark SQL背后DataFrame和Dataset的面纱。

### DataFrame和Dataset演变

Spark要对**闭包**进行计算、将其**序列化**，并将她们发送到执行进程，这意味着你的代码是以原始形式发送的，基本没有经过优化。在RDD中午发表是结构化数据，对RDD进行查询也不可行。使用RDD很容易但有时候处理元组会把代码弄乱。引入DataFrame和Dataset可以处理数据代码更加易读，支持java、scala、python和R等。
 DataFrame用于创建数据的**行和列**，它就像是关系数据库管理系统中的一张**表**，DataFrame是一种常见的数据分析抽象。
 Dataset结合了DataFrame和RDD的优势：**静态类型**、会更容易实现RDD的功能特性，以及DataFrame的卓越性能特性。

### 为什么使用DataFrame和Dataset

小强认为答案很简单：速度和易用性。DataFrame提供了优化、速度、自动模式发现；他们会读取更少的数据，并提供了RDD之间的互相操作性。

#####  1、优化

 Catalyst为DataFrame提供了优化：谓词下的**推到数据源**，**只读取需要的数据**。创建用于执行的物理计划，并生成比手写代码更优化的JVM字节码。

就像上图这样，DataFrame和Dataset进行了缓存，在缓存时，他们以**更加高效的列式**自动存储数据，这种格式比java、Python对象明显更为**紧凑，并进行了优化**。

#####  2、速度 
 由于优化器会生成用于的JVM字节码，scala和python程序就有相似的性能。Dataset使用优化的编码器把对象进行序列化和反序列化，以便进行并处理并通过网络传输。

#####  3、自动模式发现 
 要从RDD创建DataFrame，必须提供一个模式。而从JSON、Parquet和ORC文件创建DataFrame时，会**自动发现一个模式，包括分区的发现。**

### 实践 
在pyspark shell或spark-shell中，会自动创建一个名为spark的预配置SparkSession。
 从Spark 2.0及更高的版本，SparkSession成为关系型功能的入口点。当使用Hive时，SparkSession必须使用enableSupport方法创建，用来访问Hive Metastore、SerDes和用户自定义的函数。

### 创建DataFrame有三种方式：

1、从结构化数据**文件**创建DataFrame 
2、从**RDD**创建DataFrame
 3、从**Hive中的表**中创建DataFrame

把DataFrame转换为RDD非常简单，只需要使用.rdd方法

### 常用方法的示例

1、DS与DF的关系
 type DataFrame = Dataset[Row]
 2、加载txt数据
 val rdd = sc.textFile("data")

val df = rdd.toDF()
 这种直接生成DF，df数据结构为（查询语句：df.select("*").show(5)）

只有一列，属性为value。
 3、 df.printSchema()

4、使用**反射推断模式**

### 小结

小强从DataFrame和Dataset演变以及为什么使用他们，还有对于DataFrame和Dataset创建和互相转换的一些实践例子进行介绍，当时这些都是比较基础的。深入学习Spark SQL需要了解更多Spark SQL提供的方法。后续小强为大家带来Saprk SQL相关方法以及优化。

【关注】和【点赞】是对小强最大的支持！！！