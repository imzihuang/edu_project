let app = getApp()
let that = this;

Page({
  data: {
    studentName: '',
    studentClass: '',
    studentSex: '',
    studentBirthday: '',
    studentGrade: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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
    let storage_studentName = wx.getStorageSync('studentName')
    let storage_studentClass = wx.getStorageSync('studentClass')
    let storage_studentGrade = wx.getStorageSync('studentGrade')
    let storage_studentBirthday = wx.getStorageSync('studentBirthday')
    let storage_studentSex = wx.getStorageSync('studentSex')
    if(storage_studentSex=='1'){
      storage_studentSex = '男'
    }else{
      storage_studentSex = '女'
    }

    that = this
    that.setData({
      studentName: storage_studentName,
      studentClass: storage_studentClass,
      studentGrade: storage_studentGrade,
      studentSex: storage_studentSex,
      studentBirthday: storage_studentBirthday
    });
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