let app = getApp()
let that = this;
let log_teacherName
let log_teacherPhone
let log_gradeName
let log_className
let log_status

Page({
  data: {
    teacherName: log_teacherName,
    teacherPhone: log_teacherPhone,
    gradeName: log_gradeName,
    className: log_className,
    status: log_status
  },
  backBtn: function () {
    wx.navigateTo({
      url: '../info/info',
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    that = this
    log_teacherName = wx.getStorageSync('teacherName')
    log_teacherPhone = wx.getStorageSync('phoneNum')
    log_gradeName = wx.getStorageSync('classGrade')
    log_className = wx.getStorageSync('classClass')
    log_status = wx.getStorageSync('status')
    if (log_className == ''){
      log_className = '暂无'
    }
    if (log_gradeName == '') {
      log_gradeName = '暂无'
    }
    if (log_status == 'education') {
      log_status = '在教'
    } else if (log_status == 'holiday'){
      log_status = '休假'
    } else if (log_status == 'dimission') {
      log_status = '离职'
    }
    this.setData({
      teacherName: log_teacherName,
      teacherPhone: log_teacherPhone,
      gradeName: log_gradeName,
      className: log_className,
      status: log_status,
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

  }
})