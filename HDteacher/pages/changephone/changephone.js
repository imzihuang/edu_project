// pages/login/login.js
let app = getApp()
let that
let session_code_value = wx.getStorageSync('session_code')
let phoneNum = wx.getStorageSync('phoneNum')
Page({
  data: {
    userName: '',
    userCode: '',
  },

  userPasswordInput: function (e) {
    this.setData({
      userCode: e.detail.value,
    })
  },
  //获取验证码
  getCode: function (e) {
    let urlTitle = app.globalData.urlTitle;
    that = this
    //电话号码校验
    let reg = /^[1][3,4,5,7,8][0-9]{9}$/;
    let phoneNum = that.data.userName;
    let flag = reg.test(phoneNum);
    let session_code_value = wx.getStorageSync('session_code')
    
    if (flag) {
      wx.request({
        url: urlTitle + '/push_verify/action',
        data: {
          phone: that.data.userName,
          edu_session: session_code_value
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        method: "POST",
        success(res) {
          console.log(res.data);
          if (res.data.state == 1) {
            wx.showModal({
              title: '提示',
              content: '发送失败',
              success(res) {
                if (res.confirm) {
                  console.log('用户点击确定')
                } else if (res.cancel) {
                  console.log('用户点击取消')
                }
              }
            })
          } 
        }
      })
    } else {
      wx.showModal({
        title: '提示',
        content: '请输入正确的手机号',
        success(res) {
          if (res.confirm) {
            console.log('用户点击确定')
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    }
  },
  submitCode:function(){
    let that = this
    let urlTitle = app.globalData.urlTitle;
    let session_code_value = wx.getStorageSync('session_code')
    if (that.data.userCode != ''){
      wx.request({
        url: urlTitle + '/verify_phone_code/wx_action',
        data: {
          phone: that.data.userName,
          edu_session: session_code_value,
          verify_code: that.data.userCode
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        method: "POST",
        success(res) {
          console.log(res.data); 
          if (res.data.state == 1){
            wx.showModal({
              title: '提示',
              content: '验证失败',
              success(res) {
                if (res.confirm) {
                  console.log('用户点击确定')
                } else if (res.cancel) {
                  console.log('用户点击取消')
                }
              }
            })
          }else{
            wx.navigateTo({
              url: '../changenewphone/changenewphone',
            })
          }
        },
        fail: function (res) {
          wx.showModal({
            title: '提示',
            content: '验证失败',
            success(res) {
              if (res.confirm) {
                console.log('用户点击确定')
              } else if (res.cancel) {
                console.log('用户点击取消')
              }
            }
          })
        },
      })
    }else{
      wx.showModal({
        title: '提示',
        content: '请输入验证码',
        success(res) {
          if (res.confirm) {
            console.log('用户点击确定')
          } else if (res.cancel) {
            console.log('用户点击取消')
          }
        }
      })
    }
    
 
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    that = this
    let phoneNum = wx.getStorageSync('phoneNum')
    that.setData({
      userName: phoneNum,
    })
    console.log(phoneNum)
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
  //只显示确认按钮模态弹窗，tilte：标题 content：提示内容 toUrl：点确定后跳转的页面路径
  
})


