





#                   [Linq的优缺点](https://www.cnblogs.com/tianboblog/p/5424157.html)              

https://www.cnblogs.com/tianboblog/p/5424157.html

**优点：**


1.Linq提供了不同数据源的抽象层，所以可以使用相同的语法访问不同的数据源（只要该数据源有提供程序即可）


2.Linq为底层的数据存储提供了一个强类型化的界面，可以把底层的数据作为对象来访问。


3.推迟查询的执行。在运行期间定义的查询表达式时，查询不会运行。查询会在迭代数据项时运行。（把复杂的查询进行拆分，而不会影响查询效率；使代码清晰易懂）

4.Linq 语句是在编译期间就做检查的。而不是运行时检查。这样，那里出了问题，可以及时更改，而不是到了运行时才发

# LINQ TO SQL 有什么优缺点啊？

https://zhidao.baidu.com/question/213349272.html

 首先，在了解 LINQ To SQL 有什么优点之前，我们有必要首先了解下，微软为什么弄了这么个东西。 搞出这个东西来有什么目的：——当然是为了  满足不知道怎么操作数据的程序员开发设计的，并不是每个程序员 都会直接操作数据库，LinQ  可以让他们以一种面向数据对象的方式来思考，及持久化他们的数据！

好处：   容易学习，书写简单。 在开发 中小型 项目 的时候推荐使用！因为可以节省时间！
          它可以很方便的调用 存储过程、[SQL函数](https://www.baidu.com/s?wd=SQL函数&tn=SE_PcZhidaonwhc_ngpagmjz&rsv_dl=gh_pc_zhidao)

缺点：由于直接封装了所有的数据持久操作。导致批量持久数据会产生效率问题
      尤其体现在批量跟新数据，它会在内存中保持大量的数据模型。

总结：中小型 项目 就放心用吧！  不过从技术 储备的角度来说，建议 看看entity framework   





###                                                                   [Linq到底有什么优点？项目中到](https://bbs.csdn.net/topics/310170372?list=982381)底应该不应该用它？                                 [问题点数：20分，结帖人poiuy1363]                    

假设你使用 Linq to SQL，当你使用它，你就无需像有些有着巨大的闲工夫的人那样写所谓“三层”代码，你无需写DAL层，而使用Linq to SQL就足够了。你直接写业务逻辑，甚至直接在表现层里使用Linq to SQL。Linq to SQL不但给你将所有对象的操作都管理起来，而且也相当大程度上可以移植（你几乎只需要切换另外一种DataContext）。