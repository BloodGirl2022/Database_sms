'''
这里我们使用Flask中的SQLAlchemy来定义数据库模型，
1. 包括四个表：学生信息表（Student）、班级信息表（Class）、课程信息表（Course）和学生选课信息表（StudentCourse）。每个表都对应一个ORM类.
2. 其中包括表的结构以及与其他表的关联关系。例如，学生信息表中的班级号（class_id）是一个外键，指向班级信息表中的班级号（class_id）。
'''
import pymysql
from flask_sqlalchemy import SQLAlchemy
# from all import app
from flask import Flask
from datetime import datetime  # 导入 datetime 模块用于获取当前时间
# ==============================================================#
app = Flask(__name__)
# ==============================================================#
# 创建链接数据库
pymysql.install_as_MySQLdb()
# 初始化 建库链接库 初始化库
class Config():
    DEBUG = True
    # 数据库链接配置 = 数据库名称://登录账号:登录密码@数据库主机IP:数据库访问端口/数据库名称?charset=编码类型
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/sms_database?charset=utf8"  # 手动创建数据库
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True

app.config.from_object(Config)
# 链接数据库
db = SQLAlchemy(app)
# ==============================================================#
class Student(db.Model):  # 创建学生信息表的 ORM 类
    '''
    1. 其中，使用 db.ForeignKey 定义外键关系，表示该属性引用了其他表的主键。
    2. 同时，datetime.now() 用于获取当前时间，即学生信息的默认出生日期。
    '''
    __tablename__ = 'student_info'  # 指定表名为 student_info
    student_id = db.Column(db.String(20), primary_key=True,unique=True)  # 学号，主键(没有设置为自增)
    student_name = db.Column(db.String(20), nullable=False)  # 姓名，非空
    gender = db.Column(db.String(2), nullable=False)  # 性别，非空
    birthday = db.Column(db.DateTime, nullable=False, default=datetime(2000, 1, 1))  # 出生日期，非空，默认为2000.1.1
    class_id = db.Column(db.String(20), db.ForeignKey('class_info.class_id'), nullable=False)  # 班级号，外键，非空
    contact = db.Column(db.String(20), nullable=False)  # 联系方式，非空

class Class(db.Model):  # 创建班级信息表的 ORM 类
    __tablename__ = 'class_info'  # 指定表名为 class_info
    class_id = db.Column(db.String(20), primary_key=True)  # 班级号，主键
    class_name = db.Column(db.String(20), nullable=False)  # 班级名称，非空
    department = db.Column(db.String(20), nullable=False)  # 所属院系，非空

class Course(db.Model):  # 创建课程信息表的 ORM 类
    __tablename__ = 'course_info'  # 指定表名为 course_info
    course_id = db.Column(db.String(20), primary_key=True)  # 课程号，主键
    course_name = db.Column(db.String(20), nullable=False)  # 课程名称，非空
    credit = db.Column(db.Integer, nullable=False)  # 学分，非空
    teacher = db.Column(db.String(20), nullable=False)  # 开课教师，非空

class StudentCourse(db.Model):  # 创建学生选课信息表的 ORM 类
    __tablename__ = 'student_course'  # 指定表名为 student_course
    id = db.Column(db.Integer, primary_key=True)  # 自增主键
    student_id = db.Column(db.String(20), db.ForeignKey('student_info.student_id'), nullable=False)  # 学号，外键，非空
    course_id = db.Column(db.String(20), db.ForeignKey('course_info.course_id'), nullable=False)  # 课程号，外键，非空
    score = db.Column(db.Integer, nullable=True)  # 成绩，可为空

# ==============================================================#
# 执行
with app.app_context():  # debug的时候加这句不会错
    db.drop_all()  # 删除所有表
    db.create_all()  # 创建所有表
    db.session.commit()
# ==============================================================#