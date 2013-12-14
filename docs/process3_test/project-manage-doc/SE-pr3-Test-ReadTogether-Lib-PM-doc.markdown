% 软件工程 - 第三阶段\
ReadTogether 图书管理系统\
项目管理文档
% MarkAsRead 软工小组
% \today

# Git9使用情况报告

## 整体提交统计信息

从上次阶段结束的11月16日开始，MarkAsRead小组在Git9上一共有71次commits。

![Commits界面截图](commits.png)

![git9主界面，已经有256个提交，可见开发活跃度非常高](git9-main.png)

\FloatBarrier

## Git使用

通过前几个阶段的练习，我们对git的使用变的更加熟练。这一个阶段也是向原型系统添加各种功能。

![Git网络图](network.png)

\FloatBarrier

# IssueTracker使用情况报告

## 整体Issue统计信息

从上次阶段结束的11月16日开始，MarkAsRead小组一共发现并跟踪了9个Issue。内容主要分布在代码风格、安全性、前后端衔接几个方面。

我们充分利用了Issuetracker便捷的邮件提示和论坛式的讨论功能。最后我们成功解决了大部分发现的Issue，只剩下了2个Issue留待以后解决。

![Issuetracker使用情况截图](issue.png)

\FloatBarrier

# 其他辅助工具的使用

![Git9代码交流，在这里我们可以分享好的代码实现](snippets.png)

![wiki极大的帮助我们分享工具的使用、交流编码经验和进行内部设计约定](wiki.png)

\FloatBarrier

# 项目分工

\begin{table}[h]
\begin{tabular}{l | l}
姓名  & 主要职责        \\
\hline
武祥晋 & 组长、前后端衔接、测试 \\
涂珂  & 数据库设计与管理    \\
傅左右 & 前端设计、项目管理文档 \\
秦同  & 前端设计、测试     \\
李响  & 测试文档        \\
张思浩 & 关键测试       
\end{tabular}
\end{table}

# 项目进度安排

- 2013-11-17 至 2013-11-25

	进行初次讨论。由组长武祥晋同学研究Django1.6新版本特性、迁移方案以及了解相关的测试工具。相关文档发布至Git9上的wiki供组内同学充分参考。

- 2013-11-25 至 2013-12-10

	负责测试的同学充分了解测试工具的使用和测试目的。

- 2013-11-11 至 2013-12-14

	进行所有测试。对系统的各个模块进行充分细致的测试。

# 阶段总结

在这一个阶段里，我们又圆满的完成了任务。首先我们大大的完善了我们的图书管理系统，向原型系统中补充和添加了需求和设计文档相应的要求。

然后我们使用了Django Unittest、Selenium、Coverage、Pylot诸多工具完成了对我们图书管理系统的单元测试、集成测试、覆盖率测试、负载测试。我们的图书馆有着良好的性能和稳定性。

通过软件测试，我们对软件工程的测试流程有了进一步的认识，也对我们编写的图书管理系统的功能完善和稳定性有了更多的信心。

# [附录] 11-18 Django研究记录

计划包括以下内容：字符编码、时区、显示格式

### 名词定义

- Internationalization: 缩写i18n，程序中为l10n所做的准备。
- localization: 缩写l10n，包括翻译和格式化。
- Translation: 文字翻译。Django中的 `USE_I18N` 设置。
- Formatting: 日期时间、数字等的格式化。Django中的 `USE_L10N` 设置。
- locale: 语言或语言+地区，语言小写国家大写，如 *zh_CN* 、 *en_US* 。
- HTTP Accept-Language code: *zh-cn* 。（我看Chrome是 *zh-CN* ）
- message file: 即 `.po` 文件。
- translation string: 待翻译的字符串。
- format file: 定义了特定locale数据格式的Python模块（module）。
- naive datetime: 无时区信息。
- aware datetime: 有时区信息，时间为该时区时间。

### 相关Django设置

USE_I18N、LANGUAGE_CODE、LANGUAGE_COOKIE_NAME、LANGUAGES、LOCALE_PATHS；
USE_L10N、USE_THOUSAND_SEPARATOR、FORMAT_MODULE_PATH
USE_TZ、TIME_ZONE

`TEMPLATE_CONTEXT_PROCESSORS`
- `django.core.context_processors.i18n`
- `django.core.context_processors.tz`

