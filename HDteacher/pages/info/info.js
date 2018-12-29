let app = getApp()
let that = this;

Page({
  data: {
    class_name:'',
    grade_name:'',
    teacher_name: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let that = this;
    let teacherName = wx.getStorageSync('teacherName')
    let gradeName = wx.getStorageSync('classGrade')
    let className = wx.getStorageSync('classClass')
    if (className == ''){
      className = '暂无'
    }
    if (gradeName == '') {
      gradeName = '暂无'
    }
    that.setData({
      teacher_name: teacherName,
      grade_name: gradeName,
      class_name: className,
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
    let storage_studentName = wx.getStorageSync('studentName')
    let storage_studentClass = wx.getStorageSync('studentClass')
    let storage_studentGrade = wx.getStorageSync('studentGrade')

    that = this
    that.setData({
      studentName: storage_studentName,
      studentClass: storage_studentClass,
      studentGrade: storage_studentGrade
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