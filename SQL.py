import pymysql as mysql
from datetime import datetime
import sys

class Mysqlhelper:
    #对数据库进行初始化
    def __init__(self):
        # 配置内网接口
        self.config = {'host': '10.5.10.16', #服务器地址
                       'user': 'lidar',      #用户名
                       'password': 'lidar-password123',#用户密码
                       'db': 'lidar_status',   #数据库名称
                       'port': 3306,           #数据库接口
                       'charset': 'utf8',      #数据库编码方式
                       'connect_timeout': 5,}   #设置数据库连接超时时间
        # 外网接口配置
        self._config = {'host': '58.241.11.181',
                        'user': 'lidar',
                        'password': 'lidar-password123',
                        'db': 'lidar_status',
                        'port': 63306,
                        'charset': 'utf8',
                        'connect_timeout': 5,}
        self.status_info = '初始化完成'
        try:
            self.conn = mysql.connect(**self.config)  #首先尝试使用内网连接数据库
            print('数据库连接成功')
            self.status_info = '数据库连接成功'
        except Exception as e:
            self.conn = mysql.connect(**self._config) #当内网连接是被，尝试使用外网连接数据库
            print('数据库连接成功')
            self.status_info = '数据库连接成功'
        except :
            print('数据库连接失败，请依次检查网络和数据库接口配置') #当上述方式均失败时，上报错误，退出程序
            input('<按enter键退出程序>')
            sys.exit()








    #开始查询数据
    def execute(self,sql,flag = False):
        #对查询的数据进行输入
        try:
            with self.conn.cursor() as self.cur:#获得数据库游标
                try:
                    self.cur.execute(sql)     #执行相应的操作
                    if flag:
                         return self.cur.fetchone() #查询单条数据
                    else:
                        return self.cur.fetchall() #查询所有数据
                except:
                        print('需要查询数据配置错误')
                        self.status_info = '需要查询数据配置错误'
        except mysql.err.OperationalError as e: #当出现连接错误时，重起连接
            self.__init__()
            self.execute(sql,flag = False)
        except:
            print('数据查询错误')
            self.status_info ='数据查询错误'


            #对雷达的状态进行自动更新，只针对于数据库中故障类型为1的雷达
    def up_date(self):
        #首先获取故障雷达的sn码
        sql = r"select lidar_sn, station_name, manager,region,is_error,error_type from lidar_config where is_error ='1';"
        n = 0 #初始化雷达更新次数
        num=0 #初始化雷达监测数目
        for sn, station, manager, region, status, error_type in self.execute(sql): #获取正常雷达sn号
            # sql2 = r"select event_time, event_status, sn from lidar_info where sn = '{0}' ".format(sn)
            sql2 = r"select event_time, event_status ,sn from lidar_info where sn='{0}' order by event_id desc limit 1".format(sn) #对正常雷达数据进行检索
            res2 = (self.execute(sql2, flag=True))
            if not res2:
                print(f'当前{sn}无回传数据')
                self.status_info = f'当前{sn}无回传数据'
            else:
                print(f'正在检查{sn}状态')
                self.status_info =f'正在检查{sn}状态'

                lasttime = res2[0]
                now = datetime.now()
                delta = lasttime - now if lasttime > now else now - lasttime
                if delta.total_seconds() < 3600:  #当数据在1h内刷新时，判断为设备恢复
                    sql3 = r"UPDATE lidar_config SET is_error=%s , error_type=%s WHERE lidar_sn = %s;"  #设置雷达状态为正常
                    args1 = ('0', ' ', f'{sn}')
                    try:
                        # 执行SQL语句
                        self.cur.execute(sql3,args1)
                        self.conn.commit()
                    except:
                        # 发生错误时回滚
                        print(f'\033[41m更新{sn}时发生错误')
                        self.status_info = f'更新{sn}时发生错误'

                    print(f'\033[0m已更新{sn}状态配置')  #获取正常运行的雷达的sn码
                    self.status_info =f'已更新{sn}状态配置'
                    n = n+1
            num = num+1
            print(f'\033[0m已经检测了{num}个雷达')
            self.status_info =f'已经检测了{num}个雷达'

        print(f'\033[0m一共更新了{n}条数据')
        self.status_info =f'一共更新了{n}条数据'



    #根据sn码查询单个雷达配置信息
    def lidar_search_con(self,sn):
        self.__init__()
        sql = f"select station_name, manager,region,is_error,error_type from lidar_config where lidar_sn='{sn}';"
        try:
            con = self.execute(sql)
            print(con)
            string = '雷达编号：{}  雷达站点:{}   负责人:{}   所在区域:{}   雷达状态:{}   雷达故障原因:{}'.format(sn,con[0][0],con[0][1],con[0][2],con[0][3],con[0][4])
            print(string)
            self.status_info = string
        except:
            print('雷达编号错误:',f'{sn}')


    #根据SN码查询单个雷达的状态
    def lidar_search_status(self, sn):
        self.__init__()
        sql = r"select event_time, event_status from lidar_info where sn='{0}' " \
                  "order by event_id desc limit 1".format(sn)
        res = self.execute(sql,flag=True)   #获取检索的结果

        if res: #判断是够有检索结果
            print(res)
            if res[1] == '1':   #当雷达的状态未1时，说明雷达状态正常
                status =  '正常'
            else:
                status = '不正常' #否则说明雷达不正常
            string = '雷达编号：{}，最后上传状态的时间是：{}，雷达的状态是：{}'.format(sn,res[0],status)
            print(string)

        else:
            string = '该雷达从未上传过数据'
            print(string)

    # 删除雷达配置记录
    def __delete_lidar__(self, sql, args):
        print('雷达的sn码重复，是否删除数据库中的SN码记录？需要删除请输入管理员密码')
        password1 = 7577153
        password2 = int(input('请输入管理员密码：'))
        self.__init__()
        if password1 == password2:
            with self.conn.cursor() as cur:
                result = cur.execute(sql, args[0])
                print('雷达记录删除成功')
                self.conn.commit()
        else:
            print('密码错误，请慎重操作！')

    # 提交新的雷达配置信息
    def insert(self, args):
        self.__init__()
        sql = 'INSERT INTO lidar_config VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        try:                                 #尝试新增雷达信息配置信息
            with self.conn.cursor() as cur:
                try:
                    cur.execute(sql,args)
                    print('记录已提交成功')
                    self.conn.commit()
                except:
                    print('有空格未填！！')

        except mysql.err.IntegrityError as err:
            sql = 'DELETE FROM lidar_config WHERE lidar_sn = %s;' #当雷达sn号重复时，询问是够删除数据库中信息
            args = (f'{args[0]}',)  # 单个元素的tuple写法
            try:
                self.__delete_lidar__(sql, args)  #删除数据库中重复雷达信息
            except:
                print('删除原始数据信息过程出错')
        except Exception as e:
            print(e)
            print('提交出错：',f'{e}')
        # except mysql.err.OperationalError as e:
        #     print('正确了')







    # 上报雷达故障
    def update_error(self,args):
        self.__init__()
        sql = 'UPDATE lidar_config SET is_error="{}" , error_type="{}" WHERE lidar_sn = "{}";'.format(args[1],args[2],args[0])
        print(args[1],args[2],args[0])
        try:
            with self.conn.cursor() as cur:
                result = cur.execute(sql)
                self.conn.commit()

                print('故障雷达信息上传成功!!')
        except :

            print('故障雷达信息填写错误')



    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print('{} 任务结束，断开连接！'.format(self.__class__.__name__))

if __name__ == "__main__":
    #进行数据库连接
    with Mysqlhelper() as sqlhelper:


        # sql = r"select event_time, event_status, sn from lidar_info where sn = '{}' order by event_id desc limit 20 ".format('ZK3CH140608')
        # # # sql = "select event_time, event_status from lidar_info where sn='{0}' order by event_id desc limit 1"
        # res = sqlhelper.execute(sql, flag=False) #s
        # for row in res:
        #     print(row)

        #更新正常雷达配置信息
        # sqlhelper.up_date()

        #上报新的雷达配置信息
        # args2 = ('QH123', '乔浩站', '乔浩中心', '121', '30', '无锡', '江苏', '乔浩', '3', '客户', '高能雷达','江苏')
        # sqlhelper.insert(args2)

        #
        # # 查询雷达配置信息
        sqlhelper.lidar_search_con('ZK3CH140608')
        # 查询雷达自身状态
        sqlhelper.lidar_search_status('ZK3CH140608')

        #上报雷达故障信息
        args1 = ('ZK20151026','3','缺少外网连接')
        sqlhelper.update_error(args1)





