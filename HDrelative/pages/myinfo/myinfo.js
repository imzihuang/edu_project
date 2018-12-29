let app = getApp()
let that = this;
let app_relativeName
let app_relativePhone
let urlTitle = app.globalData.urlTitle
let session_code_value = wx.getStorageSync('session_code')
let app_studentName = app.globalData.studentId

Page({
  data: {
    relativeName: app_relativeName,
    relativePhone: app_relativePhone,
    relative:'',
    studentName: app_studentName
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
    app_relativeName = app.globalData.relativeName
    app_relativePhone = wx.getStorageSync('phoneNum')
    this.setData({
      relativeName: app_relativeName,
      relativePhone: app_relativePhone,
    })
    let that = this
    let session_code_value = wx.getStorageSync('session_code')
    let studentId = wx.getStorageSync('studentId')
    //获取关系字段
    wx.request({
      url: urlTitle + '/relation/infos',
      data: {
        student_id: studentId,
        relative_id: app.globalData.relativeId,
        edu_session: session_code_value
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      method: "GET",
      success(res) {console.log(res);
        let relativeNow = res.data.data[0].relation;
        if (relativeNow == 'father'){
          relativeNow = '父亲'
        } else if (relativeNow == 'moter'){
          relativeNow = '母亲'
        } else if (relativeNow == 'grandfather') {
          relativeNow = '爷爷'
        } else{
          relativeNow = '奶奶'
        }
        that.setData({
          relative: relativeNow
        })
      }
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