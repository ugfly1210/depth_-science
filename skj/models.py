from django.db import models
from django.contrib.contenttypes.models import  ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
# Create your models here.


# ######################## 深科技 ########################
class ArticleSource(models.Model):
    """文章来源"""
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """文章资讯"""
    title = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="标题")
    source = models.ForeignKey("ArticleSource", verbose_name="来源")
    article_type_choices = ((0, '资讯'), (1, '视频'))
    article_type = models.SmallIntegerField(choices=article_type_choices, default=0)
    brief = models.TextField(max_length=512, verbose_name="摘要")
    head_img = models.CharField(max_length=255)
    content = models.TextField(verbose_name="文章正文")
    pub_date = models.DateTimeField(verbose_name="上架日期")
    offline_date = models.DateTimeField(verbose_name="下架日期")
    status_choices = ((0, '在线'), (1, '下线'))
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="状态")
    order = models.SmallIntegerField(default=0, verbose_name="权重", help_text="文章想置顶，可以把数字调大，不要超过1000")
    vid = models.CharField(max_length=128, verbose_name="视频VID", help_text="文章类型是视频, 则需要添加视频VID", blank=True, null=True)
    comment_num = models.SmallIntegerField(default=0, verbose_name="评论数")
    agree_num = models.SmallIntegerField(default=0, verbose_name="点赞数")
    view_num = models.SmallIntegerField(default=0, verbose_name="观看数")
    collect_num = models.SmallIntegerField(default=0, verbose_name="收藏数")

    # tags = models.ManyToManyField("Tags", blank=True, verbose_name="标签")
    date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")

    position_choices = ((0, '信息流'), (1, 'banner大图'), (2, 'banner小图'))
    position = models.SmallIntegerField(choices=position_choices, default=0, verbose_name="位置")

    # comment = GenericRelation("Comment")  # 用于GenericForeignKey反向查询， 不会生成表字段，切勿删除，如有疑问请联系老村长

    def __str__(self):
        return "%s-%s" % (self.source, self.title)


class Collection(models.Model):
    """收藏"""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    account = models.ForeignKey("Account")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('content_type', 'object_id', 'account')


class Comment(models.Model):
    """通用的评论表"""
    # content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name="类型")
    # object_id = models.PositiveIntegerField(blank=True, null=True)
    # content_object = GenericForeignKey('content_type', 'object_id')
    # FK(Article)
    article = models.ForeignKey('Article')
    p_node = models.ForeignKey("self", blank=True, null=True, verbose_name="父级评论")
    content = models.TextField(max_length=1024)
    account = models.ForeignKey("Account", verbose_name="会员名")
    disagree_number = models.IntegerField(default=0, verbose_name="踩")
    agree_number = models.IntegerField(default=0, verbose_name="赞同数")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

# ######################## 用户 ########################
class Account(models.Model):
    username = models.CharField("用户名", max_length=64, unique=True)
    password = models.CharField('password', max_length=128)

class UserAuthToken(models.Model):
    """
    用户Token表
    """
    user = models.OneToOneField(to="Account")
    token = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)


