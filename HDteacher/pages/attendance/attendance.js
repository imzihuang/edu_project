let app = getApp()
let that
let urlTitle = app.globalData.urlTitle
var session_code_value = wx.getStorageSync('session_code')
Page({
  data: {
    nav_list: [{
      name: '',
      checked: true,
      id: ''
    }, ],
    sign_list: [],
    signLength: 0,
    imgUrlTitle: '',
    year: 0,
    month: 0,
    datenum: 0,
    date: ['日', '一', '二', '三', '四', '五', '六'],
    dateArr: [],
    isToday: 0,
    isTodayWeek: false,
    todayIndex: 0
  },
  onLoad: function() {
    let now = new Date();
    let year = now.getFullYear();
    let month = now.getMonth() + 1;
    let datenum = now.getDate();
    this.dateInit(year, month-1);
    this.setData({
      year: year,
      month: month,
      datenum: datenum,
      isToday: '' + year + month + now.getDate()
    })
  },
  onShow: function() {
    this.setData({
      imgUrlTitle: urlTitle,
    })
    this.timeData()
  },
  //数据请求
  timeData: function() {console.log(2222)
    let that = this
    let urlTitle = app.globalData.urlTitle
    wx.request({
      url: urlTitle + '/teacher_sign/infos',
      data: {
        start_time: that.data.year + '-' + that.data.month + '-' + that.data.datenum + ' 00:00:00',
        end_time: that.data.year + '-' + that.data.month + '-' + that.data.datenum + ' 23:59:59',
        teacher_id: app.globalData.teacherId,
        edu_session: session_code_value
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      method: "GET",
      success(res) {
        console.log(res);
        if (res.data.state == 0) {
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
              signList[0].teacher_img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[0].teacher_img_path
              signList[0].type = res.data.data[0].type
              signList[0].alias = res.data.data[0].alias
              signList[1].time = res.data.data[lastCount].create_time.substring(0, 10)
              signList[1].timeDetail = res.data.data[lastCount].create_time.substring(11)
              signList[1].img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[lastCount].img_path
              signList[1].teacher_img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[lastCount].teacher_img_path
              signList[1].type = res.data.data[lastCount].type
              signList[1].alias = res.data.data[lastCount].alias
            } else {
              let lastCount = res.data.data.length - 1
              signList = [{}]
              signList[0].time = res.data.data[lastCount].create_time.substring(0, 10)
              signList[0].timeDetail = res.data.data[lastCount].create_time.substring(11)
              signList[0].img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[lastCount].img_path
              signList[0].teacher_img_path = that.data.imgUrlTitle + '/edu/' + res.data.data[lastCount].teacher_img_path
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
      }
    })
  },
  //点击日历
  lookHuoDong: function(e) {
    let year = e.currentTarget.dataset.year;
    let month = e.currentTarget.dataset.month;
    let datenum = e.currentTarget.dataset.datenum;
    if (year <= new Date().getFullYear()){
      if (month < new Date().getMonth()+1){
        this.setData({
          year: year,
          month: month,
          datenum: datenum,
          isToday: '' + year + month + datenum
        })
        this.timeData()
      } else if (month == new Date().getMonth() + 1){
        if (datenum <= new Date().getDate()) {
          this.setData({
            year: year,
            month: month,
            datenum: datenum,
            isToday: '' + year + month + datenum
          })
          this.timeData()
        }
      }
    }
  },
  dateInit: function (setYear, setMonth) {
    //全部时间的月份都是按0~11基准，显示月份才+1
    let dateArr = []; //需要遍历的日历数组数据
    let arrLen = 0; //dateArr的数组长度
    let now = setYear ? new Date(setYear, setMonth) : new Date();
    let year = setYear || now.getFullYear();
    let nextYear = 0;
    let month = setMonth || now.getMonth(); //没有+1方便后面计算当月总天数
    let nextMonth = (month + 1) > 11 ? 1 : (month + 1); 
    let startWeek = new Date(year + '/' + (month + 1) + '/' + 1).getDay(); //目标月1号对应的星期
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
  /**
   * 上月切换
   */
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
  /**
   * 下月切换
   */
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