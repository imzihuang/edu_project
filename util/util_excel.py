#coding:utf-8

import StringIO
import xlwt as ExcelWrite
import xlrd as ExcelRead

'''
设置单元格样式
'''
def set_style(name, height, bold=False):
    style = ExcelWrite.XFStyle() # 初始化样式
    font = ExcelWrite.Font() # 为样式创建字体
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

def make_student_header(sheet, student_relative_list):
    row_zero = 0
    row_one = 1
    for student_dict in student_relative_list:
        col = 0
        col_merge = 0
        for k in student_dict:
            if k!="relative_list":
                if k == "name":
                    k="student_name"
                if k not in student_excel_header:
                    continue
                sheet.write(row_one, col, student_excel_header.get(k, k))
                col += 1
        sheet.write_merge(row_zero, row_zero, 0, col-1, "学生".decode('utf-8'), set_style("Times New Roman", 220, True))
        col_merge = col
        relative_list = student_dict.get("relative_list", [])
        num = 1
        for relative_info in relative_list:
            for k in relative_info:
                if k == "name":
                    k = "relative_name"
                if k not in student_excel_header:
                    continue
                sheet.write(row_one, col, student_excel_header.get(k, k))
                col += 1
            sheet.write_merge(row_zero, row_zero, col_merge, col - 1, "联系人".decode('utf-8')+str(num))
            col_merge = col
            num += 1


def make_student_excel(student_relative_list):
    if not student_relative_list:
        return ''
    xls = ExcelWrite.Workbook(style_compression=2)
    sheet = xls.add_sheet("student_relative", cell_overwrite_ok=True)

    make_student_header(sheet, student_relative_list)
    row = 2
    #填充每行的数据
    for student_dict in student_relative_list:
        col = 0
        for k, v in student_dict.items():
            if k != "relative_list":
                if k == "name":
                    k="student_name"
                if k not in student_excel_header:
                    continue
                sheet.write(row, col, v)
                col += 1
        relative_list = student_dict.get("relative_list", [])
        for relative_info in relative_list:
            for k, v in relative_info.items():
                if k == "name":
                    k = "relative_name"
                if k not in student_excel_header:
                    continue
                sheet.write(row, col, v)
                col += 1

        row += 1

    sf = StringIO.StringIO()
    xls.save(sf)
    contents = sf.getvalue()
    sf.close()
    return contents

col_teacher_dict={}

def make_teacher_header(sheet, teacher_list):
    row = 0
    col = 0
    for teacher_dict in teacher_list:
        for k in teacher_dict:
            if k == "name":
                k="teacher_name"
            if k not in teacher_excel_header:
                continue
            if k in col_teacher_dict:
                #防止重复填写
                continue
            sheet.write(row, col, teacher_excel_header.get(k, k))
            col_teacher_dict.update({k:col})
            col += 1

def make_teacher_excel(teacher_list):
    """
    :param data_array:
    :return:
    """
    if not teacher_list:
        return ''
    xls = ExcelWrite.Workbook(style_compression=2)
    sheet = xls.add_sheet("teacher_info", cell_overwrite_ok=True)

    make_teacher_header(sheet, teacher_list)
    row = 1
    for teacher_dict in teacher_list:
        for k, v in teacher_dict.items():
            if k == "name":
                k = "teacher_name"
            if k == "status":
                v = translation.get(v, v)
            if k not in teacher_excel_header:
                continue
            col = col_teacher_dict.get(k)

            sheet.write(row, col, v)
        row += 1
    sf = StringIO.StringIO()
    xls.save(sf)
    contents = sf.getvalue()
    sf.close()
    return contents

def read_teacher_excel(school_id, file_path):
    ExcelFile = ExcelRead.open_workbook(file_path)
    sheet = ExcelFile.sheet_by_name('teacher_info')

    nrows = sheet.nrows
    #ncols = sheet.ncols

    data = []
    for i in range(1, nrows):
        row_data = sheet.row(i)
        dict_info = {
            "status": row_data[1].value.encode('utf-8'),
            "name": row_data[2].value.encode('utf-8'),
            "phone": row_data[3].value.encode('utf-8'),
            "birthday": row_data[4].value.encode('utf-8'),
            "position": int(row_data[5].value),
            "sex": int(row_data[6].value),
            "school_id": school_id
        }
        data.append(dict_info)
    return data

