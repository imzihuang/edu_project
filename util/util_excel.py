#coding:utf-8

import StringIO
import xlwt as ExcelWrite
import xlrd as ExcelRead

def make_student_header(sheet, student_relative_list):
    row = 0
    for student_dict in student_relative_list:
        col = 0
        for k in student_dict:
            if k!="relative_list":
                if k not in excel_header:
                    continue
                sheet.write(row, col, excel_header.get(k, k))
                col += 1
        relative_list = student_dict.get("relative_list", [])
        for relative_info in relative_list:
            for k in relative_info:
                if k not in excel_header:
                    continue
                sheet.write(row, col, excel_header.get(k, k))
                col += 1


def make_student_excel(student_relative_list):
    if not student_relative_list:
        return ''
    xls = ExcelWrite.Workbook(style_compression=2)
    sheet = xls.add_sheet("student_relative", cell_overwrite_ok=True)

    make_student_header(sheet, student_relative_list)
    row = 1
    #填充每行的数据
    for student_dict in student_relative_list:
        col = 0
        for k, v in student_dict.items():
            if k != "relative_list":
                if k not in excel_header:
                    continue
                sheet.write(row, col, v)
                col += 1
        relative_list = student_dict.get("relative_list", [])
        for relative_info in relative_list:
            row += 1
            for k, v in relative_info.items():
                if k not in excel_header:
                    continue
                sheet.write(row, col, excel_header.get(k, k))
                col += 1

        row += 1

    sf = StringIO.StringIO()
    xls.save(sf)
    contents = sf.getvalue()
    sf.close()
    return contents

def make_teacher_excel(data_array):
    """
    :param data_array:
    :return:
    """
    if not data_array:
        return ''
    xls = ExcelWrite.Workbook(style_compression=2)
    sheet = xls.add_sheet("teacher")
    flag_header = False
    row = 1
    #填充每行的数据
    for data in data_array:
        col = 0
        if not flag_header:
            flag_header = True
            for k in data:
                sheet.write(0, col, k)
                col += 1
        col = 0
        for k, v in data.items():
            sheet.write(row, col, v)
            col += 1
        row += 1
    sf = StringIO.StringIO()
    xls.save(sf)
    contents = sf.getvalue()
    sf.close()
    return contents

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


excel_header={
    "id": "编号".decode('utf-8'),
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


# merge_format = workbook.add_format({
#     'bold':     True,
#     'border':   6,
#     'align':    'center',#水平居中
#     'valign':   'vcenter',#垂直居中
#     'fg_color': '#D7E4BC',#颜色填充
# })