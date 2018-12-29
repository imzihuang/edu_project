let app = getApp()
let that
let urlTitle = app.globalData.urlTitle
let session_code_value = wx.getStorageSync('session_code')
let now = new Date();
let year = now.getFullYear();
let month = now.getMonth() + 1;
let datenum = now.getDate();
Page({
  data: {
    nav_list: [],
    sign_list: [],
    signLength: 0,
    imgUrlTitle: '',
    open: false,
    background: ['swiper1', 'swiper2', 'swiper3'],
    indicatorDots: true,
    vertical: false,
    autoplay: true,
    circular: true,
    interval: 100000,
    duration: 500,
    previousMargin: 0,
    nextMargin: 0,
    year: 0,
    month: 0,
    datenum: 0,
    date: ['日', '一', '二', '三', '四', '五', '六'],
    dateArr: [],
    isToday: 0,
    isTodayWeek: false,
    todayIndex: 0,
    isScroll: false,
    isScrollUp: true,
    scrollHeight: 0,
    scrollTop: 0

  },
  onLoad: function(options) {
    that = this

  },
  onShow: function() {
    this.studentInfo()
    this.setData({
      imgUrlTitle: urlTitle,
    })
    wx.createSelectorQuery().select('.page').boundingClientRect((rect) => {
      this.setData({
        scrollHeight: rect.height
      })
    }).exec()

    wx.getSystemInfo({
      success: function (res) {
        console.log(res.model)
        console.log(res.pixelRatio)
        console.log(res.windowWidth)
        console.log(res.windowHeight)
        console.log(res.language)
        console.log(res.version)
      }
    })
    var query = wx.createSelectorQuery();
    //选择id
    var that = this;
    query.select('.page').boundingClientRect(function (rect) {
      console.log(rect.height)
    }).exec();
  },
  //滚动事件监听

  // onPageScroll: function (e) {
  //   console.log(e.scrollTop)
  //   if (e.scrollTop > this.data.scrollTop || e.scrollTop >= this.data.scrollHeight) {
  //     if (e.scrollTop - this.data.scrollTop > 30 || e.scrollTop > 30) {
  //       //向下滚动 
  //       this.setData({
  //         isScroll: true,
  //         isScrollUp: false,
  //       })
  //       wx.createSelectorQuery().select('.page').boundingClientRect(function(rect) {
  //         // 使页面滚动到底部
  //         // console.log(rect.bottom)
  //         wx.pageScrollTo({
  //           scrollTop: rect.bottom
  //         })
  //       }).exec()
  //     }
  //   } else {
  //     if (this.data.scrollTop - e.scrollTop > 30 || e.scrollTop < 267) {
  //       //向上滚动 
  //       this.setData({
  //         isScroll: false,
  //         isScrollUp: true,
  //       })
  //       wx.pageScrollTo({
  //         scrollTop: 0
  //       })
  //     }
  //   }
  //   //给scrollTop重新赋值 
  //   this.setData({
  //     scrollTop: e.scrollTop
  //   })
  // },

  timeData: function() {
    let that = this
    let urlTitle = app.globalData.urlTitle
    wx.request({
      url: urlTitle + '/relative_sign/infos',
      data: {
        start_time: that.data.year + '-' + that.data.month + '-' + that.data.datenum + ' 00:00:00',
        end_time: that.data.year + '-' + that.data.month + '-' + that.data.datenum + ' 23:59:59',
        relative_id: app.globalData.relativeId,
        edu_session: session_code_value
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      method: "GET",
      success(res) {
        console.log(res.data.data);
        if (res.data.data.length > 0) {
          let signList = new Array();
          let typeCount = false;
          let typeCount1 = 0;
          let typeCount2 = 0;
          for (let i = 0; i < res.data.data.length; i++) {
            if (res.data.data[i].type == 1) {
              typeCount1++;
            }
            if (res.data.data[i].type == 2) {
              typeCount = true;
              typeCount2++;
            }
          }
          if (typeCount == true && typeCount2 < 2 && typeCount1 != 0) {
            let lastCount = res.data.data.length - 1
            signList = [{}, {}]
            signList[0].time = res.data.data[0].create_time.substring(0, 10)
            signList[0].timeDetail = res.data.data[0].create_time.substring(11)
            signList[0].img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[0].img_path
            signList[0].relative_img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[0].relative_img_path
            signList[0].type = res.data.data[0].type
            signList[0].alias = res.data.data[0].alias
            signList[1].time = res.data.data[lastCount].create_time.substring(0, 10)
            signList[1].timeDetail = res.data.data[lastCount].create_time.substring(11)
            signList[1].img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[lastCount].img_path
            signList[1].relative_img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[lastCount].relative_img_path
            signList[1].type = res.data.data[lastCount].type
            signList[1].alias = res.data.data[lastCount].alias
          } else {
            let lastCount = res.data.data.length - 1
            signList = [{}]
            signList[0].time = res.data.data[lastCount].create_time.substring(0, 10)
            signList[0].timeDetail = res.data.data[lastCount].create_time.substring(11)
            signList[0].img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[lastCount].img_path
            signList[0].relative_img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[lastCount].relative_img_path
            signList[0].type = res.data.data[lastCount].type
            signList[0].type = res.data.data[lastCount].alias
          }

          for (let i = 0; i < signList.length; i++) {
            if (signList[i].type == 1) {
              signList[i].type = '签到'
            } else {
              signList[i].type = '签退'
            }
            if (signList[i].alias == '') {
              signList[i].alias = app.globalData.relativeName
            }
          }

          that.setData({
            sign_list: signList,
            signLength: res.data.data.length
          })
        } else {
          that.setData({
            sign_list: [],
            signLength: 0
          })
        }

      }
    })
  },
  //获取学生信息
  studentInfo: function() {
      let that = this
      let phoneNum_value = wx.getStorageSync('phoneNum')
      let session_code_value = wx.getStorageSync('session_code')
      wx.request({
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        url: app.globalData.urlTitle + '/relation/infos',
        data: {
          phone: phoneNum_value,
          edu_session: session_code_value
        },
        method: 'GET',
        success: function(res) {
          console.log(res)
          let student = new Array()
          let Storage_student_checked_id = ''
          if (wx.getStorageSync('student')){
            let Storage_student = wx.getStorageSync('student')
            for (let j = 0; j < Storage_student.length; j++){
              if (Storage_student[j].checked == true){
                 Storage_student_checked_id = Storage_student[j].id
              }
            }
          } 
          if (Storage_student_checked_id != '') {
            console.log(Storage_student_checked_id)
            for (let i = 0; i < res.data.data.length; i++) {
              student[i] = new Object()
              student[i].name = res.data.data[i].student_info.name
              student[i].id = res.data.data[i].student_info.id
              student[i].class_name = res.data.data[i].student_info.class_info.name
              student[i].grade_name = res.data.data[i].student_info.grade_info.name
              student[i].birthday = res.data.data[i].student_info.birthday
              student[i].sex = res.data.data[i].student_info.sex
              if (res.data.data[i].student_info.id == Storage_student_checked_id) {
                student[i].checked = true
                wx.setStorageSync('studentId', student[i].id);
                app.globalData.studentId = student[i].id;
                wx.setStorageSync('studentName', student[i].name);
                wx.setStorageSync('studentClass', student[i].class_name);
                wx.setStorageSync('studentGrade', student[i].grade_name);
                wx.setStorageSync('studentBirthday', student[i].birthday);
                wx.setStorageSync('studentSex', student[i].sex);
              } else {
                student[i].checked = false
              }
            }
          }else{
            for (let i = 0; i < res.data.data.length; i++) {
              student[i] = new Object()
              student[i].name = res.data.data[i].student_info.name
              student[i].id = res.data.data[i].student_info.id
              student[i].class_name = res.data.data[i].student_info.class_info.name
              student[i].grade_name = res.data.data[i].student_info.grade_info.name
              student[i].birthday = res.data.data[i].student_info.birthday
              student[i].sex = res.data.data[i].student_info.sex
              if (i == 0) {
                student[i].checked = true
              } else {
                student[i].checked = false
              }
            }
            wx.setStorageSync('studentId', student[0].id);
            app.globalData.studentId = student[0].id;
            wx.setStorageSync('studentName', student[0].name);
            wx.setStorageSync('studentClass', student[0].class_name);
            wx.setStorageSync('studentGrade', student[0].grade_name);
            wx.setStorageSync('studentBirthday', student[0].birthday);
            wx.setStorageSync('studentSex', student[0].sex);
          }

          that.setData({
            nav_list: student,
          })
          wx.setStorageSync('student', student);
          that.relativeId()
        },
        fail: function(res) {

        },
      })
  },
  //获取家长id\名称
  relativeId: function() {
    let that = this
    let urlTitle = app.globalData.urlTitle
    let relativePhone = wx.getStorageSync('phoneNum')
    let session_code_value = wx.getStorageSync('session_code')
    wx.request({
      url: urlTitle + '/relative/infos',
      data: {
        phone: relativePhone,
        edu_session: session_code_value
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      method: "GET",
      success(res) {
        console.log(res.data);
        app.globalData.relativeId = res.data.data[0].id;
        app.globalData.relativeName = res.data.data[0].name;
        that.timeData()
      }
    })
  },
  //切换学生
  changeStudent: function(e) {
    console.log(e);
    let changeStudent = e._relatedInfo.anchorTargetText;
    let session_code_value = wx.getStorageSync('session_code')
    let nav_listChange = this.data.nav_list;
    for (let j = 0; j < nav_listChange.length; j++) {
      if (nav_listChange[j].name == changeStudent) {
        nav_listChange[j].checked = true;
        app.globalData.studentId = nav_listChange[j].id;
        wx.setStorageSync('studentId', nav_listChange[j].id);
        wx.setStorageSync('studentName', nav_listChange[j].name);
        wx.setStorageSync('studentClass', nav_listChange[j].class_name);
        wx.setStorageSync('studentGrade', nav_listChange[j].grade_name);
        wx.setStorageSync('studentBirthday', nav_listChange[j].birthday);
        wx.setStorageSync('studentSex', nav_listChange[j].sex);

        //获取新的关系id
        wx.request({
          url: urlTitle + '/relation/infos',
          data: {
            student_id: nav_listChange[j].id,
            edu_session: session_code_value
          },
          header: {
            'content-type': 'application/x-www-form-urlencoded'
          },
          method: "GET",
          success(res) {
            console.log(res.data.data[0].relative_id);
            app.globalData.relativeId = res.data.data[0].relative_id;
          }
        })
        //获取新的关系id--end
      } else {
        nav_listChange[j].checked = false;
      }
    }

    this.setData({
      nav_list: nav_listChange
    });
    wx.setStorageSync('student', nav_listChange);
  },
  //列表的操作函数
  open_list: function(opts) {
    this.setData({
      open: false
    });
  },
  //左侧导航开关
  off_canvas: function() {
    this.data.open ? this.setData({
      open: false
    }) : this.setData({
      open: true
    });
  },
  //轮播
  changeProperty: function(e) {
    var propertyName = e.currentTarget.dataset.propertyName
    var newData = {}
    newData[propertyName] = e.detail.value
    this.setData(newData)
  },
  //页面跳转
  goAddface: function() {
    wx.navigateTo({
      url: '../addface/addface',
    })
  },
  goAttendance: function() {
    wx.navigateTo({
      url: '../attendance/attendance',
    })
  },
  //日历begin
  onLoad: function() {
    this.dateInit(year, month - 1);
    this.setData({
      year: year,
      month: month,
      datenum: datenum,
      isToday: '' + year + month + now.getDate()
    })
  },
  //点击日历
  lookHuoDong: function(e) {
    this.goAttendance()
  },

  dateInit: function(setYear, setMonth) {
    //全部时间的月份都是按0~11基准，显示月份才+1
    let dateArr = []; //需要遍历的日历数组数据
    let arrLen = 0; //dateArr的数组长度
    let now = setYear ? new Date(setYear, setMonth) : new Date();
    let year = setYear || now.getFullYear();
    let nextYear = 0;
    let month = setMonth || now.getMonth(); //没有+1方便后面计算当月总天数
    let nextMonth = (month + 1) > 11 ? 1 : (month + 1);
    let startWeek = new Date(year + '/' + (month + 1) + '/' + 1).getDay(); //目标月1号对应的星期
    console.log(new Date(year + '/' + (month + 1) + '/' + 1));
    let dayNums = new Date(year, nextMonth, 0).getDate(); //获取目标月有多少天
    let obj = {};
    let num = 0;
    if (month + 1 > 11) {
      nextYear = year + 1;
      dayNums = new Date(nextYear, nextMonth, 0).getDate();
    }
    arrLen = startWeek + dayNums;
    for (let i = 0; i < arrLen; i++) {
      if (i >= startWeek) {
        num = i - startWeek + 1;
        if (setYear <= new Date().getFullYear() && setMonth <= new Date().getMonth() + 1) {
          obj = {
            isToday: '' + year + (month + 1) + num,
            dateNum: num,
            weight: 5,
            disabled: true
          }
          if (setYear == new Date().getFullYear() && setMonth == new Date().getMonth() && num > new Date().getDate()) {
            obj = {
              isToday: '' + year + (month + 1) + num,
              dateNum: num,
              weight: 5,
              disabled: false
            }
          }
        } else {
          obj = {
            isToday: '' + year + (month + 1) + num,
            dateNum: num,
            weight: 5,
            disabled: false
          }
        }
      } else {
        obj = {};
      }
      dateArr[i] = obj;
    }
    this.setData({
      dateArr: dateArr
    })
    console.log(dateArr);
    let nowDate = new Date();
    let nowYear = nowDate.getFullYear();
    let nowMonth = nowDate.getMonth() + 1;
    let nowWeek = nowDate.getDay();
    let getYear = setYear || nowYear;
    let getMonth = setMonth >= 0 ? (setMonth + 1) : nowMonth;
    if (nowYear == getYear && nowMonth == getMonth) {
      this.setData({
        isTodayWeek: true,
        todayIndex: nowWeek
      })
    } else {
      this.setData({
        isTodayWeek: false,
        todayIndex: -1
      })
    }
  },
  /* 上月切换 */
  lastMonth: function() {
    //全部时间的月份都是按0~11基准，显示月份才+1
    let year = this.data.month - 2 < 0 ? this.data.year - 1 : this.data.year;
    let month = this.data.month - 2 < 0 ? 11 : this.data.month - 2;
    this.setData({
      year: year,
      month: (month + 1)
    })
    this.dateInit(year, month);
  },
  /* 下月切换*/
  nextMonth: function() {
    //全部时间的月份都是按0~11基准，显示月份才+1
    let year = this.data.month > 11 ? this.data.year + 1 : this.data.year;
    let month = this.data.month > 11 ? 0 : this.data.month;
    this.setData({
      year: year,
      month: (month + 1)
    })
    this.dateInit(year, month);
  },
  // 日历end
  //图片错误
  binderrorImgPath: function(e) {
    let that = this
    var errorImgIndex = e.target.dataset.bindex
    let newSignList = that.data.sign_list
    newSignList[errorImgIndex].img_path = "../images/calendar.png"
    that.setData({
      sign_list: newSignList
    })
  },
  binderrorRelativeImgPath: function(e) {
    let that = this
    var errorImgIndex = e.target.dataset.bindex
    let newSignList = that.data.sign_list
    newSignList[errorImgIndex].img_path = "../images/calendar.png"
    that.setData({
      sign_list: newSignList
    })
  }
})