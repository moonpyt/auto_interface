# 1 目录结构

        ├─base                    基础方法包目录
        │  │  db.py               数据库操作方法模块
        │  │  http_request.py     http请求方法的安装
        │  │  date_format.py      时间格式转换相关方法
        │  │  email_send.py       发送邮件
        │  │  read_config.py      对用例中所用到的配置参数进行查询，修改，删除等方法
        │  │  encrypt.py          对数据进行解密
        ├─case                    用例目录
        │  ├─interface
        │  │  ├─evopay            联机用例目录
        │  │  │  ─  QR_single_node_mode      码单节点文件夹，下面是测试文件
        │  │  │  │  ── CPMPayment.py         CPM Payment接口文件测试案例
        │  │  │  ─  QR_double_node_mode     码双节点文件夹，下面是测试文件 
        │  │  │  ─  card_single_node_mode   卡单节点文件夹，下面是测试文件
        │  │  │  ─  card_double_node_mode   卡双节点文件夹，下面是测试文件       
        │  │  ├─evosettle         清分用例目录
        │  │  │  ─  direct_evonet_fileinit.py    直清模式evonet出文件
        │  │  │  ─  direct_wop_fileinit.py       直清模式mop出文件
        │  │  │  ─  wop_to_evonet_fileinit.py    wop向evonet清算，evonet出文件
        │  │  │  ─  upi_fileinit.py              银联出文件模式share_pattern_func.
        │  │  │  ─  share_func.py        四个模式共有的方法封装到这里
        ├─common                   业务基础方法文件夹
        │  ├─evopay                联机的公共文件夹 
        │  │  reponse_check.py 
        │  ├─evosettle             清分公共方法文件夹 
        │  │  analysis_file.py 
        ├─config                  用例配置的相关信息目录
        │  │
        │  └─evopay
        │  │   ─  evopay_staging.ini   不同环境的配置
        │  │   ─  evopay_test.ini  
        │  │   ─  evopay_regression.ini  
        │  │   ─  evopay_production.ini  
        │  │  
        ├─data
        │  │  download_file_dir   存储清分文件的目录，或者是我们需要生成到本地的文件
        │  │  ssh_file_dir        存储服务器秘钥的目录;登录时会用到
        │  │  upload_file_dir     存储需要上传文件的目录
        │  │  evopay_file         联机用到的一些数据目录
        │  │  │  ─	evopay_cpmtoken.ini     联机需要的数据
        │─doc					   项目的一些文档
        │  │  pip_install_list     第三方安装包的参数
        ├─evopay_main              联机调用目录；
        │  ├─evopay					
        │  │  │  test_evonet_trans.py       联机用例
        │  │  │  ─  QR_node_model     码双节点文件夹，下面是码的 test文件 
        │  │  │  ─  card_node_model   卡单信息文件夹， 下面是卡的 test文件 
        │  ├─product                生产（给生产预留）	
        ├─evosettle_main           
        │  ├─evosettle				   清分用例调用目录
        │  │  │  ─  test_direct_evonet_fileinit.py    用例调用文件
        │  │  │  ─  test_direct_wop_fileinit.py       用例调用文件
        │  │  │  ─  test_wop_to_evonet_fileinit.py    用例调用文件
        │  │  │  ─  test_upi_fileinit.py              用例调用文件
        ├─log
        │  ├─evopay              联机日志目录
        │  │      evopay(timetime).log     日志文件以时间戳结尾  
        │  └─evosettle           清分日志目录
        │         evosettle(timetime).log  日志文件，目录以时间戳结尾
        │
        ├─report                 报告目录
        │  └─evopay
        │          report(time.time).html   联机报告
        │  └─evosettle
        │          report(time.time).html.html   清分报告
        │
        └─__pycache__
        conftest                 执行pytest时的传参设置及用例前置条件的相关配置
        

# 2 编码规范 

​	  重点； 见名知意

 	1 类：驼峰式命名。(首字母大写)                              如 HttpPost

 	2 函数和方法：使用小写，如果需要可以加下滑线  如 connct_db

 	3 参数：使用小写， 如果需要可以加下滑线		     如 response_obj

 	4 模块/包名：模块名称小写，可以用下滑线连接    如 evopay_main

 	5 模块(有些缩写名称有特殊含义的可大写)       如 QR_double_node_mode


# 3 用例规范

​	 pytest会找当前以及递归查找子文件夹下面所有的test_*.py的文件

 	1 在上述文件里，pytest会收集下面的一些函数或方法，当作测试用例

 	2 类中的测试方法都以test_开头

 	3 在以Test开头的类中(不能包含 __init__ 方法)(框架的规定,不然执行时会报错)

 	4 Test测试类不能继承类    (框架规定,不然执行 pytest 时会报错)

# 4 环境搭建流程

第三方包的安装

1.  本地安装python3.6.6,jenkins服务器安装的python就是3.6.6
2.  添加python路径到环境变量，将python 的路径和python下的scripts添加到环境变量（自行百度）
3.  访问飞书文件夹url   https://ciloa.feishu.cn/drive/folder/fldcnFIv2YN2IEsw4ogXV2Zij6d
4.  下载 pip_install_list.txt，cmd 切换到和 pip_install_list.txt同目录执行 pip install -r  pip_install_list.tx,安装时不要关闭cmd 终端，不然会终止安装
5.  这样相关的第三方包就安装结束了， 

# 5 项目获取流程

git 相关命令

1. gitlab先将testcode项目fork到自己的远程仓库	

2. 本地克隆自己的远程仓库 git clone  https://git.cardinfolink.net/walkerone/testcode.git

3. 创建分支并切换到对应分支  如  git checkout -b  EVONET-develop-20200723 相当于本地创建了EVONET-develop-20200723，在此分支对 EVONET的用例进行修改

4. 找对应的自动化用例reviewer,代码review之后，提交到自己的远程仓库

   - ​	git branch 检查自己知否在自己切的分支 EVONET-develop-20200723，如不是，则执行

     ​	git checkout   EVONET-develop-20200723  切至对应分支

   - ​    提交 git push origin  EVONET-develop-20200723  （这样代码就提交到了远程分支）

5. 在自己的远程仓库选择自己对应的分支提交  merge  >>>testcode的master分支



