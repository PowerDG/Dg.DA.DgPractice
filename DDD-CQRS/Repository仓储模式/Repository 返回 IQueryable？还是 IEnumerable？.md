​               [Repository 返回 IQueryable？还是 IEnumerable？](https://www.cnblogs.com/xishuai/p/repository-return-iqueryable-or-ienumerable.html)



这是一个很有意思的问题，我们一步一步来探讨，首先需要明确两个概念（来自 MSDN）：

- IQueryable：提供对未指定数据类型的特定数据源的查询进行计算的功能。
- IEnumerable：公开枚举数，该枚举数支持在非泛型集合上进行简单迭代。

IQueryable 继承自 IEnumerable，它们俩最大的区别是，IQueryable 是表达式树处理，可以延迟查询，而  IEnumerable 只能查询在本地内存中，Repository 的概念就不多说了，在“伪 DDD”设计中，你可以把它看作是数据访问层。



## 返回 IEnumerable

下面我们先实现 Repository 返回 IEnumerable：

```csharp
public interface IBookRepository  
{
    Book GetById();
    IEnumerable<Book> GetAllBooks();
    IEnumerable<Book> GetBy....();
    void Add(Book book);
    void Delete(Book book);
    void SaveChanges();
}
```

上面是我们的一般接口设计，包含查询、增加、删除操作，你发现并没有修改，其实我们可以先通过 GetById 操作，然后取得 Book 对象，进行修改，最后执行 SaveChanges 就可以了，在持久化数据库的时候，会判断实体状态值的概念，最后进行应用改变。

GetBy....() 代表了一类查询方法，因为我们的业务比较复杂，对 Book  的查询会千奇百怪，所以，没有办法，我们只能**增加各类查询方法来满足需求**，最后可能导致的结果是，一个 Where  对应一个查询方法，IBookRepository 会充斥着各类查询方法，并且这些查询方法一般只会被一个 Application  方法调用，如果你查看下 GetBy....() 方法实现，会发现其实都大同小异，不同的只是 Where  条件，这样的结果就会导致代码变得非常的臃肿。

## 使用 IQueryable 

针对上面的问题，怎么办呢？因为 IEnumerable 是查询在本地内存中，所以没有办法，我们只能这样处理，那如何使用 IQueryable 会是怎样的呢？我们看下代码：

```csharp
public interface IBookRepository  
{
    IQueryable<Book> GetBooks();
    void Add(Book book);
    void Delete(Book book);
    void SaveChanges();
}
```

只有一个 GetBooks 查询，那它能满足各类查询需求吗？我们看下 Application 中调用的代码：

```csharp
public class BookApplication : IBookApplication  
{
    private IBookRepository _bookRepository;

    public BookApplication(IBookRepository bookRepository)
    {
        _bookRepository = bookRepository;
    }

    public IEnumerable<Book> GetAllBooks()
    {
        return _bookRepository.GetBooks().AsEnumerable();
    }

    public IEnumerable<Book> GetBooksByUser(int userId)
    {
        return _bookRepository.GetBooks().Where(b => b.UserId == userId).AsEnumerable();
    }

    //....
}
```

##### 延迟查询**

因为 **IQueryable 是延迟查询**，只有在执行 AsEnumerable 的时候，才会真正去查询，也可以这么说，BookApplication 可以根据需求**任意构建查询表达式树**，就像我们在 SQL Server 中写查询 SQL，`SELECT * FORM Books` 在 BookRepository 中进行构建，`WHERE ...` 操作在 BookApplication 中进行构建，最后的 F5 执行也在 BookApplication 中。

从上面的代码中，我们可以看到，IQueryable 很好的解决了使用 IEnumerable  所出现的问题，**一个查询可以应对千变万化的应用查询**，IQueryable 看起来好像是那么的强大，其实 IQueryable  的强大并不限于此，上面说的是查询表达式，那添加、修改和删除操作，可以使用它进行完成吗？修改和删除是可以的，添加并不能

具体可以参考 dudu  的这篇博文：[开发笔记：基于EntityFramework.Extended用EF实现指定字段的更新](http://www.cnblogs.com/dudu/p/4735211.html)。

关于 EntityFramework.Extended 的扩展，需要记录下，因为这个东西确实非常好，改变了我们之前的很多写法和问题，比如，在之前使用 EF 进行修改和删除实体，我们一般会这些写：

```csharp
public class BookApplication : IBookApplication  
{
    private IBookRepository _bookRepository;

    public BookApplication(IBookRepository bookRepository)
    {
        _bookRepository = bookRepository;
    }

    public void UpdateNameById(int bookId, string bookName)
    {
        var book = _bookRepository.GetById(bookId);
        book.BookName = bookName;
        _bookRepository.SaveChanges();
    }

    public void UpdateNameByIds(int[] bookIds, string bookName)
    {
        var books = _bookRepository.GetBooksByIds(bookIds);
        foreach (var book in books)
        {
            book.BookName = bookName;
        }
        _bookRepository.SaveChanges();
    }

    public void Delete(int id)
    {
        var book = _bookRepository.GetById(id);
        _bookRepository.Delete(book);//context.Books.Remove(book);
        _bookRepository.SaveChanges();
    }
}
```

上面的写法有什么问题呢？其实最大的问题就是，我们要进行修改和删除，必须先获取这个实体，也就是先查询再进行修改和删除，这个就有点多余了，尤其是  UpdateNameByIds 中的批量修改，先获取 Book 对象列表，然后再遍历修改，最后保存，是不是有点 XXX  的感觉呢，仔细想想，还不如不用 EF 来的简单，因为一个 Update SQL 就可以搞定，简单并且性能又高，为什么还要使用 EF  呢？这是一个坑？其实使用 EF 也可以执行 SQL，但这就像换了个马甲，没有什么卵用。

针对上面的问题，该如何解决呢？很简单，使用 EntityFramework.Extended 和 IQueryable 就可以，我们改造下上面的代码：

```csharp
using EntityFramework.Extensions;

public class BookApplication : IBookApplication  
{
    private IBookRepository _bookRepository;

    public BookApplication(IBookRepository bookRepository)
    {
        _bookRepository = bookRepository;
    }

    public void UpdateNameById(int bookId, string bookName)
    {
        IQueryable<Book> books = _bookRepository.GetBooks();
        books = books.Where(b => b.bookId == bookId);
        books.Update<Book>(b => new Book { BookName = bookName });
    }

    public void UpdateNameByIds(int[] bookIds, string bookName)
    {
        IQueryable<Book> books = _bookRepository.GetBooks();
        books = books.Where(b => bookIds.Contains(bookIds));
        books.Update<Book>(b => new Book { BookName = bookName });
    }

    public void Delete(int id)
    {
        IQueryable<Book> books = _bookRepository.GetBooks();
        books = books.Where(b => b.bookId == id);
        books.Delete<Book>();
    }
}
```

有没有发现什么不同呢？原来 IQueryable 还可以这样写？这货居然不只是用于查询，也可以用于删除和修改，另外，通过追踪生成的 SQL  代码，你会发现，没有了 SELECT，和我们直接写 SQL  是一样的效果，在执行修改和删除之前，我们需要对查询表达树进行过滤，也就是说的，当我们最后应用修改的时候，会是在这个过滤的查询表达树基础上的，比如上面的  Delete 操作，我们先通过 bookId 进行过滤，然后直接进行 Delete 就可以了，哇塞，原来是这样的简单。

当 BookApplication 操作变的简单的时候，BookRepository 也会相应变的简单：

```
public interface IBookRepository  
{
    IQueryable<Book> GetBooks();
    void SaveChanges();//只用于Books.Add(book);
}
```

一个 IQueryable 表达树，一个 SaveChanges 操作，就可以满足 BookApplication 中的所有操作。

------

###  IQueryable 相关文章

既然 IQueryable 是这么的强大，那用它就好了，为什么还要讨论呢？如果你 Google 搜索“Repository IQueryable”关键词，会发现大量的相关文章，我先贴出几个非常赞的讨论：

- [Should Repositories return IQueryable?](http://programmers.stackexchange.com/questions/192044/should-repositories-return-iqueryable)
- [Repository Return IQueryable](https://duckduckgo.com/?q=repository+return+iqueryable&ia=qa)
- [Should you return IQueryable from Your Repositories?](http://codetunnel.io/should-you-return-iqueryablet-from-your-repositories/)
- [What are alternatives to using IQueryable in Repository Pattern?](http://stackoverflow.com/questions/16848465/what-are-alternatives-to-using-iqueryablet-in-repository-pattern)
- [IQueryable vs List: What Should Your Repository Return?](https://www.paragon-inc.com/resources/blogs-posts/what-to-return)
- [Should my repository expose IQueryable?](http://mikehadlow.blogspot.jp/2009/01/should-my-repository-expose-iqueryable.html)
- [Repository Pattern and IQueryable](http://blog.sapiensworks.com/post/2013/01/24/Repository-Pattern-and-IQueryable.aspx/)（**简洁而有力**）
- [Why the Repository Pattern Is Still Valid](http://blog.fire-development.com/2013/03/07/why-the-repository-pattern-is-still-valid/)

上面只是部分，关于这类的文章，老外写的非常多，而且评论中的讨论也非常激烈，因为英语实在差，我大概看了一些，出乎我意料之外的是，很多人都不赞成  Repository 返回 IQueryable，但讨论的却非常有意思，比如有个老外这样感叹：I'm still not convinced  that returning IQueryable is a bad idea, but at least I'm far more aware  of the arguments against it. 大致意思是：我仍然不相信返回 IQueryable  是一个坏主意，但至少我更了解他们的反对理由，是不是很有意思呢？

## 优劣势

关于 Repository 返回 IQueryable 的讨论，我大致总结下：

#### 好处：

1. 延迟执行。
2. 减少 Repository 重复代码（GetBy...）。
3. IQueryable 提供更好的灵活性。
4. ...

#### 坏处：

1. 隔离单元测试。
2. 数据访问在 Repository 之外完成。
3. 数据访问异常在 Repository 之外抛出。
4. 该领域层将充斥着这些相当详细查询。
5. ...

好处就不多说了，因为我们上面已经实践过了，关于坏处，“隔离单元测试”是什么意思呢？也就是说我们不能很好的对 Repository  进行单元测试，一方面是因为 IRepository 是那么的简单（就两个方法），另一方面 IQueryable  是查询表达树，它并不是完成时，只有在具体调用的时候才会查询完成，所以，对于 Repository 的单元测试，显然是没有任何意义的。

关于 [Repository Pattern and IQueryable](http://blog.sapiensworks.com/post/2013/01/24/Repository-Pattern-and-IQueryable.aspx/) 这篇博文，我想再说一下，因为这个老外的观点非常赞，首先，它是基于 Repository 模式概念基础上说的，所以，我们一开始说：在“伪 DDD”设计中，你可以把 Repository 看作是数据访问层。这是两个不同的前提，我再大致总结下这个老外的观点：

- However the mistake is not the IQueryable itself, but its purpose.（不是 IQueryable 本身的错误，而是它的目的。）
- The point is that using IQueryable, you're asking for a query  builder and not for a model.（问题的关键是，使用 **IQueryable 是一个查询生成器**，而不是一个模型。）
- we want to specify what to get, not how to get it.（我们想通过规约得到它，而不是怎样去得到。）
- tell it the what, not the how.

看了上面，是不是有点豁然开朗的感觉呢，其实从 Repository 的模式概念方面考虑，使用 IQueryable  确实不是很恰当，但不可否认的是，IQueryable 又这么强大和便利，怎么办呢？就像博文一开始强调的那样：Repository  的概念就不多说了，在“伪 DDD”设计中，你可以把它看作是数据访问层。

所以呢，如果你的项目是“伪 DDD”，并且 Repository 是被你看作“数据访问层”，那么使用 IQueryable 就没啥问题了。

 作者：田园里的蟋蟀 
微信公众号：**你好架构** 
出处：http://www.cnblogs.com/xishuai/  
 公众号会不定时的分享有关架构的方方面面，包含并不局限于：Microservices（微服务）、Service  Mesh（服务网格）、DDD/TDD、Spring Cloud、Dubbo、Service  Fabric、Linkerd、Envoy、Istio、Conduit、Kubernetes、Docker、MacOS/Linux、Java、.NET  Core/ASP.NET  Core、Redis、RabbitMQ、MongoDB、GitLab、CI/CD（持续集成/持续部署）、DevOps等等。 
 本文版权归作者和博客园共有，欢迎转载，但未经作者同意必须保留此段声明，且在文章页面明显位置给出原文连接。 













