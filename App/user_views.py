from flask import Blueprint,render_template,request,redirect,url_for,session

from App.models import db,Grade,Student,Role,User,Permission

user_blueprint = Blueprint('user',__name__)

# 首页
@user_blueprint.route('/index/')
def index():
    return render_template('index.html')

@user_blueprint.route('/head/')
def hand():
    user = session['username']
    return render_template('head.html',user=user)

@user_blueprint.route('/left/')
def left():
    return render_template('left.html')

# 返回班级页面
@user_blueprint.route('/grade/')
def grade():
    page = int(request.args.get('page',1))
    page_num = 2
    paginate = Grade.query.order_by('g_id').paginate(page,page_num)
    grades = paginate.items
    return render_template('grade.html',grades=grades,paginate=paginate)


# 创建数据库
@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'

# 添加班级
@user_blueprint.route('/addgrade/',methods=['GET','POST'])
def addgrade():
    if request.method == 'GET':
        return render_template('addgrade.html')
    if request.method == 'POST':
        grade_name = request.form.get('grade_name')
        grade = Grade()
        grade.g_name = grade_name
        db.session.add(grade)
        db.session.commit()
        return redirect(url_for('user.grade'))

# 返回学生列表
@user_blueprint.route('/student/')
def student():
    stus = Student.query.all()
    return render_template('student.html',stus=stus)

# 添加学生
@user_blueprint.route('/addstu/',methods=['GET','POST'])
def addstu():
    if request.method == 'GET':
        grades = Grade.query.all()
        return render_template('addstu.html',grades=grades)
    if request.method == 'POST':
        stu = Student()
        s_name = request.form.get('s_name')
        g_id = request.form.get('grade_id')
        stu.s_name = s_name
        stu.grades = g_id
        db.session.add(stu)
        db.session.commit()
        return redirect(url_for('user.student'))

# 通过班级展示学生列表
@user_blueprint.route('/show_stu_by_grade/<int:id>/')
def show_stu_by_grade(id):
    grade = Grade.query.get(id)
    stus = grade.students
    return render_template('student.html',stus=stus)

# 删除班级
@user_blueprint.route('/del_grade/',methods=['GET'])
def del_grade():
    if request.method == 'GET':
        g_id = request.args.get('id')
        grade = Grade.query.filter_by(g_id=g_id).first()
        db.session.delete(grade)
        db.session.commit()
        grades = Grade.query.all()
        return render_template('grade.html',grades=grades)

# 删除学生
@user_blueprint.route('/del_stu/<int:id>/')
def del_stu(id):
    stu = Student.query.get(id)
    db.session.delete(stu)
    db.session.commit()
    stus = Student.query.all()
    return render_template('student.html',stus=stus)

# 展示角色
@user_blueprint.route('/roles/')
def roles():
    roles = Role.query.all()
    return render_template('roles.html',roles=roles)

# 添加角色
@user_blueprint.route('/add_roles/',methods=['GET','POST'])
def add_roles():
    if request.method == 'GET':
        msg = '请填写角色名称'
        return render_template('addroles.html',msg=msg)
    if request.method == 'POST':
        role = Role()
        r_name = request.form.get('role_name')
        role.r_name = r_name
        role.save()
        roles = Role.query.all()
        return render_template('roles.html',roles=roles)

# 权限列表
@user_blueprint.route('/permissions/')
def permissions():
    pers = Permission.query.all()
    return render_template('permissions.html',pers=pers)

# 添加权限
@user_blueprint.route('/add_permission/',methods=['POST','GET'])
def add_permission():
    if request.method == 'GET':
        msg = '请输入权限名称'
        return render_template('addpermission.html',msg=msg)
    if request.method == 'POST':
        per = Permission()
        per_name = request.form.get('per_name')
        per.p_name = per_name
        db.session.add(per)
        db.session.commit()
        return redirect(url_for('user.permissions'))

# 用户列表
@user_blueprint.route('/user_list/')
def user_list():
    users = User.query.all()
    return render_template('users.html', users=users)

