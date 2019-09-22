## [为什么现在这么多公司使用Linq？](https://q.cnblogs.com/q/92316/)

https://q.cnblogs.com/q/DetailPage/92316/

### 1.linq是把复杂的问题简单化

2.使程序员只能做标准sql操作.屏蔽数据库差异.使代码更标准.因为复杂的数据库特性一般都会使项目更复杂.而程序员因为懒的动脑筋设计合理的结构.就会去用这些数据库特性.

3.linq的开发效率不是sql能比的.我一个人写接口给 pc主站/pc后台管理/app/事件处理平台  4个项目用.你试试写sql字符串能达到这样的开发效率?

4.可维护性.sql语句的可维护性就不喷啦.简直是一场灾难.刚入行的时候我也写sql.后来自己要改自己代码的时候.真的感觉是自己拉一坨屎.自己吃.而linq因为是强类型.所以维护起来非常方便

5.结构清晰.使程序员以对象的角度来开发.sql程序员实际上就是面向过程开发.而复杂业务时.面向过程的思维模式对项目来说.就是一场灾难.





### 站在公司角度而言，用linq（orm框架）肯定更容易维护

，换数据库不用说，有几个项目做大了后会换数据库的？

站在个人角度说，用linq（orm框架）可以把你从繁琐的tsql语句编写及各种赋值逻辑中解脱出来，很大程度提升了开发效率及代码可靠性，而且这种并不是和sql抵触的，你写的好linq肯定sql也不会差到哪去，写的不好的linq很容易在性能上出现问题，这种反而迫使你需要更了解数据库。

java 8  jdk中没有linq，但有lambda，这个看看就好，就那么几个方法，用起来相当费力，这个也是历史包袱太重。当然有各种第三方的加成的话的确会好很多，但由于泛型这块跛的太厉害，如果写c#再写java会发现有各种奇葩地方，为了实现相同功能的lambda语句，java的写出来会比较奇怪。







## [为什么说 LINQ 要胜过 SQL](https://www.oschina.net/translate/why-linq-beats-sql)

### 将 LINQ 用于实战

我几乎是只用 LINQ 来做数据库查询，因为它更有效率。

对于应用程序的编写而言，我的个人经验是一个使用 LINQ 的数据访问层（使用一个像 LINQ 到 SQL 或者 Entity Framework 的 API）可以将数据访问的开发时间砍掉一半，而且可以让维护工作更加的轻松。





如果你还没有沉溺于 LINQ，就会想这有啥大惊小怪的。SQL 并没有坏掉，为什么还要对它进行修补呢? 为什么我们还需要另外一种查询语言呢?

流行的说法是  LINQ 同 C#（或者  VB）集成在了一起，故而消除了编程语言和数据库之间配合上的鸿沟，同时为多个数据源的组合提供了单一的查询接口。虽然这些都是事实，但仅是故事的一部分。更重要的是：当要对数据库进行查询的时候，LINQ  在大多数情况下都比 SQL 更加有效。

同 SQL 相比， LINQ 更简单、整洁而且高级。这样子更像是拿 C# 同 C++ 做比较。真的，尽管有时候使用 C++ 仍然是最好的选择（比如使用 SQL 的场景），但在大多数场景中，使用现代整洁的语言而不必为底层细节操作就是一项大胜利。

SQL 是一门非常古老的语言—发明于 1974 年。虽然经历过了无数此扩展，但从来没有被重新设计过。这就使得它有点混乱了—不像是 VB6 或者 Visual FoxPro。你也许已经慢慢变得习惯于此因而看不到任何错漏的地方!

