# Django-blog
演示地址：http://dyeed.pythonanywhere.com/

Django Web
- 前端：Bootstrap 3.X
- Django 2.0.X
- Python 3.6

环境
```
$virtualenv --python=python3.6 myvenv
(mvenv) $  pip install django whitenoise

Django==2.0.5
whitenoise==3.3.1

```
# 功能
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
- [ ] 界面-使用新的UI界面
- [ ] 功能-博文Markdown支持
- [ ] 功能-时间线
- [ ] 模型-增加博文栏目（分类）、点赞
- [ ] 。。。