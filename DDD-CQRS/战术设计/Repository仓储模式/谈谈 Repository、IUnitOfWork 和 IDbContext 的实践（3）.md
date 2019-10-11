







#                   [DDD 领域驱动设计－谈谈 Repository、IUnitOfWork 和 IDbContext 的实践（3）](https://www.cnblogs.com/xishuai/p/ddd-repository-iunitofwork-and-idbcontext-part-3.html)              



上一篇：《[DDD 领域驱动设计－谈谈 Repository、IUnitOfWork 和 IDbContext 的实践（2）](http://www.cnblogs.com/xishuai/p/ddd-repository-iunitofwork-and-idbcontext-part-2.html)》

这篇文章主要是对 [DDD.Sample](https://github.com/yuezhongxin/DDD.Sample) 框架增加 Transaction 事务操作，以及增加了一些必要项目。

虽然现在的 IUnitOfWork 实现中有 Commit 的实现，但也就是使用的 EF SaveChanges，满足一些简单操作可以，但一些稍微复杂点的实体操作就不行了，并且 Rollback 也没有实现。

现在的 UnitOfWork 实现代码：

```
public class UnitOfWork : IUnitOfWork
{
    private IDbContext _dbContext;

    public UnitOfWork(IDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public void RegisterNew<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Set<TEntity>().Add(entity);
    }

    public void RegisterDirty<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Entry<TEntity>(entity).State = EntityState.Modified;
    }

    public void RegisterClean<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Entry<TEntity>(entity).State = EntityState.Unchanged;
    }

    public void RegisterDeleted<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Set<TEntity>().Remove(entity);
    }

    public async Task<bool> CommitAsync()
    {
        return await _dbContext.SaveChangesAsync() > 0;
    }

    public void Rollback()
    {
        throw new NotImplementedException();
    }
}
```

基于上面的实现，比如要处理这样的一个操作：先添加一个 Teacher，然后再添加一个 Student，Student 实体中有一个 TeacherId，一般实现方式如下：

```
public async Task<bool> Add(string name)
{
    var teacher = new Teacher { Name = "teacher one" };
    _unitOfWork.RegisterNew(teacher);
    await _unitOfWork.CommitAsync();

    //可能还有一些 web 请求操作，比如 httpClient.Post(tearch); 可能会出选异常。

    var student = new Student { Name = name, TeacherId = teacher.Id };
    _unitOfWork.RegisterNew(student);
    await _unitOfWork.CommitAsync();

    return true;
}
```

上面的实现可能会出现一些问题，比如添加 Teacher 出现了异常，web 请求出现了异常，添加 Student  出现了异常等，该如何进行处理？所以你可能会增加很多判断，还有就是异常出现后的修复操作，当需求很复杂的时候，我们基于上面的处理也就会更加复杂，根本原因是并没有真正的实现  Transaction 事务操作。

如果单独在 EF 中实现 Transaction 操作，可以使用 TransactionScope，参考文章：[在 Entity Framework 中使用事务](http://www.cnblogs.com/dudu/archive/2011/04/06/entity_framework_transaction.html)

TransactionScope 的实现比较简单，如何在 DDD.Sample 框架中，结合 IUnitOfWork 和 IDbContext 进行使用呢？可能实现方式有很多中，现在我的实现是这样：

首先，IDbContext 中增加 Database 属性定义：

```
public interface IDbContext
{
    Database Database { get; } //add

    DbSet<TEntity> Set<TEntity>()
        where TEntity : class;

    DbEntityEntry<TEntity> Entry<TEntity>(TEntity entity)
        where TEntity : class;

    Task<int> SaveChangesAsync();
}
```

增加 Database 属性的目的是，便于我们在 UnitOfWork 中访问到 Transaction，其实还可以定义这样的接口：`DbContextTransaction BeginTransaction();`，但  EF 中的 DbContext 并没有进行实现，而是需要通过 Database 属性，所以还需要在 IDbContext  实现中额外实现，另外增加 Database 属性的好处，还有就是可以在 UnitOfWork 中访问执行很多的操作，比如执行 SQL 语句等等。

这里需要说下 IDbContext 定义，我原先的设计初衷是，让它脱离 EF，作为所有数据操作上下文的定义，但其实实现的时候，还是脱离不了  EF，因为接口返回的类型都在 EF 下，最后 IDbContext 就变成了 EF DbContext  的部分接口定义，所以这部分是需要再进行设计的，但好在有了 IDbContext，可以让 EF 和 UnitOfWork 隔离开来。

SchoolDbContext 中的实现没有任何变换，因为继承的 EF DbContext 已经有了实现，UnitOfWork 改动比较大，代码如下：

```
public class UnitOfWork : IUnitOfWork
{
    private IDbContext _dbContext;
    private DbContextTransaction _dbTransaction;

    public UnitOfWork(IDbContext dbContext)
    {
        _dbContext = dbContext;
        _dbTransaction = _dbContext.Database.BeginTransaction();
    }

    public async Task<bool> RegisterNew<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Set<TEntity>().Add(entity);
        return await _dbContext.SaveChangesAsync() > 0;
    }

    public async Task<bool> RegisterDirty<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Entry<TEntity>(entity).State = EntityState.Modified;
        return await _dbContext.SaveChangesAsync() > 0;
    }

    public async Task<bool> RegisterClean<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Entry<TEntity>(entity).State = EntityState.Unchanged;
        return await _dbContext.SaveChangesAsync() > 0;
    }

    public async Task<bool> RegisterDeleted<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Set<TEntity>().Remove(entity);
        return await _dbContext.SaveChangesAsync() > 0;
    }

    public void Commit()
    {
        _dbTransaction.Commit();
    }

    public void Rollback()
    {
        _dbTransaction.Rollback();
    }
}
```

UnitOfWork 构造函数中，根据 DbContext 创建 DbContextTransaction  对象，然后在实体每个操作中，都添加了 SaveChanges，因为我们用了 Transaction，所以在执行 SaveChanges  的时候，并没有应用到数据库，但可以获取到新添加实体的 Id，比如上面示例 Student 中的 TeacherId，并且用 Sql  Profiler 可以检测到执行的 SQL 代码，当执行 Commit 的时候，数据对应进行更新。

测试代码：

```
public async Task<bool> AddWithTransaction(string name)
{
    var teacher = new Teacher { Name = "teacher one" };
    await _unitOfWork.RegisterNew(teacher);

    //可能还有一些 web 请求操作，比如 httpClient.Post(tearch); 可能会出选异常。
    
    var student = new Student { Name = name, TeacherId = teacher.Id };
    await _unitOfWork.RegisterNew(student);

    _unitOfWork.Commit();
    return true;
}
```

在上面代码中，首先在没执行到 Commit 之前，是可以获取到新添加 Teacher 的 Id，并且如果出现了任何异常，都是可以进行回滚的，当然也可以手动进行 catch 异常，并执行`_unitOfWork.Rollback()`。

不过上面的实现有一个问题，就是每次实体操作，都用了 Transaction，性能我没测试，但肯定会有影响，好处就是 IUnitOfWork 基本没有改动，还是按照官方的定义，只不过部分接口改成了异步接口。

除了上面的实现，还有一种解决方式，就是在 IUnitOfWork 中增加一个类似 BeginTransaction 的接口，大致实现代码：

```
public class UnitOfWork : IUnitOfWork
{
    private IDbContext _dbContext;
    private DbContextTransaction _dbTransaction;

    public UnitOfWork(IDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    //add
    public void BeginTransaction()
    {
        _dbTransaction = _dbContext.Database.BeginTransaction();
    }

    public async Task<bool> RegisterNew<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Set<TEntity>().Add(entity);
        if (_dbTransaction != null)
            return await _dbContext.SaveChangesAsync() > 0;
        return true;
    }

    public async Task<bool> RegisterDirty<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Entry<TEntity>(entity).State = EntityState.Modified;
        if (_dbTransaction != null)
            return await _dbContext.SaveChangesAsync() > 0;
        return true;
    }

    public async Task<bool> RegisterClean<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Entry<TEntity>(entity).State = EntityState.Unchanged;
        if (_dbTransaction != null)
            return await _dbContext.SaveChangesAsync() > 0;
        return true;
    }

    public async Task<bool> RegisterDeleted<TEntity>(TEntity entity)
        where TEntity : class
    {
        _dbContext.Set<TEntity>().Remove(entity);
        if (_dbTransaction != null)
            return await _dbContext.SaveChangesAsync() > 0;
        return true;
    }

    public async Task<bool> Commit()
    {
        if (_dbTransaction == null)
            return await _dbContext.SaveChangesAsync() > 0;
        else
            _dbTransaction.Commit();
        return true;
    }

    public void Rollback()
    {
        if (_dbTransaction != null)
            _dbTransaction.Rollback();
    }
}
```

上面这种实现方式就解决了第一种方式的问题，需要使用 Transaction 的时候，直接在操作之前调用 BeginTransaction 就行了，但不好的地方就是改动了 IUnitOfWork 的接口定义。

除了上面两种实现方式，大家如果有更好的解决方案，欢迎提出。

另外，DDD.Sample 增加和改动了一些东西：

- 增加 DDD.Sample.Domain.DomainEvents、DDD.Sample.Domain.DomainServices 和 DDD.Sample.Domain.ValueObjects。
- 从 DDD.Sample.Domain 分离出 DDD.Sample.Domain.Repository.Interfaces。
- 增加 DDD.Sample.BootStrapper，执行 Startup.Configure 用于系统启动的配置。
- 去除 IEntity，在 IAggregateRoot 中添加 Id 属性定义。

---



 作者：田园里的蟋蟀 
微信公众号：**你好架构** 
出处：http://www.cnblogs.com/xishuai/  
 公众号会不定时的分享有关架构的方方面面，包含并不局限于：Microservices（微服务）、Service  Mesh（服务网格）、DDD/TDD、Spring Cloud、Dubbo、Service  Fabric、Linkerd、Envoy、Istio、Conduit、Kubernetes、Docker、MacOS/Linux、Java、.NET  Core/ASP.NET  Core、Redis、RabbitMQ、MongoDB、GitLab、CI/CD（持续集成/持续部署）、DevOps等等。 
 本文版权归作者和博客园共有，欢迎转载，但未经作者同意必须保留此段声明，且在文章页面明显位置给出原文连接。 