`MIDDLEWARE_CLASSES`
- `django.middleware.locale.LocaleMiddleware`

## 时区

Python的 `datetiime` 模块包含以下类：
- `date`
- `datetime`
- `time`
- `timedelta`
- `tzinfo`
Django的 `django.utils.timezone` 模块包含以下函数：
- `now`
- `is_aware`
- `is_naive`
- `make_aware`
- `make_naive`

### 参考资料

- [Django 1.5 topics/i18n/timezones](https://docs.djangoproject.com/en/1.5/topics/i18n/timezones/)
- [pytz](http://pytz.sourceforge.net/)
- [datetime](http://docs.python.org/2.7/library/datetime.html)
- [MySQL 5.5 服务器时区支持](http://dev.mysql.com/doc/refman/5.5/en/time-zone-support.html)

# [附录] 11-25 测试工具研究记录

## testing

主要是在 `tests.py` 中定义 `django.test.TestCase` 的子类进行unit test，可以不用doctest。

## testing/overview

使用 `from django.utils import unittest` 而不是 `import unittest` 。一般直接使用 `from django.test import TestCase` 而不要使用 `unittest.TestCase` ，除非你对此很了解。即 `unittest` 要用Django的不用Python自带的， `TestCase` 要用test包的不用unittest包的。

使用 `python manage.py test` 运行测试，一次Ctrl-C安全退出，第二次强制退出。具体指令格式另行整理。运行测试时无需用 `python manage.py runserver` 启动一个服务器。

*It is a bad idea to have such import-time database queries in your code anyway - rewrite your code so that it doesn’t do this.*

### test client

`django.test.client.Client`

用于检查正确的模版是否被渲染，以及是否从view得到正确的变量。不能取代 [Selenium](http://seleniumhq.org/) 。后者用于模拟浏览器检查HTML是否正确以及JavaScript功能是否正确。后者的使用需要配合 `LiveServerTestCase` 。

### `django.test` 包中的 `django.utils.unittest.TestCase` 的子类

- `SimpleTestCase`
- `TransactionTestCase`
- `TestCase`
- `LiveServerTestCase`

### 特性

`TestCase` 的子类可直接使用 `self.client` 而无需自己构造 `Client` 。

fixture加载。

自定义测试用的urlconf。相当于测试中的URL Reverse。

临时自定义设置。

各种Assertion。

## testing/advanced

### The request factory

独立测试view函数用的。

### 自定义测试框架

### 与 coverage.py 集成

在开启 coverage 的情况下运行测试： `coverage run --source='.' manage.py test myapp`

显示报告： `coverage report` 或 `coverage html`

## Other Tools

- [cucumber](https://github.com/cucumber/cucumber/wiki/Python)
- [Lettuce](http://lettuce.it/intro/overview.html)
- [splinter](http://splinter.cobrateam.info/)
- [Guide with Django](http://cilliano.com/2011/02/07/django-bdd-with-lettuce-and-splinter.html)

Selenium -> Capybara -> Cucumber
Capybara = Pycabara
Rspec = [should-dsl](https://github.com/rodrigomanhaes/should-dsl/tree/matchers-as-functions), PySpec

SpecLoud uses nose with beautiful syntax and highlight with green & red
ludibrio provides mocks & stubs

Gherkin syntax: Pyccuracy, lettuce, freshen, behave
pycuke is dead, use freshen instead; freshen is dead, uses nose, complex!
behave > lettuce: pythonic, use test database, but poor with django

# [附录] 11-30 python学习小记

启用Python 2.7的警告 `-Wd`

Python 3兼容？ `-3` 警告开关

`__future__` 特性

列表综合，元组pack/unpack

字符串格式化

# [附录] 12-13 会议记录

以下url对应的行为解释：

- borrow: 对于一本在架上的书，管理员登记其被借走（copy_id, myuser_id）
- return: 对于一本借出的书，管理员收到了用户的归还，处于“整理中”（同时通知预约的用户）
- queue_next: 被通知的预约用户向管理员取走了书
- readify: 整理中的书被摆到架上
- disappear: 被借出的书已经向管理员赔偿，被标记为永久丢失

新书上架、图书永久下架先不考虑。

方便管理员的用户查询、拷贝查询、图书查询 AJAX GET 接口稍后讨论。

