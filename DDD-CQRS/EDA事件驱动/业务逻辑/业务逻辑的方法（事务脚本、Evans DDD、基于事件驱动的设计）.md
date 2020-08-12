[业务逻辑的方法（事务脚本、Evans DDD、基于事件驱动的设计）](https://www.cnblogs.com/Leo_wl/archive/2011/06/22/2086586.html)



##  [业务逻辑的方法 



​          [业务逻辑的方法（事务脚本、Evans DDD、基于事件驱动的设计）](https://www.cnblogs.com/Leo_wl/archive/2011/06/22/2086586.html)           	

废话不多说了，本文的目的是希望通过一个“银行转账”的例子来和大家分享一些我最近学习 到的关于如何组织业务逻辑的心得和体会。当然，本人的能力和领悟有限，如有不正确之处，还希望各位看官能帮我指出来。我始终坚持一个信念，没有讨论就没有 进步，任何一个非盈利为目的的人或组织始终应该把自己所学的知识共享出来与人讨论，这样不管对自己或对他人或对整个社会都大有好处。因为一个人的知识毕竟 是有限的，但可以（并且也只能）和别人相互沟通交流学习来弥补这个缺陷。

银行转账的核心业务逻辑大家应该都很熟悉了，主要有这么几步：

1. 源账户扣除转账金额，当然首先需要先判断源账户余额是否足够，如果不够，则无法转账；
2. 目标账户增加转账金额；
3. 为源账户生成一笔转账记录；
4. 为目标账户生成一笔转账记录；

下面让我们来看看各种实现该业务逻辑的方法，并且来做一个对比。

**事务脚本（Transaction Script、贫血模型）** 

这种方法的优缺点网上找一下一大堆，我这里也啰嗦列举一些：

1. 容易理解，符合我们大脑过程化思考的习惯；
2. 完全没有面向对象的思想，纯粹是面向过程式的一种组织业务逻辑的方式，所有的业务逻辑全部在一个方法中完成；
3. 对象只包含数据而没有行为，对象只是用来被操作的“数据”，一般我们会设计很多的Item，以及ItemManager；
4. 结构层次比较清晰，业务逻辑层和其他各层之间单项依赖；业务逻辑层中Item只代表数据，ItemManager则负责所有的业务逻辑实现，ItemManager只依赖于IDAL接口来完成持久化Item或重建Item； 
5. 由 于所有的业务逻辑全部写在一个方法内，如果有另外一个需求也需要类似的业务逻辑，通常我们是写一个新的方法来实现，这样就很容易导致相同的业务逻辑出现在 两个方法中，导致可维护性降低；虽然可以用一些重构的技巧或设计模式来解决重用的问题，但这往往需要开发人员具有很高的编码水平，并且往往很多时候因为时 间紧迫导致不允许我们花很多时间去重构；
6. 如果业务逻辑一旦改变，我们必须去修改实现该业务逻辑的方法，并且如果该业务逻辑在多个方法中出现，我们必须同时修改多个方法；

演示代码：

[![复制代码](copycode.gif)

```csharp
public class BankAccountManager
    {
        private IBankAccountDAL bankAccountDAL;

        public BankAccountManager(IBankAccountDAL bankAccountDAL)
        {
            this.bankAccountDAL = bankAccountDAL;
        }

        /// <summary>
        /// 该方法完成转账业务逻辑
        /// </summary>
         public void TransferMoney(Guid fromBankAccountId, Guid toBankAccountId, double moneyAmount)
        {
            var fromBankAccount = bankAccountDAL.GetById(fromBankAccountId);
            var toBankAccount = bankAccountDAL.GetById(toBankAccountId);
            if (fromBankAccount.MoneyAmount < moneyAmount)
            {
                throw new NotSupportedException("账户余额不足。");
            }
            fromBankAccount.MoneyAmount -= moneyAmount;
            toBankAccount.MoneyAmount += moneyAmount;

            DateTime transferDate = DateTime.Now;
            fromBankAccount.TransferHistories.Add(new TransferHistory
            {
                FromAccountId = fromBankAccountId,
                ToAccountId = toBankAccountId,
                MoneyAmount = moneyAmount,
                TransferDate = transferDate
            });
            toBankAccount.TransferHistories.Add(new TransferHistory
            {
                FromAccountId = fromBankAccountId,
                ToAccountId = toBankAccountId,
                MoneyAmount = moneyAmount,
                TransferDate = transferDate
            });
        }
    }
    /// <summary>
    /// 银行帐号
    /// </summary>
    public class BankAccount
    {
        public BankAccount() { this.TransferHistories = new List<TransferHistory>(); }
        public Guid Id { get; set; }
        public double MoneyAmount { get; set; }
        public IList<TransferHistory> TransferHistories { get; set; }
    }
    /// <summary>
    /// 转账记录
    /// </summary>
    public class TransferHistory
    {
        public Guid FromAccountId { get; set; }
        public Guid ToAccountId { get; set; }
        public double MoneyAmount { get; set; }
        public DateTime TransferDate { get; set; }
    }
    public interface IBankAccountDAL
    {
        BankAccount GetById(Guid bankAccountId);
    }
}
```



**Evans DDD（充血模型）**

这种方法的特点在网上也可以找到很多，但我也有一些其他自己的看法，见红色字体的部分：

1. 基本是一种基于OO思想的开发方法，对象既有属性也有行为，对象之间通过相互引用和方法调用来完成对象之间的交互；
2. 由于这是一种OO思想的设计方法，所以各种设计原则和模式都可以被充分利用；
3. Evans对这种开发方法又作了进一步的完善，提出了：聚合、实体、值对象、服务、工厂、仓储、上下文，等这些概念；这确保我们在基于OO的思想组织业务逻辑时有了很好的指导思想；
4. 需要特别指出的一点是，真正的Evans的DDD领域模型中的聚合根所内聚的所有值对象应该都是只读的，这一点特别重要。
5. 基 于Evans  DDD的CQRS架构。这种架构的主要思想是将命令和查询分离，另一个重要的特点就是事件溯源，意思是领域对象不需要有公共的属性，只需要有行为即可，并 且在任何一个行为发生后，都会触发一个事件。然后我们持久化的不是对象的状态，而是引起该对象状态改变的所有的事件。当我们需要重建一个领域对象时，只要 先创建一个干净的只有唯一标识的对象，然后把和该对象相关的所有领域事件全部重新执行一遍，这样我们就得到了该对象的最终的状态了。说的简单点，就是我们 不保存对象本身，而是只保存该对象的操作历史（或者叫操作日志），当我们需要重建该对象时只要”重演历史“即可。当然，为了避免性能的问题，比如因为一个 对象可能会有很多的操作历史，如果每次重建该对象都是从头开始应用每个事件，那效率无疑是非常低的。因此我们使用了快照，快照保存了对象某个时刻的二进制 形式（即被序列化过了）的状态。所以通常情况下，当我们要重建一个对象时都是从某个最近的快照开始回溯发生在快照之后的事件。
6. 不 管是Evans的DDD也好，CQRS架构也好，虽然都做到了让领域对象不仅有状态，而且有行为，但我觉得这还不够彻底。因为对象的行为总是“被调用” 的，当现在有一个业务逻辑需要调用多个对象的一些行为来完成时，我们往往会一个一个地将对象从仓储中取出来，然后调用它们的方法。虽然Evans提出了领 域服务（Service）的概念，并将一个领域对象不能完成的事情交给了领域服务去完成。但领域服务内部还是在一个个的取出对象然后调用它们的方法。这个 做法在我看来和凭血模型没有本质区别，还是没有真正做到OO。因为贫血模型的情况下，对象是提供了数据让别人去操作或者说被别人使用；而充血模型的情况 下，对象则是提供了数据和行为，但还是让别人去操作或者说被别人使用（数据被别人使用或方法被别人调用都是“被别人操作”的一种被动的方式）。所以从这个 意义上来看对象时，我觉得贫血模型和充血模型没有本质区别。

 下面也给出一个实现了银行转账业务逻辑的充血模型实现：

```csharp
/// <summary>
    /// 银行帐号, 它是一个Evans DDD中的实体, 并且是聚合根
    /// </summary>
    public class BankAccount
    {
        private IList<TransferHistory> transferHistories;

        public BankAccount() : this(Guid.NewGuid(), 0D, new List<TransferHistory>()) { }
        public BankAccount(Guid id, double moneyAmount, IList<TransferHistory> transferHistories)
        {
            this.Id = id;
            this.MoneyAmount = moneyAmount;
            this.transferHistories = transferHistories;
        }
        public Guid Id { get; private set; }
        public double MoneyAmount { get; private set; }
        public IList<TransferHistory> TransferHistories
        {
            get
            {
                return transferHistories.ToList().AsReadOnly();
            }
        }

        public void TransferTo(Guid toBankAccountId, double moneyAmount, DateTime transferDate)
        {
            if (this.MoneyAmount < moneyAmount)
            {
                throw new NotSupportedException("账户余额不足。");
            }
            this.MoneyAmount -= moneyAmount;
            this.TransferHistories.Add(
                new TransferHistory(this.Id, toBankAccountId, moneyAmount, transferDate));
        }
        public void TransferFrom(Guid fromBankAccountId, double moneyAmount, DateTime transferDate)
        {
            this.MoneyAmount += moneyAmount;
            this.TransferHistories.Add(
                new TransferHistory(fromBankAccountId, this.Id, moneyAmount, transferDate));
        }
    }
    /// <summary>
    /// 转账记录, 它是一个Evans DDD中的值对象
    /// </summary>
    public class TransferHistory
    {
        public TransferHistory(Guid fromAccountId,
                               Guid toAccountId,
                               double moneyAmount,
                               DateTime transferDate)
        {
            this.FromAccountId = fromAccountId;
            this.ToAccountId = toAccountId;
            this.MoneyAmount = moneyAmount;
            this.TransferDate = transferDate;
        }

        public Guid FromAccountId { get; private set; }
        public Guid ToAccountId { get; private set; }
        public double MoneyAmount { get; private set; }
        public DateTime TransferDate { get; private set; }
    }
    /// <summary>
    /// BankAccount聚合根对应的仓储
    /// </summary>
    public interface IBankAccountRepository
    {
        BankAccount GetBankAccount(Guid bankAccountId);
    }
    /// <summary>
    /// 转账服务, 它是一个Evans DDD中的领域服务
    /// </summary>
    public class BankAccountService
    {
        private IBankAccountRepository bankAccountRepository;

        public BankAccountService(IBankAccountRepository bankAccountRepository)
        {
            this.bankAccountRepository = bankAccountRepository;
        }

        /// <summary>
        /// 该方法完成转账业务逻辑
        /// </summary>
        public void TransferMoney(Guid fromBankAccountId, Guid toBankAccountId, double moneyAmount)
        {
            var fromBankAccount = bankAccountRepository.GetBankAccount(fromBankAccountId);
            var toBankAccount = bankAccountRepository.GetBankAccount(toBankAccountId);

            DateTime transferDate = DateTime.Now;
            fromBankAccount.TransferTo(toBankAccountId, moneyAmount, transferDate);
            toBankAccount.TransferFrom(fromBankAccountId, moneyAmount, transferDate);
        }
    }
```





**基于事件驱动的设计**

这是一种根据我自己的想法而设计出来的一种设计与实现，但是离我理想中的设计还有一些距离。在我看来，真正理想的组织业务逻辑的方法或者说模型应该是这样的：

1. 当外界需要领域逻辑的“实现模型”（简称领域模型）做某件事情时，会发出一个命令，这个命令可以理解为一个消息或者是一个事件。消息一旦创建出来后就是只读的，因为消息从某种程度上来说就是历史；
2. 领域模型中的相关领域对象会主动响应该消息；
3. 需 要特别指出的是：我们不可以自己去获取一些相关的领域对象，然后进一步调用它们的方法而实现响应；而是应该所有可能被用到的领域对象必须好像永远已经存在 于内存一样的永远在不停的在等待消息并作出响应。以银行转账作为例子，外界发出一个转账的消息，该消息会包含源帐号唯一标识、目标帐号唯一标识、转账金额 这些信息。该消息的目的是希望两个两个银行帐号之间能进行转账。好了，外界要做的仅仅是发出这条消息即可。那么领域模型内部该如何去响应该消息呢？一种方 法是将两个银行帐号先取出来，然后调用它们的转账方法（如TransferTo方法和TransferFrom方法）以实现转账的目的，前面的Evans 的DDD的例子就是这样实现的。但这样做已经违反了我前面所说的理想的情况了。我的理想要求是，这两个银行帐号对象会像已经存在于内存一样可以直接主动去 响应转账的消息，而不是转账的那两个方法（TransferTo方法和TransferFrom方法）被我们自己定义的领域服务所调用。
4. 更加需要着重强调的是，我始终认为，真正的面向对象编程中的对象应该是一个”活“的具有主观能动性的存在于内存中的客观存在，它们不仅有状态而且还有自主行为。这 里需要从两方面来解释：1）对象的状态可以表现出来被别人看到，但是必须是只读的，没有人可以直接去修改一个对象的状态，因为对象是一个在内存中的有主观 意识的客观存在，它的状态必须是由它自己的行为导致自己的状态的改变。就好像现实生活中的动物或人一样，我不能强制你做什么事情，一定是我通知你（即发送 消息给你），你才会做出响应并改变你自己的状态。2）对象的行为就是对象所具有的某种功能。对象的行为本质上应该是对某个消息的主动响应，这里强调的是主 动，就是说对象的行为不可以被别人使用，而只能自己主动的去表现出该行为。另外，行为可以表现出来给别人看到，也可以不表现出来给别人看到。实际上，我们 永远都不需要将对象的行为表现出来给别人看到，原因是别人不会去使用该行为的，行为永远只能是对象自己去表现出来。
5. 领域模型这个生态系统中的各个领域对象在运行过程中如果需要和领域模型之外的东西（如数据持久层）交互，也应该通过消息来进行，因为只有这样才能确保领域对象是一个”活“的具有主观能动性的存在于内存中的客观存在。

以 上就是我心目中理想的如何设计对象来实现业务逻辑的方式。我想了很久，要完全实现上面的目标实在是太困难了。但也不是不可能，我按照我的能力，经过不断的 设计、编码、测试、重构的反复循环过程。基本上设计出了一个令自己基本满意的基础框架出来，基于该框架，以银行转账为例子，我们可以以如下的方式来实现：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

  1     public class TransferEvent : DomainEvent
  2     {
  3         public TransferEvent(Guid fromBankAccountId, Guid toBankAccountId, double moneyAmount, DateTime transferDate)
  4         {
  5             this.FromBankAccountId = fromBankAccountId;
  6             this.ToBankAccountId = toBankAccountId;
  7             this.MoneyAmount = moneyAmount;
  8             this.TransferDate = transferDate;
  9         }
 10         public Guid FromBankAccountId { get; private set; }
 11         public Guid ToBankAccountId { get; private set; }
 12         public double MoneyAmount { get; private set; }
 13         public DateTime TransferDate { get; private set; }
 14     }
 15     public class BankAccount : DomainObject<Guid>
 16     {
 17         #region Private Variables
 18 
 19         private List<TransferHistory> transferHistories;
 20 
 21         #endregion
 22 
 23         #region Constructors
 24 
 25         public BankAccount(Guid customerId)
 26             : this(customerId, 0D, new List<TransferHistory>())
 27         {
 28         }
 29         public BankAccount(Guid customerId, double moneyAmount, IEnumerable<TransferHistory> transferHistories)
 30             : base(Guid.NewGuid())
 31         {
 32             this.CustomerId = customerId;
 33             this.MoneyAmount = moneyAmount;
 34             this.transferHistories = new List<TransferHistory>(transferHistories);
 35         }
 36 
 37         #endregion
 38 
 39         #region Public Properties
 40 
 41         public Guid CustomerId { get; private set; }
 42         [TrackingProperty]
 43         public IEnumerable<TransferHistory> TransferHistories
 44         {
 45             get
 46             {
 47                 return transferHistories.AsReadOnly();
 48             }
 49         }
 50         [TrackingProperty]
 51         public double MoneyAmount { get; private set; }
 52 
 53         #endregion
 54 
 55         #region Event Handlers
 56 
 57         private void TransferTo(TransferEvent evnt)
 58         {
 59             if (this.Id == evnt.FromBankAccountId)
 60             {
 61                 DecreaseMoney(evnt.MoneyAmount);
 62                 transferHistories.Add(
 63                     new TransferHistory(
 64                         evnt.FromBankAccountId,
 65                         evnt.ToBankAccountId,
 66                         evnt.MoneyAmount,
 67                         evnt.TransferDate));
 68             }
 69         }
 70         private void TransferFrom(TransferEvent evnt)
 71         {
 72             if (this.Id == evnt.ToBankAccountId)
 73             {
 74                 IncreaseMoney(evnt.MoneyAmount);
 75                 transferHistories.Add(
 76                     new TransferHistory(
 77                         evnt.FromBankAccountId,
 78                         evnt.ToBankAccountId,
 79                         evnt.MoneyAmount,
 80                         evnt.TransferDate));
 81             }
 82         }
 83 
 84         #endregion
 85 
 86         #region Private Methods
 87 
 88         private void DecreaseMoney(double moneyAmount)
 89         {
 90             if (this.MoneyAmount < moneyAmount)
 91             {
 92                 throw new NotSupportedException("账户余额不足。");
 93             }
 94             this.MoneyAmount -= moneyAmount;
 95         }
 96         private void IncreaseMoney(double moneyAmount)
 97         {
 98             this.MoneyAmount += moneyAmount;
 99         }
100 
101         #endregion
102     }
103     public class TransferHistory : ValueObject
104     {
105         #region Constructors
106 
107         public TransferHistory(Guid fromAccountId,
108                                Guid toAccountId,
109                                double moneyAmount,
110                                DateTime transferDate)
111         {
112             this.FromAccountId = fromAccountId;
113             this.ToAccountId = toAccountId;
114             this.MoneyAmount = moneyAmount;
115             this.TransferDate = transferDate;
116         }
117 
118         #endregion
119 
120         #region Public Properties
121 
122         public Guid FromAccountId { get; private set; }
123         public Guid ToAccountId { get; private set; }
124         public double MoneyAmount { get; private set; }
125         public DateTime TransferDate { get; private set; }
126 
127         #endregion
128 
129         #region Infrastructure
130 
131         protected override IEnumerable<object> GetAtomicValues()
132         {
133             yield return FromAccountId;
134             yield return ToAccountId;
135             yield return MoneyAmount;
136             yield return TransferDate;
137         }
138 
139         #endregion
140     }

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

以上代码是转账事件、银行帐号（实体），以及转账记录（值对象）的实现代码，然后我们可以通过如下的方式来触发TransferEvent事件来让银行帐号”自动“响应。

1 EventProcesser.ProcessEvent(new TransferEvent(bankAccount1.Id, bankAccount2.Id, 1000, DateTime.Now));

如果不需要增加其他的任何代码就OK了的话，那可就真美了，应该差不多可以实现我上面的目标了。但理想终归是理想，而现实的情况是：

1）领域对象的行为不可能做到别人不去调用它就能自己主动表现出来的地步，毕竟它不是一个真正的”活“的有主观能动性的人或动物；

2）领域对象并没有存在于内存中，而是在数据持久化介质中，如数据库，因此我们必须去把领域对象从数据库取出来；

那么难道我们只能放弃了吗？只能自己去做这两件事情了吗？不是，我们可以告诉基础框架如下一些信息，有了这些信息，基础框架就可以帮助我们完成上面的这两件事情了。

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 1     RegisterObjectEventMappingItem<TransferEvent, BankAccount>(
 2         new GetDomainObjectIdEventHandlerInfo<TransferEvent>
 3         {
 4             GetDomainObjectId = evnt => evnt.FromBankAccountId,
 5             EventHandlerName = "TransferTo"
 6         },
 7         new GetDomainObjectIdEventHandlerInfo<TransferEvent>
 8         {
 9             GetDomainObjectId = evnt => evnt.ToBankAccountId,
10             EventHandlerName = "TransferFrom"
11         }
12     );

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

上 面的代码的意思是告诉框架1）BankAccount会去响应TransferEvent事件；2）BankAccount对象的唯一标识是从 TransferEvent事件中的哪个属性中来的；3）因为这里BankAccount会有两个方法可能会响应TransferEvent事件，所以还 指定了响应方法的名字从而可以区分。当然一般情况下，我们是不需要指定方法的名字的，因为大部分情况下一个对象对同一个事件只会有一个响应方法。比如下面 的代码列出了很多中常见的事件与响应对象的映射信息：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 1     public class DomainLayerObjectEventMapping : ObjectEventMapping
 2     {
 3         protected override void InitializeObjectEventMappingItems()
 4         {
 5             //BankAccount Event Mappings.
 6             RegisterObjectEventMappingItem<DepositAccountMoneyEvent, BankAccount>(evnt => evnt.BankAccountId);
 7             RegisterObjectEventMappingItem<WithdrawAccountMoneyEvent, BankAccount>(evnt => evnt.BankAccountId);
 8             RegisterObjectEventMappingItem<TransferEvent, BankAccount>(
 9                 new GetDomainObjectIdEventHandlerInfo<TransferEvent>
10                 {
11                     GetDomainObjectId = evnt => evnt.FromBankAccountId,
12                     EventHandlerName = "TransferTo"
13                 },
14                 new GetDomainObjectIdEventHandlerInfo<TransferEvent>
15                 {
16                     GetDomainObjectId = evnt => evnt.ToBankAccountId,
17                     EventHandlerName = "TransferFrom"
18                 }
19             );
20 
21             //Topic Event Mappings.
22             RegisterObjectEventMappingItem<DomainObjectAddedEvent<Reply>, Topic>(evnt => evnt.DomainObject.TopicId);
23             RegisterObjectEventMappingItem<DomainObjectRemovedEvent<Reply>, Topic>(evnt => evnt.DomainObject.TopicId);
24 
25             //ForumUser Event Mappings.
26             RegisterObjectEventMappingItem<PreAddDomainObjectEvent<Topic>, ForumUser>(evnt => evnt.DomainObject.CreatedBy);
27             RegisterObjectEventMappingItem<DomainObjectAddedEvent<Topic>, ForumUser>(evnt => evnt.DomainObject.CreatedBy);
28 
29             //Reply Event Mappings.
30             RegisterObjectEventMappingItem<DomainObjectRemovedEvent<Topic>, Reply>(evnt => Repository.Find<Reply>(new FindTopicRepliesEvent(evnt.DomainObject.Id)));
31         }
32     }

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

关于这种组织业务逻辑的方法，大家如果有仔细研究的兴趣，可以下载我的框架源代码和聚合演示例子源代码。

 http://files.cnblogs.com/netfocus/EventBasedDDDExample.rar 

好了，大家觉得这三种组织业务逻辑的方法如何呢？很想听听大家的声音。我是一个喜欢思考问题、寻找真理的人，期望能和大家多多交流。 

 介绍了我设计的**基于“事件”驱动的领域模型的基础框架**

1. 任何一个领域对象是**“活”**的， 它不仅有属性（对象的状态），而且有方法（对象的行为）。为什么说是“活”的呢？因为领域对象的行为都不是被另外的领域对象调用的，而是自己去响应一些 “事件”  ，然后执行其自身的某个行为的。在我看来，如果一个领域对象的方法是被其他的领域对象调用的，那这个对象就是“死”的，因为它没有主动地去参与到某个活动 中去。这里需要强调的一点是，领域对象只会更新它自己的状态，而不会更新其他领域对象的状态。
2. 所有的领域对象之间都是平等的，任何两个领域对象之间不会有任何引用的关系（如，依赖、关联、聚合、组合）；但是它们之间会存在数据上的关系，如一个对象会保留另外一个对象的唯一标识。
3. 领 域对象之间的交互和通信全部通过事件来完成，事件可以将所有的领域对象串联起来使它们能相互协作。除此之外，领域对象和外界的各种交互也通过事件完成。按 照Eric  Evans的理论，为了确保领域对象之间的概念完整性，需要有聚合及聚合根的概念，聚合根聚合了很多子的实体或值对象，或者还会关联其他的聚合根。另外， 每个聚合需要有一个仓储（Repository）来负责聚合的持久化和重建的职责。其实，我觉得要确保领域对象之间的概念完整性，除了通过聚合的方式之 外，还可以通过事件来确保。其实，用聚合来确保概念完整性是事物之间直接作用的反映；而用事件来确保概念完整性则是事物之间间接作用的反映。在用事件的方 式下，仓储也不再需要了，因为领域模型和外界的交互也是通过事件来完成的。 

虽然在前面那篇文章中提供了两个Demo用来展示框架的功能，但我想大家直接看Demo源代码还是比较累，并且不能直观的看到框架能做什么以及如何使用。因此，本篇文章打算举几个典型的例子来分析如何使用我的框架来解决各种典型的应用场景。

**应用场景1：银行转账**

银行转账的核心流程大家应该都很熟悉了，主要有这么几步：

1. 源账户扣除转账金额，当然首先需要先判断当前账户余额是否足够，如果不够，则无法转账。
2. 目标账户增加转账金额；
3. 为源账户生成一笔转账记录；
4. 为目标账户生成一笔转账记录；

下面看看如何通过事件来实现上面的应用场景：

首先定义一个转账的事件：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

1     public class TransferEvent : DomainEvent
2     {
3         public Guid FromBankAccountId { get; set; }
4         public Guid ToBankAccountId { get; set; }
5         public double MoneyAmount { get; set; }
6         public DateTime TransferDate { get; set; }
7     }

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

该事件定义了：源账户、目标账户、转账金额、转账时间四个信息；

然后看看银行帐号类的设计：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 1     public class BankAccount : DomainObject<Guid>
 2     {
 3         #region Constructors
 4 
 5         public BankAccount(Guid customerId) : base(Guid.NewGuid())
 6         {
 7             this.CustomerId = customerId;
 8         }
 9 
10         #endregion
11 
12         #region Public Properties
13 
14         public Guid CustomerId { get; private set; }
15         [TrackingProperty]
16         public double MoneyAmount { get; set; }
17 
18         #endregion
19 
20         #region Event Handlers
21 
22         private void TransferTo(TransferEvent evnt)
23         {
24             WithdrawMoney(evnt.MoneyAmount);
25 
26             CreateTransferHistory(evnt.FromBankAccountId,
27                                   evnt.FromBankAccountId,
28                                   evnt.ToBankAccountId,
29                                   evnt.MoneyAmount,
30                                   evnt.TransferDate);
31         }
32         private void TransferFrom(TransferEvent evnt)
33         {
34             DepositMoney(evnt.MoneyAmount);
35 
36             CreateTransferHistory(evnt.ToBankAccountId,
37                                   evnt.FromBankAccountId,
38                                   evnt.ToBankAccountId,
39                                   evnt.MoneyAmount,
40                                   evnt.TransferDate);
41         }
42 
43         #endregion
44 
45         #region Private Methods
46 
47         private void WithdrawMoney(double moneyAmount)
48         {
49             if (this.MoneyAmount < moneyAmount)
50             {
51                 throw new InvalidOperationException("账户余额不足。");
52             }
53             this.MoneyAmount -= moneyAmount;
54         }
55         private void DepositMoney(double moneyAmount)
56         {
57             this.MoneyAmount += moneyAmount;
58         }
59         private void CreateTransferHistory(Guid currentBankAccount,
60                                            Guid fromBankAccountId,
61                                            Guid toBankAccountId,
62                                            double moneyAmount,
63                                            DateTime transferDate)
64         {
65             TransferHistory transferHistory =
66                 new TransferHistory(
67                     fromBankAccountId,
68                     toBankAccountId,
69                     moneyAmount,
70                     transferDate);
71 
72             Repository.Add(transferHistory);
73 
74             EventProcesser.ProcessEvent(
75                 new AddAccountTransferHistoryEvent
76                 {
77                     BankAccountId = currentBankAccount,
78                     TransferHistory = transferHistory
79                 });
80         }
81 
82         #endregion
83     }

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

BankAccount是一个领域对象，TransferTo和TransferFrom是两个事件的响应函数。目前为止，我们只需要知道：1）TransferTo方法会自动被源帐号对象调用，2）TransferFrom方法会自动被目标帐号对象调用。

最后，如何来通知领域模型进行转账操作呢？很简单，只要触发TransferEvent事件即可：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

1     EventProcesser.ProcessEvent(
2         new TransferEvent {
3             FromBankAccountId = bankAccount1.Id,
4             ToBankAccountId = bankAccount2.Id,
5             MoneyAmount = 1000,
6             TransferDate = DateTime.Now
7         }
8     );

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

上面的代码通知中央事件处理器处理一个转账的事件。 

好 了，理想情况下，如果只要上面的这样三段代码就能完成转账的业务场景了，那就太好了。但是那时不可能的，因为还有一个很重要的信息没有告诉框架，那就是框 架还不知道源账号和目标账号的唯一标识，我们需要告诉框架源账号的唯一标识是从事件的那个属性中获取，目标帐号的唯一标识是从事件的那个属性中获取。如下 的代码体现了这点：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 1     RegisterObjectEventMappingItem<TransferEvent, BankAccount>(
 2         new GetDomainObjectIdEventHandlerInfo<TransferEvent>
 3         {
 4             GetDomainObjectId = evnt => evnt.FromBankAccountId,
 5             EventHandlerName = "TransferTo"
 6         },
 7         new GetDomainObjectIdEventHandlerInfo<TransferEvent>
 8         {
 9             GetDomainObjectId = evnt => evnt.ToBankAccountId,
10             EventHandlerName = "TransferFrom"
11         }
12     );

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

上 面的代码表示，一个BankAccount对象会响应TransferEvent事件，并且会有两个方法会响应；“TransferTo”方法表示源账号 对TransferEvent事件的响应，“TransferFrom”方法表示目标帐号对TransferEvent事件的响应；另外，通过传递给框架 一个“GetDomainObjectId”委托函数来告诉框架，当前响应者的唯一标识。通过上面的四段代码，我们就能实现转账的应用场景了。可以看出， 转账的逻辑都在BankAccount对象中，而RegisterObjectEventMappingItem方法则是用来告诉框架 BankAccount对象的唯一标识是从TransferEvent事件中的那个属性中获取的。另外一般情况下，我们不需要指定事件响应函数的名字，但 由于这里一个对象对同一个事件有两个响应函数，则需要额外指定一个名字来告诉框架对应关系。

**应用场景2：论坛中帖子的回复对帖子的影响**

大家都知道，一个论坛的注册用户可以发表帖子，发表帖子的回复，或者是删除自己发表的某个回复。假设有如下的场景：帖子有一个属性表示它有多少个回复，当该帖子新增一个回复时，该属性值加1；当该帖子删除一个回复时，该属性值减1。

首先看一下帖子类：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 1     public class Topic : DomainObject<Guid>
 2     {
 3         #region Constructors
 4 
 5         public Topic(Guid createdBy, DateTime createDate, int totalReplyCount) : base(Guid.NewGuid())
 6         {
 7             this.CreatedBy = createdBy;
 8             this.CreateDate = createDate;
 9             this.TotalReplyCount = totalReplyCount;
10         }
11 
12         #endregion
13 
14         #region Public Properties
15 
16         public Guid CreatedBy { get; private set; }         //作者
17          public DateTime CreateDate { get; private set; }    //创建日期
18          [TrackingProperty]
19         public string Subject { get; set; }                 //标题
20          [TrackingProperty]
21         public string Body { get; set; }                    //消息内容
22         [TrackingProperty]
23         public int TotalMarks { get; set; }                 //点数
24         [TrackingProperty]
25         public int TotalReplyCount { get; set; }            //当前主题下的消息总数
26 
27         #endregion
28 
29         #region Event Handlers
30 
31         private void Handle(DomainObjectAddedEvent<Reply> evnt)
32         {
33             this.TotalReplyCount += 1;
34         }
35         private void Handle(DomainObjectRemovedEvent<Reply> evnt)
36         {
37             this.TotalReplyCount -= 1;
38         }
39 
40         #endregion
41     }

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

Topic类表示一个帖子，大家可以看到它响应两个事件DomainObjectAddedEvent<Reply>和DomainObjectRemovedEvent<Reply>，其中Reply类表示帖子的回复。

DomainObjectAddedEvent<TDomainObject> 和DomainObjectRemovedEvent<TDomainObject>这两个事件是由框架定义的泛型事件，用来表示某个领域对 象被创建了或被移除了。所以，DomainObjectAddedEvent<Reply>和 DomainObjectRemovedEvent<Reply>这两个事件就表示新增了一个帖子的回复的事件和移除了一个帖子的回复的事 件。

另外我们可以通过下面的代码来添加一个回复，或移除一个回复。

1 var reply1 = Repository.Add(new Reply(topic.Id) { Body = "A new topic reply1." }); //添加回复的代码
2 Repository.Remove(reply1); //移除回复的代码 

大家从上面的代码中看到了Repository，也就是仓储。其实这个类不是真正的仓储，因为它的内部实现也仅仅是做了“发布事件”的事情。换句话说，我这里的Repository只是帮我们做了发布一些通用典型事件的操作。可以看一下这两个方法的实现：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 1         public static TDomainObject Add<TDomainObject>(TDomainObject domainObject) where TDomainObject : class
 2         {
 3             EventProcesser.ProcessEvent(new PreAddDomainObjectEvent<TDomainObject> { DomainObject = domainObject });
 4             EventProcesser.ProcessEvent(new AddDomainObjectEvent<TDomainObject> { DomainObject = domainObject });
 5             EventProcesser.ProcessEvent(new DomainObjectAddedEvent<TDomainObject> { DomainObject = domainObject });
 6             return domainObject;
 7         }
 8         public static void Remove<TDomainObject>(TDomainObject domainObject) where TDomainObject : class
 9         {
10             EventProcesser.ProcessEvent(new PreRemoveDomainObjectEvent<TDomainObject> { DomainObject = domainObject });
11             EventProcesser.ProcessEvent(new RemoveDomainObjectEvent<TDomainObject> { DomainObject = domainObject });
12             EventProcesser.ProcessEvent(new DomainObjectRemovedEvent<TDomainObject> { DomainObject = domainObject });
13         }

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

当然，和前面的例子一样，我们还必须告诉框架，从事件的那个部分去获取事先响应者的唯一标识，我们可以通过下面的简单明了的代码来告诉框架这个信息：

1         RegisterObjectEventMappingItem<DomainObjectAddedEvent<Reply>, Topic>(evnt => evnt.DomainObject.TopicId);
2         RegisterObjectEventMappingItem<DomainObjectRemovedEvent<Reply>, Topic>(evnt => evnt.DomainObject.TopicId);

我 们可以看出，这里的代码要币上例的代码简单很多，原因是Topic类对同一个事件的响应函数只有一个。这里，我们仅仅只是提供了一个委托用来告诉框架 Topic的唯一标识如何获取，这样就足够了。其实在大多数情况下，一个类对某个事件的响应函数只有一个，也就是说，只要确定了领域对象类型和事件类型， 我们就可以找到对应的响应函数了。

**应用场景3：论坛中帖子被删除后帖子回复的级联删除**

本篇文章一开始简单讨论了聚合和仓储的概念。首先聚合有业务逻辑，而仓储是用来持久化整个聚合的，那么仓储也肯定知道它所管理的聚合的业务逻辑。也就是说，仓储在持久化聚合时，肯定知道了该聚合内的哪些对象需要被一起持久化，哪些则不用。比如下面的例子：

Book.Author

Book.Comments

假 设有一本书，用Book表示；它是一个聚合根，一本书有一些评论，用Comments表示书本的所有评论，书本评论离开书本没有意义，类似于Order和 OrderItem之间的关系，所以Book聚合了一些Comments；另外，一本书有一个作者，用Author表示。一般情况下，Author也是一 个聚合根，因为它是独立于书本而存在的。当我们删除一本书时，书本的作者肯定不能被删除，最多删除他们之间的关系。好了，有了上面这些前提条件后，假设有 一个BookRepository，它负责持久化Book。则BookRepository的RemoveBook方法看起来应该是这样：

bookRepository.RemoveBook(book)

{

​    //delete book it self;

​    //delete book comments;

​    //remove the relationship between book and author; 

} 

我 们可以充分看到上面的方法之所以知道当一本书需要被删除时需要做哪些事情，是因为BookRepository完全知道整个聚合（这里就是Book）的所 有和聚合相关的业务逻辑。事实上，在Eric Evans的DDD理论中，也正是通过聚合及仓储的设计来确保各个领域对象之间的概念完整性的。

但是，我上面提到过，没有了聚合，没有了仓储，我们还可以通过事件来确保领域对象的完整性。下面举个例子来说明如何实现这个目标：

大家都知道一个论坛中**帖子与帖子回复的关系**应该是和**书本与书本评论的关系**是同一种关系。也就是说，当我们在删除一个帖子时，还需要级联删除帖子的回复。

帖子类的实现上面已经写了，这里我们看一下帖子回复类的实现：

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 1     public class Reply : DomainObject<Guid>
 2     {
 3         #region Constructors
 4 
 5         public Reply(Guid topicId) : base(Guid.NewGuid())
 6         {
 7             this.TopicId = topicId;
 8         }
 9 
10         #endregion
11 
12         #region Public Properties
13 
14         public Guid TopicId { get; private set; }     //主题ID
15         [TrackingProperty]
16         public string Body { get; set; }              //消息内容
17 
18         #endregion
19 
20         #region Event Handlers
21 
22         private void Handle(DomainObjectRemovedEvent<Topic> evnt)
23         {
24             Repository.Remove(this);
25         }
26 
27         #endregion
28     }

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

可以看到回复类有一个事件响应函数，该函数表示当其所属的帖子删除时，需要把自己也一起删除。也就是说，当我们在执行如下代码时，上面代码中的响应函数就会自动被执行。

1 Repository.Remove(topic);

当然，框架还不可能也做不到这么智能的地步。我们必须告诉框架哪些回复回去响应DomainObjectRemovedEvent<Topic>事件。如下代码所示：

​    RegisterObjectEventMappingItem<DomainObjectRemovedEvent<Topic>, Reply>(
​        evnt => Repository.Find<Reply, FindTopicRepliesEvent>(evt => evt.TopicId = evnt.DomainObject.Id));

上面的代码表示帖子回复类会去响应DomainObjectRemovedEvent<Topic>事件，也就是帖子被删除的事件，并且通过一个委托来告诉框架有哪些回复会响应该事件。

**总结：** 

从上面的几个例子，我们可以清楚的看到领域对象之间没有相互引用，完全通过事件来实现相互协作。比如父对象通知子对象，子对象通知父对象，一个事件通知一个或多个同类型或不同类型的对象，等等。要实现任何一个业务场景，我们需要做的事情一般是：

1）通知中央事件处理器处理某个事件（如果该事件是框架没有提供特定的业务事件，则需要自己定义，如TransferEvent）；

2）领域对象响应该事件，通过定义私有的响应函数来实现响应；

3）在领域模型内部，告诉框架事件及响应者之间的映射关系，并告诉框架有哪个或哪些对象会去响应，它们的唯一标识是如何从事件中获取的；

通 过这三个步骤，我们就可以轻松简单的实现各种领域对象之间的协作了。而且需要强调的是，通过这样的方式，可以充分体现出领域对象是“活”的这个概念。因为 所有的领域对象的事件响应函数都是私有的，也就是领域对象自己的行为别的领域对象无法去调用，而都是由一个“中央事件处理器”去统一调用。这样的效果就 是，任何一个领域对象都会“主动”去响应某个事件，这样就从分体现出了“活”对象的概念了。在我看来，这才是真正的面向对象编程，因为所有的对象都是主动 参与到某个业务场景中去的。

最后，关于使用这种方式来组织业务逻辑的好处和坏处，我目前还没有仔细研究过，我还没有 利用该框架做过一个真实的项目。但我想有一点是可以肯定的，那就是这应该是另外一种全新的组织业务逻辑的方法，并且它的最大特点是高度可扩展性，因为是基 于事件消息机制的，把领域对象之间的耦合度降到了最低，但同时我想在可维护性方面可能会有一些缺点。 

 		[基于“事件”驱动的领域驱动设计（DDD）框架分析及Demo演示](http://www.cnblogs.com/netfocus/archive/2011/03/27/1997014.html) 	

从 去年10月份开始，学了几个月的领域驱动设计（Domain Driven Design，简称DDD）。主要是学习领域驱动设计之父Eric  Evans的名著：《Domain-driven design：领域驱动设计:软件核心复杂性应对之道》，以及另外一本Martin  Flower的《企业应用架构模式》，学习到了不少关于如何组织业务逻辑方面的知识。另外，在这个过程中也接触到了一些开源的架构和一些很好的思想。如： 命令查询职责分离（Command Query Responsibility Segregation，简称CQRS），事件驱动架构（Event  Driven  Architecture，简称EDA），以及四色原型和DCI架构，等等。前面这些知识对我来说是非常宝贵的财富，可以说我能进淘宝，很大程度上也是因 为我学习了前面这些知识的原因。

   在 介绍我设计的框架之前，我想先探讨一下以往我们都是如何思考设计OO的系统的。大家都知道，真正的对象应该是不仅有属性，而且有行为的。并且大家也有另外 一个共识，那就是为了完成某个任务，各个对象应该会相互协作共同完成这个任务。之前我们在设计一个系统时，往往会先设计好各个对象，明确他们的职责，在这 个过程中，还会考虑如何建立对象之间的关系（依赖、关联、聚合、组合），在这些关系的影响下，我们会认为对象之间应该有主从关系、依赖关系，等等。然后我 们所做的这些设计最终的目的是为了能让对象之间能够通过相互协作来共同完成某个任务。这种方式最核心的设计特色是，我们会通过”对象引用“的方式来实现对 象之间的各种关系。这种方式很好，**并且我们也已经完全习惯了从对象的职责以及它们之间的关系的角度去设计对象**。但这仅仅体现了一个哲学思想，那就是“物体之间通过直接作用完成某个任务”。   我觉得任何两个对象之间的交互有两种形式：1）**直接作用**，即对象A引用一个对象B，然后A调用B提供的某个方法，以此来完成两个对象之间的协作；2）**间接作用**， 对象A不引用对象B，仅仅包含了一个对象B的唯一标识，当它要和对象B协作时，会发送一个消息给对象B，然后对象B收到该消息后做出响应，从而实现两个对 象之间的协作；不管是哪种方式，他们最终的效果是一致的，都可以实现两个对象之间的交互并最终完成某个任务。那么这两种方式各自的优缺点在哪里呢？我个人 觉得对于对象引用的方式，其好处就是简单、直观、容易理解，很符合我们平时的设计习惯。但坏处是什么呢？我个人觉得这种方式是形成对象耦合的根本原因，对 象A对对象B存在了紧密的耦合，也许你会说，在间接作用的方式下，对象A不也会保留一个对象B的唯一标识吗？没错，但要知道保留引用和保留唯一标识的耦合 强度是不一样的。前者的耦合强度更大，因为持有另外一个对象的引用就意味着可以直接操作该对象，而仅仅持有另外一个对象的唯一标识则不行，必须先根据该唯 一标识获取另外一个对象，然后再操作它。而对于发送接受消息的方式，它的好处和坏处是什么呢？其实正好和前者相反，即不简单、不直观、不容易理解，容易让 大家觉得有过度设计的嫌疑，而好处则是能够将两个对象之间的耦合度降到最低。   好了，有了前面这些介绍之后，我想可以引出我所设计的这个框架的设计思想了。   既 然在对象直接作用的思路下设计软件的各种原则、模式，以及各种最佳实践已经很多了，如SOLID五大设计原则、GRASP九大OO设计原则、Gof的23 种设计模式、各种更大的模式如MVC、MVP、MVVM，等等。所以，我也就不用去费功夫去研究了，直接利用前辈的研究成果就行了。但我发现在对象间接作 用的思路下设计软件的各种原则或框架似乎还不够多。当然也有很多大家都很熟悉了，比如Observer设计模式，按照这个设计模式设计出来的.NET框架 中的事件和委托的机制，还有比如一些第三方的开源框架如事件总线，事件驱动架构，等等。   思考到这里，再结合自己最近不断学习DDD的背景下，我脑子里有了一个奇特的想法！那就是：是否可以搞一个**事件驱动的领域模型实现框架**从而可以让我们**从消息和行为的角度去设计对象呢？** 有 了这个框架，我们可以：1）通过消息实现领域模型中各个领域对象之间的交互，或者说是通信及协作；2）通过消息实现领域模型和外界的交互，如领域模型的使 用者和领域模型之间的交互，一般这个使用者是应用层；还有比如领域模型和数据持久层的交互。带着这个问题，我试图去寻找目前已有的框架来实现我的想法，但 遗憾的是，我找不到，所以只能自己开发。想到这里，我其实挺担心的，因为我很有可能已经走火入魔了，因为我要走的设计道路很可能是个死胡同或不归路，或者 说不是一条真正能很好的解决软件设计的路，不然我怎么会找不到这样的框架呢？但不管怎样，还是先试试再说吧！反正我的大脑放在那里不用也是浪费。就这样， 带着这样的目标和思路，我开始一步步设计我的框架了。

经过了三个月的设计、编码、测试、分享、讨论、重构的循环过程。到目前为止，总算初步实现了自己当初的目标，现在唯一差的就是在真正的实际项目中使用了。但幸好已经写了两个不同层次的Demo用来验证我的框架了。

http://files.cnblogs.com/netfocus/EventBasedDDDExample.rar

该 Demo包含了框架的源代码和Demo文件，基于VS2010开发，因为需要用到.NET4.0中的一些特性，如逆变和协变。源代码打开 后，EventBasedDDDExample.PresentationLayer是启动项目，直接F5就可以运行。该Demo为了重点突出领域模型的 设计，特意采用内存作为数据持久层，去掉了应用层，并且用控制台应用程序作为UI层，这样就方便大家运行Demo。该项目包含了四个演示的例子，前面两个 例子演示了如何利用我的框架实现特定的业务场景（一个是银行转账的例子，另一个是论坛中发帖发回复删除回复的例子）。具体功能参见源代码。

http://files.cnblogs.com/netfocus/ProductName.rar

该 Demo是一个比较真实的项目，也是用VS2010开发。前身是我之前开发过的一个蜘蛛侠论坛，现在用我最新的框架来实现这个论坛。但由于时间有限，UI 层还没开发好，但应用层、领域层、持久层已经开发好。因此大家在查看源代码时，不要去看UI层的设计，因为我还没开发好。而应该去看其他几层的设计！大家 从我这个Demo中，可以看到如何将经典的领域驱动四层分层架构和我的框架集成。相信这对大家非常具有实用价值。然后关于项目的命名空间，我也要解释下。 假设现在有一个公司要做一个项目，我觉得比较好的项目命名方式为：以CompanyName.ProductName作为前缀，基础类库命名为 Common，产品中的某个子应用模块，则可以命名为 CompanyName.ProductName.Modules.Forum，CompanyName.ProductName.Modules.Blog， 等。然后每个模块还可以根据模块的分层设计分出不同的Project，比如论坛的应用层可以命名 为：CompanyName.ProductName.Modules.Forum.ApplicationService，等。由于我做的只是一个展示 架构的Demo，所以没有用具体的CompanyName，ProductName。我觉得在开发阶段我们可以不使用最后的名字，到了最后项目快完成时再 做统一全局替换即可。

**下面介绍一下我的框架的设计思想：**

领域模型的组成元素：领域服务（Domain Service）+领域对象（Domain Object）+领域事件（Domain Event）+中央事件处理器（Event Processer）。

1. 领域服务：这个元素和Evans提到的领域服务一致，主要目的也是用来完成单个领域对象不能完成的职责，如银行转账操作；
2. 领 域对象：这个元素和Evans提到的Entity很类似，也有一个唯一标识，但和Evans中的概念也有不同的地方。比如Evans中的Entity为了 保持领域模型的完整性，有聚合的概念，即Aggregate。另外还有值对象的概念，即Value  Object。但在我的设计中，领域模型中的所有的对象都是平等的，没有任何聚合或关联的概念，也没有值对象的概念。所有的领域对象都通过事件来进行交互 协作，从而达到完成各种任务的目的。
3. 领域事件：这个元素在整个领域模型中最重要，就好比是人体的血液或神经。它是领域模型内部各个领域 对象之间通信以及领域模型和外部通信时传递的信息的载体。通过领域事件，我们可以“串”连任何两个领域对象，从而达到让他们相互协作的目的。所谓的串联就 是，一个对象发出消息，另外一个对象接收消息并做出正确响应。值得一提的是，我这里提到的事件不仅仅是通知别人发生了什么，而是泛指所有可能的通信情况。 比如告诉别人我要什么（我想干什么），告诉别人我将要做什么，等等。也就是说，事件有可能带有一定的目的性，即有可能会指定应该由哪个对象去响应该事件。 也许在你看来这已经不是标准的事件了，因为标准的事件应该是不可能知道会由哪些人回去响应该事件的。没错，它就是一个不标准的事件。我前面已经提到了，我 这里的事件指对象之间通信的载体。而通信的情况是非常多的，肯定不只局限于告诉别人我发生了什么，还有非常多其他的情况。最后还有一点需要特别指出的是， 事件发出去并响应后，有可能会有响应结果。关于这个问题，一般有两个实现方式：利用事件的回调函数实现；让事件响应函数提供返回值，然后在事件完全响应完 成后，从事件对象中取出可能的返回值。我认为这两种方式都可以，我的框架采用的是后者。
4. 中央事件处理器：这个元素只做一件事情，那就是处理某个传进来的事件。怎么处理？就是根据当前事件获取所有可能的响应者，然后调用每个响应者的响应函数执行每个响应。

另 外，领域模型与外界如何交互呢？还是通过上面所提到的事件，当外界需要领域模型做什么事情时，就发送一个在领域模型中已经定义好的事件，然后领域模型或其 他人（比如持久层）就会响应该事件了。当领域模型发生了什么或想要外界提供什么数据时，也是通过发送事件，然后外界就会响应，从而为领域模型提供必要的支 持，如持久化支持。通过上面的分析，似乎可以看出我们已经找到银弹了，即找到了一种单一的模式可以用来解决所有的对象交互与协作的问题了？应该不是这样， 但我自己没发现不知道这种设计的问题出在哪里，所以非常期望大家能多给我些意见。还是那句话，我希望我们每个中国人都是一个不盲目相信权威并敢于怀疑权威 并能积极去思考和将自己的思考转化为生产力的人，而不只是一个仅仅会使用外国人写出来的框架的人。

这篇文章说 的全部是思想或思考心得，接下来我会具体分析我上面提到的两个Demo的具体设计。但我真的很希望大家能重视思想，重视自己的思考过程，并且要敢于去将自 己的思想转化为具体的成果，如框架。我们来这个地球上走一趟，如果仅仅只是会用别人写出来的东西，那不是很可惜？但如果你根据自己的思想写出了几个能让别 人用的东西出来，那不是非常好吗？那才是很有意义和价值的事情。





​     分类:              [[12\]Architecture](https://www.cnblogs.com/Leo_wl/category/225687.html),             [[20\]DesignAnalysis](https://www.cnblogs.com/Leo_wl/category/225695.html)

​         [好文要顶](javascript:void(0);)         [已关注](javascript:void(0);)     [收藏该文](javascript:void(0);)     [![img](icon_weibo_24.png)](javascript:void(0);)     [![img](wechat.png)](javascript:void(0);) 

[![img](u104109.gif)](https://home.cnblogs.com/u/Leo_wl/)

​             [HackerVirus](https://home.cnblogs.com/u/Leo_wl/)
​             [关注 - 246](https://home.cnblogs.com/u/Leo_wl/followees/)
​             [粉丝 - 3408](https://home.cnblogs.com/u/Leo_wl/followers/)         





​                 我在关注他 [取消关注](javascript:void(0);)     

​         1     

​         0     



​     

[关注](javascript:void(0);)  |  [顶部](https://www.cnblogs.com/leo_wl/archive/2011/06/22/2086586.html#top)  |  [评论](javascript:void(0);)



​      [« ](https://www.cnblogs.com/Leo_wl/archive/2011/06/22/2086583.html) 上一篇：    [SpringBird Erp系统快速开发平台](https://www.cnblogs.com/Leo_wl/archive/2011/06/22/2086583.html)     
​     [» ](https://www.cnblogs.com/Leo_wl/archive/2011/06/23/2088458.html) 下一篇：    [C# List.Sort排序](https://www.cnblogs.com/Leo_wl/archive/2011/06/23/2088458.html)  

 		posted on  2011-06-22 09:41 [HackerVirus](https://www.cnblogs.com/Leo_wl/) 阅读(554) 评论(1) [ 编辑](https://i.cnblogs.com/EditPosts.aspx?postid=2086586) [收藏](javascript:void(0))  	