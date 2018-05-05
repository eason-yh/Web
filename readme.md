项目名为微型博客
目前实现功能
1，用户注册及登录
2，密码通过hash加密传入数据库
3，用户编辑个人信息，上传头像（简单处理，并未完善）
4，用户可编辑属于自己的内容，目前仅支持插入，没有删除和更新内容的功能

环境
项目基于 Python2.7，sqlite3，其余依赖请参考requirements.txt

错误
如运行过程中出现错误，请自行解决

追述
本项目会持续更新，如有问题可发邮箱到 eason19890916@gmail.com ，看到会及时回复，不过大部分时间应该不会看到

下一步目标
下一步准备实现的有：报错的优化，bug的修改，文本框的整合，更加合理的布局方式，日志记录等
之后会有：个人自定义上传头像，内容页的字段增加，功能增加，增加管理员权限及审核，等级，评论和收藏，点赞等

此次上传版本是在 pycharm下开发的，会带有一些你可能需要或许也不需要的东西，代码下载之后，可以自行处理

第二目标完成情况
报错优化，flask的flash的优化，文本框的前端优化，内容页可以删除，目前仅支持添加新的内容，编辑按钮目前没有实现功能，
用户不需要登录遍可以在首页查看文章，收藏按钮目前只展示后台添加的数据，用户收藏并未实现

下一步目标：
布局这个事情不能操之过急，前端东西太多，js 和 ajax 都不会
增加一个管理员的权限和后台，自定义头像上传