#添加用户
@user_blueprint.route('/add_edit/',methods=['GET','POST'])
def add_edit():
    if request.method == 'GET':
        roles = Role.query.all()
        return render_template('add_edit.html',roles=roles)
    if request.method == 'POST':
        username = request.form.get('username')
        pwd1 = request.form.get('password1')
        pwd2 = request.form.get('password2')
        r_id = request.form.get('r_id')
        if not all([username,pwd1,pwd2,r_id]):
            msg = '请输入完整参数'
            return render_template('add_edit.html',msg=msg)
        if pwd1 != pwd2:
            msg = '两次密码输入不一致'
            return render_template('add_edit.html',msg=msg)
        user = User()
        role = Role.query.get(r_id)
        user.u_name = username
        user.password = pwd1
        user.role = role
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.user_list'))

# 修改密码
@user_blueprint.route('/changepwd/')
def changepwd():
    return render_template('changepwd.html')

# 增加角色权限
@user_blueprint.route('/add_role_per/<int:id>/',methods=['GET','POST'])
def add_role_per(id):
    if request.method == 'GET':
        role = Role.query.get(id)
        pers = Permission.query.all()
        return render_template('add_role_per.html',role=role,pers=pers)
    if request.method == 'POST':
        role = Role.query.get(id)
        p_id = request.form.get('per_id')
        per = Permission.query.get(p_id)
        role.permission.append(per)
        db.session.add(role)
        db.session.commit()
        return redirect(url_for('user.roles'))

# 删除角色权限
@user_blueprint.route('/del_role_per/<int:id>/',methods=['GET','POST'])
def del_role_per(id):
    if request.method == 'GET':
        role = Role.query.get(id)
        return render_template('del_role_per.html',role=role)
    if request.method == 'POST':
        role = Role.query.get(id)
        p_id = request.form.get('per_id')
        per = Permission.query.get(p_id)
        role.permission.remove(per)
        db.session.commit()
        return redirect(url_for('user.roles'))

# 删除角色
@user_blueprint.route('/del_role/<int:id>/')
def del_role(id):
    role = Role.query.get(id)
    db.session.delete(role)
    db.session.commit()
    roles = Role.query.all()
    return render_template('roles.html', roles=roles)

# 修改权限名
@user_blueprint.route('/change_per/',methods=['GET','POST'])
def change_per():
    if request.method == 'GET':
        msg = '请输入要修改的权限名'
        id = request.args.get('id')
        return render_template('addpermission.html',msg=msg,id=id)
    if request.method == 'POST':
        id = request.form.get('per_id')
        p_name = request.form.get('per_name')
        per = Permission.query.get(id)
        per.p_name = p_name
        db.session.add(per)
        db.session.commit()
        return redirect(url_for('user.permissions'))

# 删除权限
@user_blueprint.route('/del_per/<int:id>/')
def del_per(id):
    per = Permission.query.filter_by(p_id=id).first()
    db.session.delete(per)
    db.session.commit()
    return redirect(url_for('user.permissions'))

# 删除用户
@user_blueprint.route('/del_user/')
def del_user():
    id = request.args.get('id')
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user.user_list'))

# 修改用户角色
@user_blueprint.route('/change_user_role/',methods=['GET','POST'])
def change_user_role():
    if request.method == 'GET':
        id = request.args.get('id')
        user = User.query.get(id)
        roles = Role.query.all()
        return render_template('change_user_role.html',user=user,roles=roles)
    if request.method == 'POST':
        r_id = request.form.get('r_id')
        role = Role.query.get(r_id)
        u_id = request.args.get('id')
        user = User.query.get(u_id)
        user.role = role
        db.session.commit()
        return redirect(url_for('user.user_list'))


# 登录
@user_blueprint.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(u_name=username,password=password).first()
        if user:
            session['username'] = username
            return render_template('index.html')
        else:
            msg = '用户不存在'
            return render_template('login.html',msg=msg)

# 注销
@user_blueprint.route('/logout/',methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('user.login'))