# Django-blog
演示地址：http://dyeed.pythonanywhere.com/

Django Web
- 前端：Bootstrap 3.X
- Django 2.0.X
- Python 3.6

环境
```
$virtualenv --python=python3 myvenv
()$pip install -r requirements.txt
```
# 功能
- 首页：逆序文章列表，最近文章、归档、分类、标签。。。
- 创建、修改、删除博客
- 创建、审核评论

## 模型
```
.博客Post
--标题title
--内容text
--发布时间published_date
--创建时间created_date
--作者author

.评论Comment
--外键-博客post
--作者author
--内容text
--创建日期created_date
--审核（布尔）approved_comment

```

# To-Do
- [x] 界面-使用新的UI界面
- [x] 功能-博文Markdown支持
- [ ] 功能-时间线
- [ ] 文章分类
- [ ] 点赞
- [ ] 全文搜索|标题搜索
- [x] 文章归档
- [ ] 。。。