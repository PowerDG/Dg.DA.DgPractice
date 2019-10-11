#                   [Repository 简化实现多条件查询](https://www.cnblogs.com/xishuai/p/repository-query-linq-expression.html)              



Repository 在做查询的时候，如果查询条件多的话，`linq`查询表达式会写的很复杂，比如：

```csharp
public IQueryable<Student> Get(int id, string name, string address, Status? status, DateTime createTime)
{
    var query = _entities;
    if(id != 0)
    {
        query = query.where(x => x.Id == id);
    }
    if(!string.IsNullOrWhiteSpace(name))
    {
        query = query.where(x => x.Name.Contains(name));
    }
    if(!string.IsNullOrWhiteSpace(address))
    {
        query = query.where(x => x.Address.Contains(address));
    }
    if(status.HasValue)
    {
        query = query.where(x => x.Status == status.Value);
    }
    if(createTime != null)
    {
        query = query.where(x => x.CreateTime == createTime);
    }
    // ...

    return query;
}
```

可以看到，查询条件多的话，我们会写很多的`if`判断，代码看起来很不美观，解决方式使用`Expression<Func<T, bool>>`，示例代码：

```csharp
using System.Linq.Expressions;

public IQueryable<Student> Get(int id, string name, string address, Status? status, DateTime createTime)
{
    Expression<Func<Student, bool>> studentFunc = x =>
            (id == 0 || x.Id == id) &&
            (string.IsNullOrWhiteSpace(name) || x.Name.Contains(name)) &&
            (string.IsNullOrWhiteSpace(address) || x.Address.Contains(address)) &&
            (!status.HasValue || x.Status == status.Value) &&
            (createTime == null || x.CreateTime <= createTime);

    return _entities.Where(studentFunc);
}
```

生成示例`sql`代码：

```sql
SELECT `x`.`id`, `x`.`name`, `x`.`address`, `x`.`status`, `x`.`create_time`
FROM `students` AS `x`
WHERE (`x`.`id` = 2)
AND (`x`.`status` = 0) AND (`x`.`create_time` == '2017-04-25T16:24:29.769+08:00')) 
```

 作者：田园里的蟋蟀 
微信公众号：**你好架构** 
出处：http://www.cnblogs.com/xishuai/  
 公众号会不定时的分享有关架构的方方面面，包含并不局限于：Microservices（微服务）、Service  Mesh（服务网格）、DDD/TDD、Spring Cloud、Dubbo、Service  Fabric、Linkerd、Envoy、Istio、Conduit、Kubernetes、Docker、MacOS/Linux、Java、.NET  Core/ASP.NET  Core、Redis、RabbitMQ、MongoDB、GitLab、CI/CD（持续集成/持续部署）、DevOps等等。 
 本文版权归作者和博客园共有，欢迎转载，但未经作者同意必须保留此段声明，且在文章页面明显位置给出原文连接。 