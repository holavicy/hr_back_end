import pandas as pd
import cx_Oracle
from datetime import datetime


class UserModel(object):
    ncDbInfo = {
        "user": "nc633_rebulid",
        "password": "nc633_123",
        "db": "wtdb",
        "host": "192.168.40.230",
        "port": "1521",
    }
    db_nc = cx_Oracle.connect(
        f'{ncDbInfo["user"]}/{ncDbInfo["password"]}@{ncDbInfo["host"]}:{ncDbInfo["port"]}/{ncDbInfo["db"]}',
        encoding="UTF-8", nencoding="UTF-8")

    # 获取NC中bd_psndoc员工基本信息
    @classmethod
    def get_user_info(cls, code):
        try:
            sql = "select ss.code, ss.name, ss.birthdate,c.hiredate, jr.jobrankcode\
    from bd_psndoc ss\
    inner join hi_psnjob job on ss.pk_psndoc = job.pk_psndoc\
    inner join om_jobrank jr on jr.pk_jobrank = job.pk_jobrank\
    left join (\
      select a.clerkcode, min(a.begindate) as hiredate \
      from hi_psnjob a \
      left join bd_psncl b on a.pk_psncl = b.pk_psncl \
      where b.name = '全职' group by a.clerkcode) c on c.clerkcode = ss.code \
    where job.endflag = 'N'\
    and job.ismainjob = 'Y'\
    and job.lastflag = 'Y'\
    and ss.code = '%s'" % (code)
            df_records = pd.read_sql(sql, con=cls.db_nc)
            df_records = df_records.to_json(orient='records')
            return df_records
        except Exception as e:
            print(e)

    # 获取花名册
    @classmethod
    def hua_ming_ce(cls, page, page_size, staff_no, name, group_value):
        try:
            # 获取当前时间
            now = datetime.now()

            # 获取当前年份
            year = now.year

            name_sql = ''
            staff_no_sql = ''
            group_value_sql = ''

            if name:
                name_sql =  f'and ss.name like \'%{name}%\''

            if staff_no:
                staff_no_sql = f'and ss.code = \'{staff_no}\''

            if group_value:
                group_value_sql = f'and ss.pk_org = \'{group_value}\''

            sql = '''select ss.code,ss.name, org.name as ORGNAME,op.postname, br.name as jiguan, bd.name as minzu,
CASE ss.sex  WHEN 1 THEN '男'  WHEN 2 THEN '女'  ELSE '其他' END as sex ,
bd2.name as hukouxingzhi , br2.name as hukousuozaidi, bd3.name as zhengzhimianmao , bd4.name as hunyinzhuangkuang ,
ss.mobile,bp.name as zhengjianleixing, ss.id as zhengjianhao , hpc.enddate as youxiaoqi, ss.censusaddr, ss.glbdef1,
ss.birthdate,%d - (REGEXP_SUBSTR(ss.birthdate,'(\d){4}')) + 1 as age,d.joindate,hp.begindate as muxianbegindate,
c.zcdengji,c.zcname,c.CREATIONTIME,bd5.name as xueli,hpe.school,hpe.major,hpe.begindate,hpe.enddate,oj.jobname as zwmc, ojr.jobrankname as zwjb,
ojl.name as zhiji,ops.postseriesname,jt.name as jobTypeName,hpct.ifprop, hpct.probegindate , hpct.probenddate,b.zzdate,
hpl.linkman as linkman, hpl.mobile as linkmanMobile,job.pk_dept,
trunc(months_between(to_date(sysdate),to_date(d.joindate, 'yyyy-mm-dd'))/12) as jtAge,
trunc(months_between(to_date(sysdate),to_date(hp.begindate, 'yyyy-mm-dd'))/12) as mxAge
from bd_psndoc ss
inner join hi_psnjob job on ss.pk_psndoc = job.pk_psndoc
inner join bd_psncl jt on jt.pk_psncl = job.pk_psncl
left join om_job oj on job.pk_job = oj.pk_job
left join om_jobrank ojr on ojr.pk_jobrank = job.pk_jobrank
left join om_joblevel ojl on ojl.pk_joblevel = job.pk_jobgrade
left join om_post op on op.pk_post = job.pk_post
left join om_postseries ops on ops.pk_postseries = job.pk_postseries
left join org_dept dp on dp.pk_dept = job.pk_dept
left join org_orgs org on dp.pk_org = org.pk_org
left join bd_region br on ss.nativeplace = br.pk_region
left join bd_region br2 on ss.permanreside  = br2.pk_region
left join bd_defdoc bd on ss.nationality = bd.pk_defdoc
left join bd_defdoc bd2 on ss.characterrpr  = bd2.pk_defdoc
left join bd_defdoc bd3 on ss.polity  = bd3.pk_defdoc
left join bd_defdoc bd4 on ss.marital = bd4.pk_defdoc
left join bd_psnidtype bp on ss.idtype = bp.pk_identitype
left join hi_psndoc_cert hpc on hpc.pk_psndoc = ss.pk_psndoc
left join hi_psnorg hp on hp.pk_psndoc = ss.pk_psndoc and hp.endflag = 'N' and hp.lastflag = 'Y'
left join (
     select job.pk_psndoc, min(job.begindate) as zzdate
     from hi_psnjob job
     join bd_psncl jt on job.pk_psncl = jt.pk_psncl
     where jt.name in ('正式员工','全职','车间在职', '退休返聘')
     group by job.pk_psndoc) b on ss.pk_psndoc = b.pk_psndoc
left join (
      select ss.pk_psndoc,bd.name as zcname, bd2.name as zcdengji,hpt.begindate as CREATIONTIME
      from bd_psndoc ss
      inner join hi_psndoc_title hpt on ss.pk_psndoc = hpt.pk_psndoc
      inner join bd_defdoc bd on hpt.pk_techposttitle  = bd.pk_defdoc
      inner join bd_defdoc bd2 on hpt.titlerank = bd2.pk_defdoc
      where hpt.lastflag = 'Y'
) c on ss.pk_psndoc = c.pk_psndoc

left join (
     select job.pk_psndoc, min(job.begindate) as joindate
     from hi_psnjob job
     join bd_psncl jt on job.pk_psncl = jt.pk_psncl
     where jt.name in ('正式员工','全职','车间在职', '退休返聘', '试用期员工')
     group by job.pk_psndoc) d on ss.pk_psndoc = d.pk_psndoc

left join bd_defdoc bd5 on ss.edu = bd5.pk_defdoc
left join hi_psndoc_edu hpe on ss.pk_psndoc = hpe.pk_psndoc and hpe.lasteducation = 'Y'
left join hi_psndoc_ctrt hpct on ss.pk_psndoc = hpct.pk_psndoc and hpct.lastflag = 'Y'
left join hi_psndoc_linkman hpl on ss.pk_psndoc = hpl.pk_psndoc
where job.endflag = 'N'
and job.ismainjob = 'Y'
and job.lastflag = 'Y'
and ss.name not like '%%测试%%'
and jt.name in ('正式员工','全职','车间在职', '试用期员工', '退休返聘') 
and ss.code not like '%%L%%' 
%s %s %s
order by d.joindate desc'''%(year, name_sql, staff_no_sql,group_value_sql)

            num_sql = '''select count(ss.code) as TOTALNUM
from bd_psndoc ss
inner join hi_psnjob job on ss.pk_psndoc = job.pk_psndoc
inner join bd_psncl jt on jt.pk_psncl = job.pk_psncl
left join om_job oj on job.pk_job = oj.pk_job
left join om_jobrank ojr on ojr.pk_jobrank = job.pk_jobrank
left join om_joblevel ojl on ojl.pk_joblevel = job.pk_jobgrade
left join om_post op on op.pk_post = job.pk_post
left join om_postseries ops on ops.pk_postseries = job.pk_postseries
left join org_dept dp on dp.pk_dept = job.pk_dept
left join org_orgs org on dp.pk_org = org.pk_org
left join bd_region br on ss.nativeplace = br.pk_region 
left join bd_region br2 on ss.permanreside  = br2.pk_region 
left join bd_defdoc bd on ss.nationality = bd.pk_defdoc 
left join bd_defdoc bd2 on ss.characterrpr  = bd2.pk_defdoc 
left join bd_defdoc bd3 on ss.polity  = bd3.pk_defdoc  
left join bd_defdoc bd4 on ss.marital = bd4.pk_defdoc
left join bd_psnidtype bp on ss.idtype = bp.pk_identitype 
left join hi_psndoc_cert hpc on hpc.pk_psndoc = ss.pk_psndoc
left join hi_psnorg hp on hp.pk_psndoc = ss.pk_psndoc and hp.endflag = 'N' and hp.lastflag = 'Y'
left join (             
     select job.pk_psndoc, min(job.begindate) as zzdate 
     from hi_psnjob job 
     join bd_psncl jt on job.pk_psncl = jt.pk_psncl 
     where jt.name in ('正式员工','全职','车间在职', '退休返聘') 
     group by job.pk_psndoc) b on ss.pk_psndoc = b.pk_psndoc  
left join (
      select ss.pk_psndoc,bd.name as zcname, bd2.name as zcdengji,hpt.begindate as CREATIONTIME
      from bd_psndoc ss
      inner join hi_psndoc_title hpt on ss.pk_psndoc = hpt.pk_psndoc
      inner join bd_defdoc bd on hpt.pk_techposttitle  = bd.pk_defdoc
      inner join bd_defdoc bd2 on hpt.titlerank = bd2.pk_defdoc
      where hpt.lastflag = 'Y'
) c on ss.pk_psndoc = c.pk_psndoc

left join (             
     select job.pk_psndoc, min(job.begindate) as joindate 
     from hi_psnjob job 
     join bd_psncl jt on job.pk_psncl = jt.pk_psncl 
     where jt.name in ('正式员工','全职','车间在职', '退休返聘', '试用期员工') 
     group by job.pk_psndoc) d on ss.pk_psndoc = d.pk_psndoc

left join bd_defdoc bd5 on ss.edu = bd5.pk_defdoc
left join hi_psndoc_edu hpe on ss.pk_psndoc = hpe.pk_psndoc and hpe.lasteducation = 'Y'
left join hi_psndoc_ctrt hpct on ss.pk_psndoc = hpct.pk_psndoc and hpct.lastflag = 'Y'
left join hi_psndoc_linkman hpl on ss.pk_psndoc = hpl.pk_psndoc 
where job.endflag = 'N'
and job.ismainjob = 'Y'
and job.lastflag = 'Y'
and ss.name not like '%%测试%%'
and jt.name in ('正式员工','全职','车间在职', '试用期员工', '退休返聘') 
and ss.code not like '%%L%%' 
%s %s %s
order by d.joindate desc''' % (name_sql, staff_no_sql,group_value_sql)

            df_num = pd.read_sql(num_sql, con=cls.db_nc)
            total_num = df_num['TOTALNUM'][0]

            if page and page_size:
                min_top = (int(page) - 1) * int(page_size)+1
                max_top = int(page) * int(page_size)

                sql = '''SELECT *
                            FROM (SELECT tt.*, ROWNUM AS rowno
                                  FROM (%s) tt
                                   WHERE ROWNUM <= %d) table_alias
                             WHERE table_alias.rowno >= %d
                            ''' % (sql, max_top, min_top)

            df_records = pd.read_sql(sql, con=cls.db_nc)
            user_list = []
            dept_dic = {}
            for index, row in df_records.iterrows():
                last_dept = row[40]

                if last_dept in dept_dic:
                    dept_list = dept_dic[last_dept]
                    row['dept_list'] = dept_list
                else:
                    dept_list = cls.get_dept_list(last_dept, [])
                    dept_dic[last_dept] = dept_list
                    row['dept_list'] = dept_list
                user_list.append(row)
            df = pd.DataFrame(user_list)
            df = df.to_json(orient='records')

            return total_num, df
        except Exception as e:
            print(e)

    # 获取员工所在的部门列表
    @classmethod
    def get_dept_info(cls, dept_id):
        sql = "select name,pk_fatherorg from org_dept where pk_dept='%s'" % (dept_id.strip())
        df_records = pd.read_sql(sql, con=cls.db_nc)
        return df_records

    @classmethod
    def get_dept_list(cls, dept_id, dept_list):
        dept_info = cls.get_dept_info(dept_id)
        dept_name = dept_info['NAME'][0]
        dept_father_id = dept_info['PK_FATHERORG'][0]
        dept_list.insert(0, dept_name)
        if dept_father_id == '~':
            return dept_list

        return cls.get_dept_list(dept_father_id, dept_list)

    @classmethod
    def get_dept_id_list(cls, dept_id, dept_list):
        dept_info = cls.get_dept_info(dept_id)
        dept_father_id = dept_info['PK_FATHERORG'][0]
        dept_list.insert(0, dept_id)
        if dept_father_id == '~':
            return dept_list

        return cls.get_dept_list(dept_father_id, dept_list)

    @classmethod
    def get_org_list(cls):
        try:
            get_org_sql = '''select ss.name,job.pk_dept,dp.name,ss.pk_org,org.name
    from bd_psndoc ss
    inner join hi_psnjob job on ss.pk_psndoc = job.pk_psndoc
    inner join bd_psncl jt on jt.pk_psncl = job.pk_psncl
    left join org_dept dp on dp.pk_dept = job.pk_dept
    left join org_orgs org on dp.pk_org = org.pk_org
    where job.endflag = 'N'
    and job.ismainjob = 'Y'
    and job.lastflag = 'Y'
    and ss.name not like '%测试%'
    and jt.name in ('正式员工','全职','车间在职', '试用期员工', '退休返聘') 
    and ss.code not like '%L%' '''

            df_records = pd.read_sql(get_org_sql, con=cls.db_nc)
            org_dict = {}
            org_list = []
            for index, row in df_records.iterrows():
                last_dept = row[1]
                first_dept = row[3]

                if first_dept in org_dict:
                    org_dict_item = org_dict[first_dept]
                    num = org_dict_item['num']
                    org_dict_item['num'] = num + 1
                    org_dict[first_dept] = org_dict_item
                else:
                    org_dict_item = {
                        'label': row[4],
                        'value': first_dept,
                        'num': 1,
                        'fatherCode': '0'
                    }
                    org_dict[first_dept] = org_dict_item

                cls.get_dept_org(first_dept, last_dept, org_dict)
                # cls.get_dept_org('0001A31000000002DQ1F', '1001V1100000003JR0KL', org_dict)

            print(org_dict)
            for key in org_dict:
                item = org_dict[key]
                org_list.append(item)
            df = pd.DataFrame(org_list)
            df = df.to_json(orient='records')

            return df
        except Exception as e:
            print(e)

    @classmethod
    def get_dept_org(cls, first_dept, dept_id, org_dict):
        try:
            dept_info = cls.get_dept_info(dept_id)
            dept_name = dept_info['NAME'][0]
            dept_father_id = dept_info['PK_FATHERORG'][0]
            if dept_id in org_dict:
                org_dict_item = org_dict[dept_id]
                num = org_dict_item['num']
                org_dict_item['num'] = num + 1
                org_dict[dept_id] = org_dict_item
            else:
                father_code = dept_father_id
                if dept_father_id == '~':
                    father_code = first_dept
                org_dict_item = {
                    'label': dept_name,
                    'value': dept_id,
                    'num': 1,
                    'fatherCode': father_code
                }
                org_dict[dept_id] = org_dict_item
            if dept_father_id == '~':
                return org_dict

            return cls.get_dept_org(first_dept, dept_father_id, org_dict)
        except Exception as e:
            print(e)

    @classmethod
    def get_groups_list(cls):
        try:
            get_org_sql = '''select ss.name,job.pk_dept,dp.name,ss.pk_org,org.name
    from bd_psndoc ss
    inner join hi_psnjob job on ss.pk_psndoc = job.pk_psndoc
    inner join bd_psncl jt on jt.pk_psncl = job.pk_psncl
    left join org_dept dp on dp.pk_dept = job.pk_dept
    left join org_orgs org on dp.pk_org = org.pk_org
    where job.endflag = 'N'
    and job.ismainjob = 'Y'
    and job.lastflag = 'Y'
    and ss.name not like '%测试%'
    and jt.name in ('正式员工','全职','车间在职', '试用期员工', '退休返聘') 
    and ss.code not like '%L%' '''

            df_records = pd.read_sql(get_org_sql, con=cls.db_nc)
            group_dict = {}
            group_list = []
            for index, row in df_records.iterrows():
                key = row[3]

                if key in group_dict:
                    group_dict_item = group_dict[key]
                    num = group_dict_item['num']
                    group_dict_item['num'] = num + 1
                    group_dict[key] = group_dict_item
                else:
                    group_dict_item = {
                        'label': row[4],
                        'value': key,
                        'num': 1
                    }
                    group_dict[key] = group_dict_item

            print(group_dict)
            for key in group_dict:
                item = group_dict[key]
                # item['label'] = item['label'] + '(' + item['num'] + ')'
                group_list.append(item)
            print(group_list)
            df = pd.DataFrame(group_list)
            df = df.to_json(orient='records')

            return df
        except Exception as e:
            print(e)