def read_student_excel(school_id, class_id, file_path):
    ExcelFile = ExcelRead.open_workbook(file_path)
    sheet = ExcelFile.sheet_by_name('teacher_info')

    nrows = sheet.nrows
    #ncols = sheet.ncols

    data = []
    for i in range(1, nrows):
        row_data = sheet.row(i)

        relative_list = []
        if row_data[4].value:
            relative_info = {
                "name": row_data[4].value.encode('utf-8'),
                "birthday": row_data[5].value.encode('utf-8'),
                "phone": row_data[6].value.encode('utf-8'),
                "relation": row_data[7].value.encode('utf-8'),
                "sex": int(row_data[8].value),
                "class_id": class_id
            }
            relative_list.append(relative_info)
        if row_data[9].value:
            relative_info = {
                "name": row_data[9].value.encode('utf-8'),
                "birthday": row_data[10].value.encode('utf-8'),
                "phone": row_data[11].value.encode('utf-8'),
                "relation": row_data[12].value.encode('utf-8'),
                "sex": int(row_data[13].value),
            }
            relative_list.append(relative_info)
        if row_data[14].value:
            relative_info = {
                "name": row_data[14].value.encode('utf-8'),
                "birthday": row_data[15].value.encode('utf-8'),
                "phone": row_data[16].value.encode('utf-8'),
                "relation": row_data[17].value.encode('utf-8'),
                "sex": int(row_data[18].value),
            }
            relative_list.append(relative_info)

        student_info = {
            "name": row_data[1].value.encode('utf-8'),
            "sex": int(row_data[2].value),
            "birthday": row_data[3].value.encode('utf-8'),
            "school_id": school_id,
            "relative_list": relative_list
        }

        data.append(student_info)
    return data


def demo_read_excel(file_path):
    ExcelFile = ExcelRead.open_workbook(file_path)
    # 获取目标EXCEL文件sheet名
    print(ExcelFile.sheet_names())


    # ------------------------------------
    # 若有多个sheet，则需要指定读取目标sheet例如读取sheet2
    # sheet2_name=ExcelFile.sheet_names()[1]
    # ------------------------------------
    # 获取sheet内容【1.根据sheet索引2.根据sheet名称】
    # sheet=ExcelFile.sheet_by_index(1)
    sheet = ExcelFile.sheet_by_name('TestCase002')

    # 打印sheet的名称，行数，列数
    print(sheet.name, sheet.nrows, sheet.ncols)

    # 获取整行或者整列的值
    rows = sheet.row_values(2)  # 第三行内容
    cols = sheet.col_values(1)  # 第二列内容
    print(cols, rows)
    # 获取单元格内容
    print(sheet.cell(1, 0).value.encode('utf-8'))
    print(sheet.cell_value(1, 0).encode('utf-8'))
    print(sheet.row(1)[0].value.encode('utf-8'))

    # 打印单元格内容格式
    print(sheet.cell(1, 0).ctype)


student_excel_header={
    #"id": "编号".decode('utf-8'),
    "student_name": "学生名称".decode('utf-8'),
    "relative_name": "家长名称".decode('utf-8'),
    "sex": "性别".decode('utf-8'),
    "birthday": "出生日期".decode('utf-8'),
    "school_name": "学校名称".decode('utf-8'),
    "grade_name": "年级名称".decode('utf-8'),
    "class_name": "班级名称".decode('utf-8'),
    "create_time": "创建日期".decode('utf-8'),
    "phone": "电话号码".decode('utf-8'),
    "relation": "关系".decode('utf-8')
}

teacher_excel_header={
    #"id": "编号".decode('utf-8'),
    "teacher_name": "教师名称".decode('utf-8'),
    "sex": "性别".decode('utf-8'),
    "birthday": "出生日期".decode('utf-8'),
    "school_name": "学校名称".decode('utf-8'),
    "grade_name": "年级名称".decode('utf-8'),
    "class_name": "班级名称".decode('utf-8'),
    "create_time": "创建日期".decode('utf-8'),
    "phone": "电话号码".decode('utf-8'),
    "status": "状态".decode('utf-8'),
    "position": "职位".decode('utf-8'),
}

#状态手动翻译

translation = {
    "education": "在教".decode("utf-8"),
    "holiday": "休假".decode("utf-8"),
    "dimission": "离职".decode("utf-8")
}


# merge_format = workbook.add_format({
#     'bold':     True,
#     'border':   6,
#     'align':    'center',#水平居中
#     'valign':   'vcenter',#垂直居中
#     'fg_color': '#D7E4BC',#颜色填充
# })