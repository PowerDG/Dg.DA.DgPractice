# 《从0到1学习Spark》-- 初识Spark SQL

https://www.jianshu.com/p/24356b917338





Spark SQL是整个Spark生态系统中最常用的组件

今天小强给大家介绍Spark SQL，小强的平时的开发中会经常使用Spark SQL进行数据分析查询操作，Spark SQL是整个Spark生态系统中最常用的组件。这也是为什么很多大公司使用Spark SQL作为大数据分析的关键组件之一。

> 为什么引入Spark SQL

在Spark的早起版本，为了解决Hive查询在性能方面遇到的挑战，在Spark生态系统引入Shark的新项目。Shark使用Spark而不是MR作为执行引擎来执行Hive查询。Shark是在Hive的代码库上构建的，使用Hive查询编译器来解析Hive查询并生成的抽象的语法树，它会转换为一个具有某些基本优化的逻辑计划。Shark应用了额外的优化手段并创建了一个RDD的物理计划，然后在Spark中执行他们的。

这样Shark就能让Hive查询具有了内存级别的性能，但是Shark有三个问题需要处理：

1、Shark只适合查询Hive表，它无法咋RDD上进行关系查询

2、在Spark程序中将Hive Sql作为字符串运行很容易出错

3、它的Hive优化器是MR创建的，很难讲Spark苦熬占到新的数据源和新的处理模型。

之后Spark社区引入了SparkSql，主要包含DataSet和DataFrame，DataFram类似于关系表，它支持丰富的域特定语言、RDD函数和Sql，DataSet主要是DataSet Api，提供了RDD和DataFrame的Api最佳特性。

> Spark SQL架构

Spark Sql是在Spark核心执行引擎之上的一个库，它借助了JDBC、ODBC公开了SQL接口，用于数据仓库应用程序，或通过命令行控制台进行交互式的查询。



![img](https:////upload-images.jianshu.io/upload_images/7187100-6560a59a0fb180f9?imageMogr2/auto-orient/strip%7CimageView2/2/w/640)

image

任何BI工具都可以连接到Spark SQL，以内存速度执行分析。同时还提供了java、scala、python和R支持的Dataset Api和DataFrame Api。Spark SQL用户可以使用Data Sources Api从各种数据源读取和写入数据，从而创建DataFrame或DataSet。

从Spark软件栈中Spark SQL还扩展了用于其他的Spark库，SparkSteaming、Structured Streaming、机器学习库和GraphX的DataSet Api、DataFrame Api。



![img](https:////upload-images.jianshu.io/upload_images/7187100-4a88640ff5cab568?imageMogr2/auto-orient/strip%7CimageView2/2/w/640)

image

创建DataFrame或DataSet后，就可以额在任何库中使用他们呢，他们可互操作，也可以转换为传统的RDD。

Spark SQL引入了一个名为Catalyst的可扩展优化器，以支持大多数常见的数据源和算法。Catalyst支持添加新的数据源、优化规则和某些领域使用的数据类型Catalyst利用Scala的模式匹配功能来表示规则，它提供了一个用于对树结构进行变幻的通用框架，用来进行分析、规划和运行时代码生成。

> Spark SQL的组件

因为Spark SQL是一种类似与SQL的语言，非常容易上手，小强第一次使用就佩服这种简单操作和内存级别的运算速度。为了更好的使用Spark SQL，我们需要深入了解Spark SQL。

Spark SQL中的四大组件：SQL、Data Source Api、DataFrame Api和DataSet Api。

1、Spark SQL可以使用SQL语言向Hive表写入数据和从Hive表读取数据。SQL可以通过JDBC、ODBC或命令行在java、scala、python和R语言中使用。当在编程语言中使用SQL时，结果会转换为DataFrame。

2、Data Source Api为使用Spark SQL读取和写入数据提供了统一的接口。

3、DataFrame Api让大数据分析工作对各种用户更为简单易行。这个Api收到了R和Python中DataFrame的启发，但是它被设计用于大规模数据集的分布式处理，以支持现代大数据分析。当然了，DataFrame可以看作是对现有RDD Api的扩展，也是对RDD的之上的一种抽象。

4、DataSet Api结合了RDD和DataFrame的最大优点。DataSet会使用编码器将JVM对象转换为用Spark的二进制格式存储的Dataset表形式。

Dataset Api及其子集DataFrame Api将取代RDD Api成为主流的 APi。因为它通过Catalyst中进行的优化提供了更高的性能。

> 小结

小强介绍了Spark社区为什么引入Spark SQL、Spark SQL的整体架构以及Spark SQL包含的四大组件及其含义。今天算是带领大家入门Spark SQL，后续小强将会深入介绍Dataset和DataFrame，以及Spark SQL优化的实践干货。

> 【转发】和【关注】是对小强最大的支持！！！