let app = getApp()
let that = this;

Page({
  data: {
    grade_name:'',
    class_name:'',
    array: ['全部','请假', '迟到', '缺勤', '已签到'],
    index: 0,
    listData: [
      { "code": "陈霞", "text": "已签到", "time": "08:30:46", "type": "18350866589" },
      { "code": "陈霞", "text": "已签到", "time": "08:30:46", "type": "18350866589" },
      { "code": "陈霞", "text": "已签到", "time": "08:30:46", "type": "18350866589" },
      { "code": "陈霞", "text": "已签到", "time": "08:30:46", "type": "18350866589" },
      { "code": "陈霞", "text": "已签到", "time": "08:30:46", "type": "18350866589" },
      { "code": "陈霞", "text": "已签到", "time": "08:30:46", "type": "18350866589" },
    ],
    now_month:'',
    now_date:'',
    week:''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let gradeName = wx.getStorageSync('classGrade')
    let className = wx.getStorageSync('classClass')
    let nowmonth = new Date().getMonth() + 1
    let nowdate = new Date().getDate()
    let nowday = new Date().getDay()
    let week
    switch (nowday) {
      case 0:  week = "星期天"; break;
      case 1:  week = "星期一"; break;
      case 2:  week = "星期二"; break;
      case 3:  week = "星期三"; break;
      case 4:  week = "星期四"; break;
      case 5:  week = "星期五"; break;
      case 6:  week = "星期六"; break;
    }  
    this.setData({
      grade_name: gradeName,
      class_name: className,
      now_month: nowmonth,
      now_date: nowdate,
      week: week,
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  bindPickerChange(e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      index: e.detail.value
    })
  },
})