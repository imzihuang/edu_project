// pages/login/login.js
let app = getApp()
let that
if (wx.getStorageSync('session_code')) {
  let session_code_value = wx.getStorageSync('session_code')
} else {
  let session_code_value = ''
}
Page({
  data: {
    userName: '',
    userCode: '',
    code_btn_no:false,
    // session_code:'',
  },
  userNameInput: function(e) {
    this.setData({
      userName: e.detail.value,
    })
  },
  userPasswordInput: function(e) {
    this.setData({
      userCode: e.detail.value,
    })
  },
  //获取验证码
  getCode: function(e) {
    let urlTitle = app.globalData.urlTitle;
    //电话号码校验
    let reg = /^[1][3,4,5,7,8][0-9]{9}$/;
    let phoneNum = this.data.userName;
    let flag = reg.test(phoneNum);
    let session_code_value = wx.getStorageSync('session_code');
    let that = this
    if (flag) {
      wx.request({
        url: urlTitle + '/push_verify/action',
        data: {
          phone: this.data.userName,
          edu_session: session_code_value
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        method: "POST",
        success(res) {
          if (res.data.state == 1) {
            wx.showModal({
              title: '提示',
              content: '发送失败',
              success(res) {
              }
            })
          } else if (res.data.state == 0){
            wx.showModal({
              title: '提示',
              content: '发送成功',
              success(res) {
              }
            })
            that.setData({
              code_btn_no: true,
            })
            var time = setTimeout(function () {
              that.setData({
                code_btn_no: false,
              })
            }, 30000);
          }
          console.log(res.data);
        }
      })
    } else {
      wx.showModal({
        title: '提示',
        content: '请输入正确的手机号',
        success(res) {
        }
      })
    }
  },
  //登录
  logIn: function(e) {
    let urlTitle = app.globalData.urlTitle
    //电话号码校验
    let reg = /^[1][3,4,5,7,8][0-9]{9}$/;
    let phoneNum = that.data.userName;
    let flag = reg.test(phoneNum);
    if (flag) {
      let session_code_value = wx.getStorageSync('session_code')
      if (session_code_value) {
        wx.request({
          url: urlTitle + '/bind/wx_action',
          data: {
            edu_session: session_code_value,
            phone: that.data.userName,
            verify_code: that.data.userCode
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
                content: '用户名或验证码错误 ',
                success(res) {
                }
              })
            } else if (res.data.state == 2){
                wx.showModal({
                  title: '提示',
                  content: '手机号还未注册 ',
                  success(res) {
                  }
                })
            }else {
              try {
                wx.setStorageSync('phoneNum', that.data.userName)
              } catch (e) {}
              wx.switchTab({
                url: '../index/index',
              })
            }

          }
        })
      } else {
        //session_code获取失败
        wx.showModal({
          title: '提示',
          content: '微信登录失败',
          success(res) {
          }
        })
      }
    } else {
      wx.showModal({
        title: '提示',
        content: '请输入正确的手机号',
        success(res) {
        }
      })
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    that = this
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
    try {
      let value = wx.getStorageSync('phoneNum')
      if (value != '' || value != undefine) {
        wx.switchTab({
          url: '../index/index',
        })
      } else {
        this.reqWxIdAndLogin()
      }
    } catch (e) {
      this.reqWxIdAndLogin()
    }
  },

  reqWxIdAndLogin: function() {
    app.globalData.loginInit = 0
    wx.login({
      success: function(res) {
        console.log('---wxLogin')
        console.log(res.code)

        wx.request({
          header: {
            'content-type': 'application/x-www-form-urlencoded'
          },
          url: app.globalData.urlTitle + '/login/wx_action',
          data: {
            code: res.code,
            wx_type: 2
          },
          method: 'POST',
          success: function(res) {
            console.log(res)
            try {
              wx.setStorageSync('session_code', res.data.session_code)
              session_code_value = wx.getStorageSync('session_code')
            } catch (e) {}
          },
          fail: function(res) {

          },
        })
      },
      fail: function(res) {

      }
    })
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

  },
  //只显示确认按钮模态弹窗，tilte：标题 content：提示内容 toUrl：点确定后跳转的页面路径
  promptShow: function(tilte, content, toUrl) {
    wx.showModal({
      title: tilte,
      content: content,
      showCancel: false,
      success: function(res) {
        if (res.confirm) {
          if (toUrl) {
            wx.switchTab({
              url: toUrl,
            })
          }
        }
      }
    })
  }
})