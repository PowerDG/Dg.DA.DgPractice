# 《从0到1学习spark》--手撕parallelize源码

https://www.jianshu.com/p/894b33b6a56e



之前小强介绍了RDD是什么以及RDD的用法，如果还有疑惑的同学可以查看[《从0到1学习spark》-- RDD](http://mp.weixin.qq.com/s?__biz=MzU3NDc5NzMzNw==&mid=2247483795&idx=1&sn=658dedfeb05e610c900eba6f41f16cd2&chksm=fd2da2e5ca5a2bf333b937943d39f418e2ab4f7c6d065dcd9bf57898d586be31a5959340af25&scene=21#wechat_redirect)，今天小强将介绍一下RDD的使用和源码解析。

### 手撕RDD

RDD有两种，一种如上图所示的，使用parallelize方法创建的并行集合



![img](https:////upload-images.jianshu.io/upload_images/7187100-ada3966c4a659f6b?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

另外一种是外部存储创建的RDD,例如读取HDFS的内容。

http://spark.apache.org/docs/latest/rdd-programming-guide.html#resilient-distributed-datasets-rdds

关于spark RDD官网资料



![img](https:////upload-images.jianshu.io/upload_images/7187100-fea2dc89d38876df?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

这里在传参的时，也就是图片红色圈起来的方法，和函数体里面都有执行到assertNotStopped()这个方法，那么这里看一下具体的内容



![img](https:////upload-images.jianshu.io/upload_images/7187100-e12c7d31b709c321?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

找到parallelize方法，先看看withScope这个方法的作用，因为这里在进入到这个断点前会先进入到这个方法里面,这里梳理一下几个方法的执行顺序

首先因为defaultParallelism这个方法作为形参的结果返回，因此第一个执行也就是最开始执行的内容，然后第二个执行withScope，接着才是执行函数体里面的内容也就是assertNotStooped()和new 这里的内容



![img](https:////upload-images.jianshu.io/upload_images/7187100-5318aef8d3c1ac0e?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

这里会根据方法的注释可以知道，用户未指定时要使用的默认并行级别

那么这里默认级别是多少呢？还有这里是根据什么来设置的呢？

一直进入具体的方法



![img](https:////upload-images.jianshu.io/upload_images/7187100-053d6b6b073275eb?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

这里可以知道就是根据spark.default.parallelism这个参数来设置的，这里取两者的最大值



![img](https:////upload-images.jianshu.io/upload_images/7187100-5e56c20d318def00?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

另外这里可以看到这里返回的参数结果是2，这里参数部分执行完默认的并行度之后，接着就是执行withScope方法了，这里同样进入查看一下



![img](https:////upload-images.jianshu.io/upload_images/7187100-eb82cbfedbb87847?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

这里执行withScope，获取方法名称，然后再次调用withScope，但是这里的形参不一样



![img](https:////upload-images.jianshu.io/upload_images/7187100-b3d142f171c6745d?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

这里是对sc的一些属性进行设置，主要是对RDD的范围的获取

这里是一个柯里化的函数，柯里化是把接受多个参数的函数变换成接受一个单一参数（最初函数的第一个参数）的函数， 并且返回接受余下的参数而且返回结果的新函数的技术。

https://www.jianshu.com/p/8869c0777cbe

这里关于scala的函数的一些资料

https://blog.csdn.net/qq_21383435/article/details/79666170

关于spark  withScope的源码的含义，可以具体参考网上的资料

withScope是最近的发现版中新增加的一个模块，它是用来做DAG可视化的（DAG visualization on SparkUI）

以前的sparkUI中只有stage的执行情况，也就是说我们不可以看到上个RDD到下个RDD的具体信息。于是为了在sparkUI中能展示更多的信息。所以把所有创建的RDD的方法都包裹起来，同时用RDDOperationScope 记录 RDD 的操作历史和关联，就能达成目标



![img](https:////upload-images.jianshu.io/upload_images/7187100-6b404aafc2d2204f?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

然后这里执行完设置spark.rdd.scope的结果如上所示，关于withScope的内容这里因为涉及到其他模块，因此这里暂时只作为了解，后面有机会再详细研究。

然后执行完这里之后，就又回到了最前面的 parallelize



![img](https:////upload-images.jianshu.io/upload_images/7187100-5f6490f22d76d12f?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

然后这里进入查看一下



![img](https:////upload-images.jianshu.io/upload_images/7187100-da326a31a6d2c7d0?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

这里主要是继承了RDD，然后看下具体的执行过程



![img](https:////upload-images.jianshu.io/upload_images/7187100-d7192e9b5ab1fde1?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

这里主要的执行方法就是RDD.scala里面的内容了，可以看到这里涉及有checkpoint的内容

这个其实就是RDD的安全检查点，所谓的安全检查点其实是将系统运行的内存数据结构和状态持久化到磁盘当中，在需要时通过对这些吃就好数据的读取，重新构造出之前的运行期的状态



![img](https:////upload-images.jianshu.io/upload_images/7187100-2705d27e151b8365?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

这里有几个地方可以注意一下，第一个地方是指定了持久化级别的

第二个看注释是用于创建RDD的，然后这里sc.getCallSite()这个方法是和堆栈有关的，这部分内容在创建sparkContext中也有，可以看具体的相关内容

然后可以看到这里得到的RDDOperationScope就是一个jsonMapper和scopeCounter

这里主要内容其实还是这个jsonMapper，说白了其实RDD也是一个大的Mapper，只不过里面包含了很多其他的各种工具内容等等。

那么创建完RDD之后，这里数据在哪里呢？



![img](https:////upload-images.jianshu.io/upload_images/7187100-fbb13c2b8aa16293?imageMogr2/auto-orient/strip%7CimageView2/2/w/830)

image

就是在这个body里面了

### 总结

今天小强介绍了RDD通过parallelize方法并行化创建的源码执行流程，欢迎大家在后台拍砖，让我们一起学习spark。

【关注】和【点赞】是对小强最大的支持！！！