[                                                              ![LeoXu](233834_50.jpeg)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 22:42

​                                                                      

​                                                                     

让我们来看一个例子。你想要编写一个简单的查询来获取客户数据，如下：

```
SELECT UPPER(Name)
FROM Customer
WHERE Name LIKE 'A%'
ORDER BY Name
```

现在假设要将结果集里的这些数据提供给一个网页，并且我们想获取第 21 到 30 行数据。所以我们需要一个子查询：

```
SELECT UPPER(Name) FROM
(
   SELECT *, RN = row_number()
   OVER (ORDER BY Name)
   FROM Customer
   WHERE Name LIKE 'A%'
) A
WHERE RN BETWEEN 21 AND 30
ORDER BY Name
```

而如果你需要支持版本（在 SQL Server 2005 之前的）更老的数据库，情况会更糟糕:

```
SELECT TOP 10 UPPER (c1.Name)
FROM Customer c1
WHERE
   c1.Name LIKE 'A%'
   AND c1.ID NOT IN
   (
      SELECT TOP 20 c2.ID
      FROM Customer c2
      WHERE c2.Name LIKE 'A%'
      ORDER BY c2.Name
   ) 
ORDER BY c1.Name
```

这样做不仅复杂而混乱，而且也违背了 DRY 原则。如下是使用 LINQ 实现相同的查询功能。显然在简单性上更胜一筹：

```
var query =
   from c in db.Customers
   where c.Name.StartsWith ("A")
   orderby c.Name
   select c.Name.ToUpper();

var thirdPage = query.Skip(20).Take(10);
```

只有当我们枚举到 thirdPage 时，查询才会实际执行。在从  LINQ 到 SQL 或者 Entity Framework 的场景中，翻译引擎会将（我们用两个步骤组合而成的）查询转换成一个 SQL  语句，这个语句是针对其所连接的数据库服务器进行了优化的。

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 22:52

​                                                                      

​                                                                     

### 可组合性

您可能已经注意到 LINQ 的另一个更微妙（微妙但意义重大）的好处。我们选择了组合中的两个查询步骤：

```
IQueryable<T> Paginate<T> (this IQueryable<T> query, int skip, int take)
{
   return query.Skip(skip).Take(take);
}
```

我们可以这样做：

```
var query = ...
var thirdPage = query.Paginate (20, 10);
```

更重要的是，在这里我们可以进行任意的分页查询。换言之就是通过 LINQ 你可以把查询分解成一部分，然后在你的应用程序中重用。

[                                                              ![溪边九节](553781_50.jpeg)                                              ](https://my.oschina.net/crooner)

[溪边九节](https://my.oschina.net/crooner)

翻译于 2017/02/22 18:04

​                                                                      

​                                                                             其它翻译版本 (1)                                             

### 联合

LINQ 另一好处就是你可以不用 JOIN  就能进行关系间查询。例如，我们想要列出所有购物在 $1000  或者以上，并且居住在华盛顿的顾客。我们会假定让购买项目化（也就是经典的采购/项目采购场景）并且把（没有顾客记录的）现金销售也囊括进来。这就需要在四个表（Purchase,  Customer, Address 以及 PurchaseItem）之间进行查询。使用 LINQ，这样的查询不费吹灰之力：

```
from p in db.Purchases
where p.Customer.Address.State == "WA" || p.Customer == null
where p.PurchaseItems.Sum (pi => pi.SaleAmount) > 1000
select p
```

将此与同等功能的 SQL 相比较：

```
SELECT p.*
FROM Purchase p
    LEFT OUTER JOIN 
        Customer c INNER JOIN Address a ON c.AddressID = a.ID
    ON p.CustomerID = c.ID	
WHERE
   (a.State = 'WA' || p.CustomerID IS NULL)
    AND p.ID in
    (
        SELECT PurchaseID FROM PurchaseItem
        GROUP BY PurchaseID HAVING SUM (SaleAmount) > 1000
    )
```

对此例进一步扩展，假设我们想要将结果集按价格进行逆序排列，并在最终的投影中显示销售员的姓名以及所购买项目的数量。我们可以自然不重复地表达出这些附件的查询条件：

```
from p in db.Purchases
where p.Customer.Address.State == "WA" || p.Customer == null
let purchaseValue = p.PurchaseItems.Sum (pi => pi.SaleAmount)
where purchaseValue > 1000
orderby purchaseValue descending
select new
{
   p.Description,
   p.Customer.SalesPerson.Name,
   PurchaseItemCount = p.PurchaseItems.Count()
}
```

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 23:07

​                                                                      

​                                                                     

下面是使用 SQL 实现相同的查询：

```
SELECT 
    p.Description,
    s.Name,
    (SELECT COUNT(*) FROM PurchaseItem pi WHERE p.ID = pi.PurchaseID) PurchaseItemCount	
FROM Purchase p
    LEFT OUTER JOIN 
        Customer c 
            INNER JOIN Address a ON c.AddressID = a.ID
            LEFT OUTER JOIN SalesPerson s ON c.SalesPersonID = s.ID
    ON p.CustomerID = c.ID	
WHERE
    (a.State = 'WA' OR p.CustomerID IS NULL)
    AND p.ID in
    (
        SELECT PurchaseID FROM PurchaseItem
        GROUP BY PurchaseID HAVING SUM (SaleAmount) > 1000
    )
ORDER BY
    (SELECT SUM (SaleAmount) FROM PurchaseItem pi WHERE p.ID = pi.PurchaseID) DESC
```

有意思的是可以将上述 SQL 查询转换回到 LINQ，所生成的查询每一块都会有傻瓜式重复。论坛里常会贴出这样的查询（通常是非工作的版本）——这是用 SQL 进行思考而不是以 [LINQ 进行思考](https://www.linqpad.net/Challenge.aspx)的结果。这就像是是将 Fortran 程序转换成 C# 6 时会抱怨 GOTO 的笨拙语法一样。

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 23:15

​                                                                      

​                                                                     

### 数据修整

在查询联合中从多个表选择数据 -  最终的结果会是一个扁平的以行为单位的元组。如果你使用了多年的  SQL，你可能认为这种事不会发生在你身上——它导致数据重复，从而使得结果集无法在客户端很好地使用。所以当它发生时往往难以接受。与此相反，LINQ   让你可以获取到休整过的分层级的数据。这就避免了重复，让结果集容易处理，而且在大多数情况下也会消除进行联合操作的必要。例如，假设我们想要提取一组顾客，每一条记录都带上了它们的高价值交易。使用  LINQ，你可以这样做：

```
from c in db.Customers
where c.Address.State == "WA"
select new
{
   c.Name,
   c.CustomerNumber,
   HighValuePurchases = c.Purchases.Where (p => p.Price > 1000)
}
```

HighValuePurchases，在这里是一个集合。由于我们查询的是一个相关属性，就不需要进行联合了。因此这是一个内联合还是外联合的细节问题就被很好的抽象掉了。在此例中，当翻译成了  SQL，可能就是一个外联合：LINQ 不会因为子集合返回的是零个元素就排除行。如果我们想要有一个可以翻译成一个内联合的东西，可以这样做:

```
from c in db.Customers
where c.Address.State == "WA"
let HighValuePurchases = c.Purchases.Where (p => p.Price > 1000)where HighValuePurchases.Any()select new
{
   c.Name,
   c.CustomerNumber,
   HighValuePurchases
}
```

LINQ 还通过一组丰富的操作符对平面外联合、自联合、组查询以及其它各种不同类型查询进行了支持。

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 23:31

​                                                                      

​                                                                     

### 参数化

如果我们想要将之前的例子参数化会如何呢，如此"WA"状态是不是就要来自于一个变量呢? 其实我们只要像下面这样做就可以了:

```
string state = "WA";

var query =
   from c in db.Customers
   where c.Address.State == state
   ...
```

不会混淆 DbCommand 对象上面的参数，或者担心 SQL 注入攻击。 LINQ 的参数化是内联、类型安全并且高度可读的。它不仅解决了问题——而且解决得很不错。

因为 LINQ 查询时可以进行组合，所以我们可以有条件的添加谓词。例如，我们写出一个方法，如下：

```
IQueryable<Customer> GetCustomers (string state, decimal? minPurchase)
{
    var query = Customers.AsQueryable();
    
    if (state != null)
        query = query.Where (c => c.Address.State == state);
    
    if (minPurchase != null)
        query = query.Where (c => c.Purchases.Any (p => p.Price > minPurchase.Value));
    
    return query;
}
```

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 23:35

​                                                                      

​                                                                     

如果我们使用空的 state 以及 minPurchase 值调用了这个方法，那么在我们枚举结果集的时候如下 SQL 就会被生成出来：

```
SELECT [t0].[ID], [t0].[Name], [t0].[AddressID]
FROM [Customer] AS [t0]
```

不过，如果我们指定了 state 和 minPurchase 的值，LINQ 到 SQL 就不只是向查询添加了谓词，还会有必要的联合语句：

```
SELECT [t0].[ID], [t0].[Name], [t0].[AddressID]
FROM [Customer] AS [t0]
LEFT OUTER JOIN [Address] AS [t1] ON [t1].[ID] = [t0].[AddressID]
WHERE (EXISTS(
    SELECT NULL AS [EMPTY]
    FROM [Purchase] AS [t2]
    WHERE ([t2].[Price] > @p0) AND ([t2].[CustomerID] = [t0].[ID])
    )) AND ([t1].[State] = @p1)
```

因为我们的方法返回了一个 IQueryable，查询在枚举到之前并不会被实际地转换成 SQL 并加以执行。这样就给了调用进一步添加谓词、分页、自定义投影等等的机会。

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 23:41

​                                                                      

​                                                                     

### 静态类型安全

在之前的查询中，如果我们将 state 变量声明成了一个整型数而不是一个字符串，那么查询可能在如果你还没有沉溺于 LINQ，就会想这有啥大惊小怪的。SQL 并没有坏掉，为什么还要对它进行修补呢? 为什么我们还需要另外一种查询语言呢?

流行的说法是  LINQ 同 C#（或者  VB）集成在了一起，故而消除了编程语言和数据库之间配合上的鸿沟，同时为多个数据源的组合提供了单一的查询接口。虽然这些都是事实，但仅是故事的一部分。更重要的是：当要对数据库进行查询的时候，LINQ  在大多数情况下都比 SQL 更加有效。

同 SQL 相比， LINQ 更简单、整洁而且高级。这样子更像是拿 C# 同 C++ 做比较。真的，尽管有时候使用 C++ 仍然是最好的选择（比如使用 SQL 的场景），但在大多数场景中，使用现代整洁的语言而不必为底层细节操作就是一项大胜利。

SQL 是一门非常古老的语言—发明于 1974 年。虽然经历过了无数此扩展，但从来没有被重新设计过。这就使得它有点混乱了—不像是 VB6 或者 Visual FoxPro。你也许已经慢慢变得习惯于此因而看不到任何错漏的地方!

[                                                              ![LeoXu](233834_50-1568954574412.jpeg)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 22:42

​                                                                      

​                                                                     

让我们来看一个例子。你想要编写一个简单的查询来获取客户数据，如下：

```
SELECT UPPER(Name)
FROM Customer
WHERE Name LIKE 'A%'
ORDER BY Name
```

现在假设要将结果集里的这些数据提供给一个网页，并且我们想获取第 21 到 30 行数据。所以我们需要一个子查询：

```
SELECT UPPER(Name) FROM
(
   SELECT *, RN = row_number()
   OVER (ORDER BY Name)
   FROM Customer
   WHERE Name LIKE 'A%'
) A
WHERE RN BETWEEN 21 AND 30
ORDER BY Name
```

而如果你需要支持版本（在 SQL Server 2005 之前的）更老的数据库，情况会更糟糕:

```
SELECT TOP 10 UPPER (c1.Name)
FROM Customer c1
WHERE
   c1.Name LIKE 'A%'
   AND c1.ID NOT IN
   (
      SELECT TOP 20 c2.ID
      FROM Customer c2
      WHERE c2.Name LIKE 'A%'
      ORDER BY c2.Name
   ) 
ORDER BY c1.Name
```

这样做不仅复杂而混乱，而且也违背了 DRY 原则。如下是使用 LINQ 实现相同的查询功能。显然在简单性上更胜一筹：

```
var query =
   from c in db.Customers
   where c.Name.StartsWith ("A")
   orderby c.Name
   select c.Name.ToUpper();

var thirdPage = query.Skip(20).Take(10);
```

只有当我们枚举到 thirdPage 时，查询才会实际执行。在从  LINQ 到 SQL 或者 Entity Framework 的场景中，翻译引擎会将（我们用两个步骤组合而成的）查询转换成一个 SQL  语句，这个语句是针对其所连接的数据库服务器进行了优化的。

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 22:52

​                                                                      

​                                                                     

### 可组合性

您可能已经注意到 LINQ 的另一个更微妙（微妙但意义重大）的好处。我们选择了组合中的两个查询步骤：

```
IQueryable<T> Paginate<T> (this IQueryable<T> query, int skip, int take)
{
   return query.Skip(skip).Take(take);
}
```

我们可以这样做：

```
var query = ...
var thirdPage = query.Paginate (20, 10);
```

更重要的是，在这里我们可以进行任意的分页查询。换言之就是通过 LINQ 你可以把查询分解成一部分，然后在你的应用程序中重用。

[                                                              ![溪边九节](553781_50-1568954574422.jpeg)                                              ](https://my.oschina.net/crooner)

[溪边九节](https://my.oschina.net/crooner)

翻译于 2017/02/22 18:04

​                                                                      

​                                                                             其它翻译版本 (1)                                             

### 联合

LINQ 另一好处就是你可以不用 JOIN  就能进行关系间查询。例如，我们想要列出所有购物在 $1000  或者以上，并且居住在华盛顿的顾客。我们会假定让购买项目化（也就是经典的采购/项目采购场景）并且把（没有顾客记录的）现金销售也囊括进来。这就需要在四个表（Purchase,  Customer, Address 以及 PurchaseItem）之间进行查询。使用 LINQ，这样的查询不费吹灰之力：

```
from p in db.Purchases
where p.Customer.Address.State == "WA" || p.Customer == null
where p.PurchaseItems.Sum (pi => pi.SaleAmount) > 1000
select p
```

将此与同等功能的 SQL 相比较：

```
SELECT p.*
FROM Purchase p
    LEFT OUTER JOIN 
        Customer c INNER JOIN Address a ON c.AddressID = a.ID
    ON p.CustomerID = c.ID	
WHERE
   (a.State = 'WA' || p.CustomerID IS NULL)
    AND p.ID in
    (
        SELECT PurchaseID FROM PurchaseItem
        GROUP BY PurchaseID HAVING SUM (SaleAmount) > 1000
    )
```

对此例进一步扩展，假设我们想要将结果集按价格进行逆序排列，并在最终的投影中显示销售员的姓名以及所购买项目的数量。我们可以自然不重复地表达出这些附件的查询条件：

```
from p in db.Purchases
where p.Customer.Address.State == "WA" || p.Customer == null
let purchaseValue = p.PurchaseItems.Sum (pi => pi.SaleAmount)
where purchaseValue > 1000
orderby purchaseValue descending
select new
{
   p.Description,
   p.Customer.SalesPerson.Name,
   PurchaseItemCount = p.PurchaseItems.Count()
}
```

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 23:07

​                                                                      

​                                                                     

下面是使用 SQL 实现相同的查询：

```
SELECT 
    p.Description,
    s.Name,
    (SELECT COUNT(*) FROM PurchaseItem pi WHERE p.ID = pi.PurchaseID) PurchaseItemCount	
FROM Purchase p
    LEFT OUTER JOIN 
        Customer c 
            INNER JOIN Address a ON c.AddressID = a.ID
            LEFT OUTER JOIN SalesPerson s ON c.SalesPersonID = s.ID
    ON p.CustomerID = c.ID	
WHERE
    (a.State = 'WA' OR p.CustomerID IS NULL)
    AND p.ID in
    (
        SELECT PurchaseID FROM PurchaseItem
        GROUP BY PurchaseID HAVING SUM (SaleAmount) > 1000
    )
ORDER BY
    (SELECT SUM (SaleAmount) FROM PurchaseItem pi WHERE p.ID = pi.PurchaseID) DESC
```

有意思的是可以将上述 SQL 查询转换回到 LINQ，所生成的查询每一块都会有傻瓜式重复。论坛里常会贴出这样的查询（通常是非工作的版本）——这是用 SQL 进行思考而不是以 [LINQ 进行思考](https://www.linqpad.net/Challenge.aspx)的结果。这就像是是将 Fortran 程序转换成 C# 6 时会抱怨 GOTO 的笨拙语法一样。

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 23:15

​                                                                      

​                                                                     

### 数据修整

在查询联合中从多个表选择数据 -  最终的结果会是一个扁平的以行为单位的元组。如果你使用了多年的  SQL，你可能认为这种事不会发生在你身上——它导致数据重复，从而使得结果集无法在客户端很好地使用。所以当它发生时往往难以接受。与此相反，LINQ   让你可以获取到休整过的分层级的数据。这就避免了重复，让结果集容易处理，而且在大多数情况下也会消除进行联合操作的必要。例如，假设我们想要提取一组顾客，每一条记录都带上了它们的高价值交易。使用  LINQ，你可以这样做：

```
from c in db.Customers
where c.Address.State == "WA"
select new
{
   c.Name,
   c.CustomerNumber,
   HighValuePurchases = c.Purchases.Where (p => p.Price > 1000)
}
```

HighValuePurchases，在这里是一个集合。由于我们查询的是一个相关属性，就不需要进行联合了。因此这是一个内联合还是外联合的细节问题就被很好的抽象掉了。在此例中，当翻译成了  SQL，可能就是一个外联合：LINQ 不会因为子集合返回的是零个元素就排除行。如果我们想要有一个可以翻译成一个内联合的东西，可以这样做:

```
from c in db.Customers
where c.Address.State == "WA"
let HighValuePurchases = c.Purchases.Where (p => p.Price > 1000)where HighValuePurchases.Any()select new
{
   c.Name,
   c.CustomerNumber,
   HighValuePurchases
}
```

LINQ 还通过一组丰富的操作符对平面外联合、自联合、组查询以及其它各种不同类型查询进行了支持。

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 23:31

​                                                                      

​                                                                     

### 参数化

如果我们想要将之前的例子参数化会如何呢，如此"WA"状态是不是就要来自于一个变量呢? 其实我们只要像下面这样做就可以了:

```
string state = "WA";

var query =
   from c in db.Customers
   where c.Address.State == state
   ...
```

不会混淆 DbCommand 对象上面的参数，或者担心 SQL 注入攻击。 LINQ 的参数化是内联、类型安全并且高度可读的。它不仅解决了问题——而且解决得很不错。

因为 LINQ 查询时可以进行组合，所以我们可以有条件的添加谓词。例如，我们写出一个方法，如下：

```
IQueryable<Customer> GetCustomers (string state, decimal? minPurchase)
{
    var query = Customers.AsQueryable();
    
    if (state != null)
        query = query.Where (c => c.Address.State == state);
    
    if (minPurchase != null)
        query = query.Where (c => c.Purchases.Any (p => p.Price > minPurchase.Value));
    
    return query;
}
```

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 23:35

​                                                                      

​                                                                     

如果我们使用空的 state 以及 minPurchase 值调用了这个方法，那么在我们枚举结果集的时候如下 SQL 就会被生成出来：

```
SELECT [t0].[ID], [t0].[Name], [t0].[AddressID]
FROM [Customer] AS [t0]
```

不过，如果我们指定了 state 和 minPurchase 的值，LINQ 到 SQL 就不只是向查询添加了谓词，还会有必要的联合语句：

```
SELECT [t0].[ID], [t0].[Name], [t0].[AddressID]
FROM [Customer] AS [t0]
LEFT OUTER JOIN [Address] AS [t1] ON [t1].[ID] = [t0].[AddressID]
WHERE (EXISTS(
    SELECT NULL AS [EMPTY]
    FROM [Purchase] AS [t2]
    WHERE ([t2].[Price] > @p0) AND ([t2].[CustomerID] = [t0].[ID])
    )) AND ([t1].[State] = @p1)
```

因为我们的方法返回了一个 IQueryable，查询在枚举到之前并不会被实际地转换成 SQL 并加以执行。这样就给了调用进一步添加谓词、分页、自定义投影等等的机会。

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/22 23:41

​                                                                      

​                                                                     

### 静态类型安全

在之前的查询中，如果我们将 state 变量声明成了一个整型数而不是一个字符串，那么查询可能在编译时就会报错，而不用等到运行时。这个也同样适用于把表名或者列名弄错的情况。这在重构时有一个很实在的好处：如果你没有完成手头的工作，编译器会给出提示。

### 客户端处理

LINQ   让你可以轻松地将查询的一些部分转移到客户端上进行处理。对于负载负担较大的数据库服务器，这样做可实际提升性能。只要你所取数据没有超过所需（换言之，你还是要在服务器上做过滤），就可以经常性地通过把对结果集进行重新排序、转换以及重组的压力转移到负载较少的应用服务器上去。使用 LINQ，你需要做的就是  AsEnumerable() 转移到查询之中，而自那个点之后的所有事情都可以在本地执行。

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/23 00:48

​                                                                      

​                                                                     

### 什么时候不用 LINQ 去查询数据库

尽管 LINQ 的功能强大，但是它并不能取代 SQL。它可以满足 95% 以上的需求，不过你有时仍然需要SQL:

- 需要手动调整的查询 (特殊是**需要优化和进行锁定提示的时候**)；
- 有些涉及到要 **select 临时表**，然后又要对那些表进行查询操作的查询；
- 预知的更新以及批量插入操作。

还有就在用到触发器时，你还是需要  SQL。 (尽管在使用 LINQ 的时候诸如此类的东西并非常常被需要，但在要使用存储过程和函数的时候，SQL 是不可或缺的)。你可以通过在  SQL 中编写表值函数来将 SQL 与 LINQ 结合在一起, 然后在更加复杂的 LINQ 查询里面调用这些函数。

了解两门查询语言并不是问题，因为无论如何你都会想要去学习  LINQ 的 — LINQ 在查询本地集合以及 XML DOM 的时候非常实用。如果你使用的仍然是老旧的基于 XmlDocument 的  DOM，LINQ to XML 的 DOM 操作会是一种具有戏剧效果的进步。

还有就是相比于 SQL， LINQ [更易于掌握](https://www.linqpad.net/MasteringLINQ.aspx)，所以如果你想写个不错的查询，使用 LINQ 会比 SQL 更好达成。，而不用等到运行时。这个也同样适用于把表名或者列名弄错的情况。这在重构时有一个很实在的好处：如果你没有完成手头的工作，编译器会给出提示。

### 客户端处理

LINQ   让你可以轻松地将查询的一些部分转移到客户端上进行处理。对于负载负担较大的数据库服务器，这样做可实际提升性能。只要你所取数据没有超过所需（换言之，你还是要在服务器上做过滤），就可以经常性**地通过把对结果集进行重新排序、转换以及重组的压力转移到负载较少的应用服务器上去**。使用 LINQ，你需要做的就是  **AsEnumerable() 转移**到查询之中，而自那个点之后的所有事情都可以在本地执行。

[                                                              ![LeoXu](https://static.oschina.net/uploads/user/116/233834_50.jpeg?t=1509637344000)                                              ](https://my.oschina.net/xuleo)

[LeoXu](https://my.oschina.net/xuleo)

翻译于 2017/02/23 00:48

​                                                                      

​                                                                     

### 什么时候不用 LINQ 去查询数据库

尽管 LINQ 的功能强大，但是它并不能取代 SQL。它可以满足 95% 以上的需求，不过你有时仍然需要SQL:

- 需要手动调整的查询 (特殊是需要**优化和进行锁定提示**的时候)；
- 有些涉及到要 **select 临时表**，然后又要对那些表进行查询操作的查询；
- 预知的**更新以及批量插入操作**。

还有就在用到触发器时，你还是需要  SQL。 (尽管在使用 LINQ 的时候诸如此类的东西并非常常被需要，但在要使用存储过程和函数的时候，SQL 是不可或缺的)。你可以通过在  SQL 中编写表值函数来将 SQL 与 LINQ 结合在一起, 然后在更加复杂的 LINQ 查询里面调用这些函数。

了解两门查询语言并不是问题，因为无论如何你都会想要去学习  LINQ 的 — LINQ 在查询本地集合以及 XML DOM 的时候非常实用。如果你使用的仍然是老旧的基于 XmlDocument 的  DOM，LINQ to XML 的 DOM 操作会是一种具有戏剧效果的进步。

还有就是相比于 SQL， LINQ [更易于掌握](https://www.linqpad.net/MasteringLINQ.aspx)，所以如果你想写个不错的查询，使用 LINQ 会比 SQL 更好达成。