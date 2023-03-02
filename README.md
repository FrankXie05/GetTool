# GetTool
获取vcpkg最新master的端口下的vcpkg.json所有信息，目前主要是 name 和 version.

配置环境：
  1. python3.8以上
  2. 目前使用QQ邮箱来发送：QQ的SMTP服务，这就需要你在你的QQ邮箱的设置当中开启STMP并且获取授权码

注意：
  BeautifulSoup：这个python包在导入是需要注意两点：

    1. pip必须是最新的版本
    2. 旧的包已经舍弃，安装新包名: beautifulsoup4.
