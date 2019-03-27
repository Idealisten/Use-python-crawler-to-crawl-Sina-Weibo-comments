# 使用Python爬虫爬取新浪微博评论
## 整体思路
有移动版肯定是爬取移动版啦，比PC版简洁太多
要爬每一条微博下的每一条评论，先把一条微博下的所有评论爬下来，再想办法逐条爬取呗

## 爬取单条微博
由于微博对爬虫不是很友好，所以第一步先登陆微博PC站（因为在m站找不到cookie）记录下自己的cookie和user-agent，这样会让微博觉得你不是一个爬虫而是一个真人
记录方法为：右键→检查→network选项卡→ www.weibo.com →headers，在里面就可以找到你的cookie和user-agent信息了，复制下来即可
![](https://i.bmp.ovh/imgs/2019/03/0d293b7d167eceba.jpg)
打开一条微博，发现其URL格式为 https://m.weibo.cn/detail/123456789 ，所以我猜测123456789为这条微博的ID，然后每条微博都有其唯一的ID，那么微博的评论在哪里呢？先在网页源代码里搜了一下，发现并没有相关评论，那么肯定是用某种动态方法进行传输的，按照常规思路，我在network下的XHR选项卡里发现了一个叫hotflow?XXX的文件，里面是一个json文件，果然我要的评论就在里面，还有评论者昵称、评论者ID、评论时间等等，"ok"的值1/0代表该微博有无评论。
![](https://i.bmp.ovh/imgs/2019/03/1ea8ecccd78cf864.png)
如何获取这个json呢？打开headers看到它请求了一个URL: https://m.weibo.cn/comments/hotflow?id=123456789&mid=123456789&max_id_type=0 ，发现这里的id与mid和微博URL里的ID一样，这么不简单了吗。直接请求这个URL获取json，然后只需要把json转换为字典就可以提取出我要的信息啦哈哈哈

## 爬取所有微博
既然已经可以爬取一条微博下的所有评论了，那么只需要想办法对每条微博挨个爬取就OK了
打开她的微博主页，发现首页只有那么几条微博，侧边栏进度条拉到最下面出现”全部微博“字样，点击后每次把进度条拉到最下面都会自动加载更之前的微博，那么也是异步加载没错了，右键→检查，回到XHR选项卡，然后继续滑动滚轮，发现每次加载新的微博时都会出现一个名叫getIndex?containerid=XXXXXXXX的文件，打开这个文件，是一个json，preview，在data->cards->[0/1/.../8/9]->mbolg->id下发现了一串数字，这个ID引起了我的注意，经过对比发现，这个ID就是微博的ID
![](https://i.bmp.ovh/imgs/2019/03/d39194b3b3cd40e0.png)
也就是说只要获取到这个json就可以获取到接下来10条微博的ID，在上一步中我们已经知道有了微博ID就可以爬下该微博下所有的评论信息。
那么如何获取这个json呢？从preview切换到headers，发现它请求了一个URL： https://m.weibo.cn/api/container/getIndex?containerid=2304136486443586_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=2 ，我一眼看到最后的page=2，立马想到很有可能是通过page=1、2、3...来进行分页的，为了验证我的猜想，我又向下拉了进度条，果然在之后的getIndex?containerid文件中page依次增加，而containerid不变
![](https://i.bmp.ovh/imgs/2019/03/fc3b20333954d037.png)

## 总结
首先要获取getIndex?containerid这个文件种的json，这个json中包含了下面10条微博的ID，获取方式为请求一个有规律的URL: https://m.weibo.cn/api/container/getIndex?containerid=2304136486443586_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=2 ，通过控制page参数我们就可以获取到所有的getIndex?containerid文件，继而获取到所有的微博ID，有了所有的微博ID就可以获取所有微博下的评论了
