







# DDD聚合五种设计方法



https://www.jdon.com/51180

​                                     18-12-24                                      				  [                     banq](https://www.jdon.com/blog/banq)                 

​                 

#形式逻辑     
                
                    #DDD领域驱动设计     
                
                    #DDD聚合     
                
                    #事务架构     
                

​                聚合是啥？聚合就是整体与部分的组合，这里推荐一篇Szymon Kulec英文文档，点击标题进入后可获得实现聚合的五种规则，该文档大意翻译如下：我第一次阅读领域驱动设计（DDD）的蓝皮书时，它改变了我对业务领域的看法。一开始，我认为这种新方法纯粹是技术性的。我尝试按照规定应用建模，以“DDD”或“非-DDD”的黑白态度处理每个解决方案，就像之间没有其他任何东西一样。在接下来的几年里，这种方法变得越来越模糊。毕竟，DDD就像任何其他方法/范例一样，你可以选择你想要使用的工具并从中获得一些东西。即使您不使用DDD（再次，没有黑白解决方案），有用的工具之一就是使用基于聚合的思维对您的解决方案进行建模。我认为基于聚合思维的术语是什么意思？我指的是使用建模技术使您的解决方案的某些部分独立，可能会在以后的微/纳米或任何大小的服务中嵌入。只需看看技术的景观及其不同的部分，例如公共云或现代数据库。即使不使用“完全DDD”，如果以正确的方式绘制原子部件的边界，您的解决方案仍将获得更多。而且，正确的方法是什么？是否有任何规则要遵循？我鼓励你继续阅读并学习其中的一些内容。现在是时候访问你不想 破坏的5个聚合规则。

 **1.聚合是事务边界**

每当您发现域的两个元素紧密结合在一起时，您就会发现潜在的聚合。根据使用的方法，聚合可以存储为： 文档，如果您使用文档数据库 实体ER图，如果使用某种类型的ORM存储聚合或者手动编写SQL   事件流，如果使用事件源来捕获聚合历史记录的所有业务更改 无论使用何种存储机制，它们都共享一个共同的属性。此属性是包装为存储聚合状态而执行的存储操作的事务。是的，我故意使用相同的术语“交易”来描述：业务操作和存储操作，因为它们真的是一样的。无论您使用哪种存储机制，一起操作的东西都将存储在一起。当然，我们可以讨论存储实现的优缺点，但这并没有改变事务性的事实。 *找到必须一起更改的项目，您将找到聚合的一部分。* 

**2.把聚合设计得大一些**

在设计聚合时可以犯的一个常见错误是将所有内容切割成尽可能小的部分。您可以想象每个聚合只存储一个值是什么样？如果分开的部分之间存在某种相互作用，您将需要以某种方式处理它。“只是调用聚合的方法”等常用方法将不再有效，因此将使用事件投影、流程管理器和Saga来处理这两个或更多步骤流程。每次将聚合体分成较小的部分时，请问自己是否在切割部件之间的某些重要关系。比如在建模时，Peter发现用户每次在聚合帐户结算上执行操作时，都需要使用另一个名为Balance的聚合。在将它们合并到模型中之后，使用属于这个新的单个聚合的数据，在没有额外异步通信的情况下就可执行所有操作。

 **3.使聚合尽可能小**

阅读上一部分后，人们可能会认为制作大型聚合总是一个好主意。我经常使用的一个反例是创建一个名为The System，The Service或The Module的超级聚合。由于聚合需要以原子方式更新，因此您有两种处理事务的方法：乐观和悲观并发。使用乐观并发意味着尝试更新/附加聚合数据，检查版本是否在后台不会更改。很容易想象，即使有两个用户在The System中积极工作，也很容易导致这些版本不匹配。使用悲观并发意味着无论何时想要对聚合执行操作，都需要以某种方式锁定它。锁定聚合通常会保留其边界。这意味着，使用的锁是粗粒度锁，它将聚合作为一个整体锁定。在乐观并发/锁定的情况下，机制有点不同。从存储中获取聚合时，也会获得其版本。一旦操作在内存中执行并且状态更新，它将有条件地更新，并附加一个子句检查以确保版本没有更改。如果是，则发生错误并且应该尝试执行操作。在两种并发情况下，只有一个actor可以一次执行一个操作。这意味着，有更细粒度的聚合，您的系统将能够执行的操作越多，反过来，吞吐量就越高。如你所见，有两种相反的力量。一种是尝试使聚合物尽可能大，另一种 - 使它们尽可能小。由您和您使用的模型决定如何拆分实体以及如何选择聚合边界。 

**4. 尽可能使用time-bounded时间维度范围内的聚合**

每当您为与时间紧密相关的领域建模时，寻找有时间范围限制的聚合！。例如：建模“医生预约”，有时间表或周计划。你怎么设计这种有时间限制的聚合？首要的是为您的聚合找到合适的时间粒度。让我们考虑医生预约的例子。通常，约会不太可能需要一个多小时。另一方面，患者通常会在特定日期搜索访问并尝试提前一天或一天后移动（至少这是我使用的算法）。这种聚合的自然时间边界将是一天。考虑到这一点，您可以将特定医生的每个工作日建模为单独的聚合，例如：对于ID为doc123的医生，您将创建一个ID为doc123-2019-Jan-02的聚合，以处理1月2日的所有访问。

 **5.翻转主谓宾句子直至做对了**

让我们考虑以下句子：用户正在订购一本书。你想到的第一个元素是什么？模型能够支持这种操作。是用户吗？以下句子怎么样：一本书是由用户订购的；还有这一个：用户下了一本书的订单。（banq注：主语更换了），最后一个是相当正常的，但是所有三个都描述了相同的操作，然而，表现出不同的语言表达。让我们讨论不同的模型以及它们可以代表什么。在第一个示例中，用户正在订购书籍，可以模拟表示用户的单个聚合。这似乎很自然，因为它匹配执行订单的自然人。这个聚合体的大小怎么样？不是太大了吗？如果用户购买了数千本书怎么办？我们真的想将这些信息整合在一起吗？以下操作是否取决于订购历史记录？我会说，这不太可能。您可能希望不时显示历史记录，但没有操作需要整个历史记录来验证是否可以执行该历史记录。在第二个例子中，一本书是由用户订购的，人们可以想到一个书籍聚合，其中包含订购了这本书的所有用户的所有订单。我们真的需要这种历史吗？当然有人可能会争辩说我们需要保留我们拥有的副本数量，但通常情况并非如此。今天，电子商店出售商品，即使他们现在没有库存。因此，不需要在一个巨大的聚合中聚合所有内容。对于最后一个示例，用户下了一本书的订单。现在，所有与同一订单相关的信息都放在一个地方。聚合很小，并为每个订单创建一个新的聚合！根据需要添加用户信息和订单行（banq注：这个合适！）案例：Fumika正在尝试提炼模型，在得出结论之前，她尝试使用描述需求的翻转主谓宾的句子来找到符合系统要求的最佳边界。花了一些时间后，她发现了一个合理大小的聚合时间限制（因为她处理某种调度系统）。

#形式逻辑     
                
                    #DDD领域驱动设计     
                
                    #DDD聚合     
                
                    #事务架构     
                



​       3

[赞](javascript:digMessage('23150566'))     



​                                    				  [                     songyang](https://www.jdon.com/blog/songyang)                 

​                     2018-12-26 15:43

​                 

​           对于聚合让我感到有些困惑在IDDD的第十章中通过唯一标识符引用其他聚合对一个臃肿的聚合进行优化而在后文又说 使用唯一标识符来引用对象的缺点在于组装多个聚合并显示给用户界面变得非常困难并给出两种解决方案 CQRS和theta-join那么会延伸出两个问题1，那么通过theta-join查询出的数据对象在DDD领域里处于一个什么位置？2，如果使用标识符来引用其他对象，那么你这个聚合是否还能保证边界清晰。打个比方：产品 和 产品分类 两个聚合产品通过唯一标识符引用产品分类那么我对产品分类这个聚合进行删除操作，那么如何保证产品的数据的一致性





​                                    				  [                     banq](https://www.jdon.com/blog/banq)                 

​                     2018-12-26 16:01

​                 

#                  >通过唯一标识符引用其他聚合对一个臃肿的聚合进行优化按照Evans逻辑，一个聚合是不可直接引用另外一个聚合，但是可以将另外一个聚合的唯一标识作为值对象的一部分，将ID作为值来对待。当对产品分类这个聚合进行删除操作，删除的是产品分类和产品ID的关系表，删除了关系，但是没有删除这个分类下的所有产品，这是两个聚合应该出现的正常情况。如果需求想删除分类后，删除所有产品，从这句话的语义分析你已经得到，产品是重点，是聚合根，分类只是对产品的特征说明描述的值而已，那么久不应该设计两个聚合：产品聚合与分类聚合，而是一个聚合：产品，分类只是产品的值对象而已。