let app = getApp()
let that = this;
let app_relativeName
var session_code_value = wx.getStorageSync('session_code')

Page({
  data: {
    relativeName: app_relativeName,
    productInfo: {} ,
    imgpaths:'../images/face.png'
  },
  upImg: function () {
    let session_code_value = wx.getStorageSync('session_code')
    wx.chooseImage({
      count: 1,  //最多可以选择的图片总数  
      sizeType: ['compressed'], // 可以指定是原图还是压缩图，默认二者都有  
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有  
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片  
        let tempFilePaths = res.tempFilePaths;
        that.setData({
          imgpaths: tempFilePaths[0],
        })
      }
    });  
  },
  replyBtn: function () {
    if (that.data.imgpaths == '../images/face.png') {
      wx.showModal({
        title: '提示',
        content: '请上传接送人照片',
        success(res) {
          if (res.confirm) {
            console.log('用户点击确定')
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    } else {
    let session_code_value = wx.getStorageSync('session_code')
    //启动上传等待中...  
    wx.showToast({
      title: '正在提交...',
      icon: 'loading',
      mask: true,
      duration: 10000
    })
    let uploadImgCount = 0;
    let urlTitle = app.globalData.urlTitle;
      wx.uploadFile({
        url: urlTitle + '/face_auth/action',
        filePath: that.data.imgpaths,
        name: 'image',
        formData: {
          'edu_session': session_code_value,
          'relevance_id': app.globalData.relativeId
        },
        header: {
          "Content-Type": "multipart/form-data"
        },
        success: function (res) {
          console.log(res)
          wx.navigateTo({
            url: '../addface/addface',
          })
        },
        fail: function (res) {
          wx.hideToast();
          wx.showModal({
            title: '错误提示',
            content: '提交失败',
            showCancel: false,
            success: function (res) { }
          })
        }
      });
    }
  },
  backBtn: function () {
    wx.navigateTo({
      url: '../addface/addface',
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    that = this
    app_relativeName = app.globalData.relativeName
    this.setData({
      relativeName: app_relativeName,
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