## Sequoia选股系统
### 简介
本程序使用[AKShare接口](https://github.com/akfamily/akshare) 从东方财富获取数据。

本程序实现了若干种选股策略，大家可以自行选择其中的一到多种策略组合使用，参见[work_flow.py](https://github.com/sngyai/Sequoia/blob/master/work_flow.py#L28-L38) ，也可以实现自己的策略。

各策略中的`end_date`参数主要用于回测。

## 准备工作:
###  环境&依赖管理
推荐使用 Miniconda来进行 Python 环境管理 [Miniconda — conda documentation](https://docs.conda.io/en/latest/miniconda.html)

windows版本直接安装后，用cmd打开，并且创建对应的专属环境

安装 conda 后，切换到项目专属环境进行配置，例如：
```
conda create -n sequoia39 python=3.9
conda activate sequoia39
```
 ### 将conda环境配置到idea中（Project structure）

 ### 根据不同的平台安装TA-Lib程序
* Windows

    下载 [ta-lib-0.4.0-msvc.zip](http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-msvc.zip)，解压到 ``C:\ta-lib``

 ### 推荐使用Python3.8以上以及pip3
 ### Python 依赖:
 也可以直接点击idea的install requirements.txt 来进行设置

 
 部分依赖没办法用conda的源来进行设置，还是需要用pip install的方法安装，比如wxpusher-2.2.0
 
 部分依赖包，低版本通过conda安装失败了，这里避免包安装冲突，还是用项目中的包好了，比如pandas==2.2.0
 ```
 pip install -r requirements.txt 
 ```
 ### 更新akshare数据接口
 本项目已切换至akshare数据接口，该项目更新频率较高，使用前建议检查接口更新
 注意，默认版本很容易不对，需要及时更换akshare的版本号
``` 
pip install akshare --upgrade
```
 ### 生成配置文件

windows命令行不方便操作直接复制粘贴一个出来就好了，复制到更目录下，改下名字

```
cp config.yaml.example config.yaml
```
## 运行
### 本地运行
```
$ python main.py
```
运行结果查看 logs 目录下生成的日志文件 格式为 `logs/sequoia-$YEAR-$MONTH-$DAY-$HOUR-$MINUTE-$SECOND.log`
如：`logs/sequoia-2023-03-03-20-47-56.log`

目前windows上直接运行会报错，待调试

### 服务器端运行
#### 定时任务
服务器端运行需要改为定时任务，共有两种方式：
1. 使用Python schedule定时任务
   * 将[config.yaml](config.yaml.example)中的`cron`配置改为`true`，`push`.`enable`改为`true`

2. 使用crontab定时任务
   * 保持[config.yaml](config.yaml.example)中的`cron`配置为***false***，`push`.`enable`为`true`
   * [安装crontab](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804)
   * `crontab -e` 添加如下内容(服务器端安装了miniconda3)：
   ```bash
    SHELL=/bin/bash
    PATH=/usr/bin:/bin:/home/ubuntu/miniconda3/bin/
    # m h  dom mon dow   command
    0 3 * * 1-5 source /home/ubuntu/miniconda3/bin/activate python3.10; python3 /home/ubuntu/Sequoia/main.py >> /home/ubuntu/Sequoia/sequoia.log; source /home/ubuntu/miniconda3/bin/deactivate
   ```
#### 微信推送
使用[WxPusher](https://wxpusher.zjiecode.com/docs/#/)实现了微信推送，用户需要自行获取[wxpusher_token](https://wxpusher.zjiecode.com/docs/#/?id=%e8%8e%b7%e5%8f%96apptoken)和[wxpusher_uid](https://wxpusher.zjiecode.com/docs/#/?id=%e8%8e%b7%e5%8f%96uid)，并配置到`config.yaml`中去。


## 如何回测
修改[config.yaml](config.yaml.example)中`end_date`为指定日期，格式为`'YYYY-MM-DD'`，如：
```
end = '2019-06-17'
```

