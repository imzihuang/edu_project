let app = getApp()
let that = this;
let app_teacherName
let urlTitle = app.globalData.urlTitle
var session_code_value = wx.getStorageSync('session_code')

Page({
  data: {
    teacherName: app_teacherName,
    productInfo: {},
    imgpaths: '../images/face.png',
    hasImg: false,
    imgId: ''
  },
  upImg: function() {
    let session_code_value = wx.getStorageSync('session_code')
    wx.chooseImage({
      count: 1, //最多可以选择的图片总数  
      sizeType: ['compressed'], // 可以指定是原图还是压缩图，默认二者都有  
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有  
      success: function(res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片  
        let tempFilePaths = res.tempFilePaths;
        that.setData({
          imgpaths: tempFilePaths[0],
        })
      }
    });
  },
  replyBtn: function() {
    if (that.data.imgpaths == '../images/face.png') {
      wx.showModal({
        title: '提示',
        content: '请上传照片',
        success(res) {
        }
      })
    } else {
      let session_code_value = wx.getStorageSync('session_code')
      if (that.data.hasImg == true) {
        wx.request({
          url: urlTitle + '/face/delete',
          data: {
            id: that.data.imgId,
            edu_session: session_code_value,
          },
          header: {
            'content-type': 'application/x-www-form-urlencoded'
          },
          method: "POST",
          success(res) {
            //启动上传等待中...  
            wx.showToast({
              title: '正在提交...',
              icon: 'loading',
              mask: true,
              duration: 3000
            })
            let uploadImgCount = 0;
            let urlTitle = app.globalData.urlTitle;
            wx.uploadFile({
              url: urlTitle + '/face_auth/action',
              filePath: that.data.imgpaths,
              name: 'image',
              formData: {
                'edu_session': session_code_value,
                'relevance_id': app.globalData.teacherId,
                'relevance_type': 2
              },
              header: {
                "Content-Type": "multipart/form-data"
              },
              success: function(res) {
                console.log(res)
                wx.showModal({
                  title: '提示',
                  content: '提交成功',
                  success(res) {
                    if (res.confirm) {
                      wx.switchTab({
                        url: '../info/info',
                      })
                    } else if (res.cancel) {
                    }
                  }
                })
              },
              fail: function(res) {
                wx.hideToast();
                wx.showModal({
                  title: '错误提示',
                  content: '提交失败',
                  showCancel: false,
                  success: function(res) {}
                })
              }
            });
          },
          fail: function (res) {
            wx.showModal({
              title: '提示',
              content: '上传照片失败',
              success(res) {

              }
            })
          }
        })
      }
    }
  },
  // backBtn: function () {
  //   wx.navigateTo({
  //     url: '../info/info',
  //   })
  // },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    that = this
    app_teacherName = app.globalData.teacherName
    this.setData({
      teacherName: app_teacherName,
    })
    //初始图片获取
    wx.request({
      url: urlTitle + '/face/infos',
      data: {
        relevance_id: app.globalData.teacherId,
        edu_session: session_code_value,
        relevance_type: 2
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      method: "GET",
      success(res) {
        console.log(res)
        if (res.data.data.length > 0) {
          that.setData({
            imgpaths: urlTitle + '/edu/' + res.data.data[0].img_path,
            hasImg: true,
            imgId: res.data.data[0].id
          })
        }
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  }
})