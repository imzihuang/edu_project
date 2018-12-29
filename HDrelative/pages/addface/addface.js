// pages/addface/addface.js
let app = getApp()
let that = this
let urlTitle = app.globalData.urlTitle
let session_code_value = wx.getStorageSync('session_code')
Page({
  data: {
    items: [],
    startX: 0, //开始坐标
    startY: 0,
    imgUrlTitle: '',
    relativeName: '',
    addRelativeBtn:'block'
  },
  onLoad: function () {
    let that = this
    let app_relativeName = app.globalData.relativeName
    let session_code_value = wx.getStorageSync('session_code')
    this.setData({
      imgUrlTitle: urlTitle,
      relativeName: app_relativeName
    })
    //初始数据获取
    wx.request({
      url: urlTitle + '/face/infos',
      data: {
        relevance_id: app.globalData.relativeId,
        edu_session: session_code_value
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      method: "GET",
      success(res) {
        //显示隐藏添加亲属图片按钮
        for (let i = 0; i < res.data.data.length;i++){
          if (res.data.data[i].relevance_type == 1) {
            that.setData({
              addRelativeBtn: 'none'
            })
          }
        }
        //显示隐藏添加亲属图片按钮--end//
        let newItems = res.data.data
        for (let i = 0; i < newItems.length; i++) {
          newItems[i].isTouchMove = false//默认全隐藏删除
        }
        for (let i = 0; i < newItems.length; i++) {
          let numberOne;
          if (newItems[0].relevance_type != 1){
            if (newItems[i].relevance_type == 1) {
              numberOne = newItems[i];
              newItems.splice(i);
              newItems.unshift(numberOne); console.log(newItems);
            }
          }
        }
        that.setData({
          items: newItems,
        })
      }
    })
  },
  
  //手指触摸动作开始 记录起点X坐标
  touchstart: function (e) {
    let that = this
    //开始触摸时 重置所有删除
    that.data.items.forEach(function (v, i) {
      if (v.isTouchMove)//只操作为true的
        v.isTouchMove = false;
    })
    that.setData({
      startX: e.changedTouches[0].clientX,
      startY: e.changedTouches[0].clientY,
      items: that.data.items
    })
  },
  //滑动事件处理
  touchmove: function (e) {
    let that = this,
      index = e.currentTarget.dataset.index,//当前索引
      startX = that.data.startX,//开始X坐标
      startY = that.data.startY,//开始Y坐标
      touchMoveX = e.changedTouches[0].clientX,//滑动变化坐标
      touchMoveY = e.changedTouches[0].clientY,//滑动变化坐标
      //获取滑动角度
      angle = that.angle({ X: startX, Y: startY }, { X: touchMoveX, Y: touchMoveY });
    that.data.items.forEach(function (v, i) {
      v.isTouchMove = false
      //滑动超过30度角 return
      if (Math.abs(angle) > 30) return;
      if (i == index) {
        if (touchMoveX > startX) //右滑
          v.isTouchMove = false
        else //左滑
          v.isTouchMove = true
      }
    })
    //更新数据
    that.setData({
      items: that.data.items
    })
  },
  /**
   * 计算滑动角度
   * @param {Object} start 起点坐标
   * @param {Object} end 终点坐标
   */
  angle: function (start, end) {
    var _X = end.X - start.X,
      _Y = end.Y - start.Y
    //返回角度 /Math.atan()返回数字的反正切值
    return 360 * Math.atan(_Y / _X) / (2 * Math.PI);
  },
  //删除事件
  del: function (e) {
    let that=this
    let session_code_value = wx.getStorageSync('session_code')
    wx.request({
      url: urlTitle + '/face/delete',
      data: {
        id: e.currentTarget.id,
        edu_session: session_code_value
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      method: "POST",
      success(res) {
        that.onLoad()
      }
    })
  },
  changeProperty: function (e) {
    console.log(e.detail.value);
    let that = this
    let session_code_value = wx.getStorageSync('session_code')
    if (e.detail.value == true){
      wx.request({
        url: urlTitle + '/face_activate/action',
        data: {
          id: e.currentTarget.id,
          edu_session: session_code_value
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        method: "POST",
        success(res) {
          wx.showModal({
            title: '提示',
            content: '设置成功',
            success(res) {
              that.onLoad()
            }
          })
          
        }
      })
    }else{
      let session_code_value = wx.getStorageSync('session_code')
      wx.request({
        url: urlTitle + '/face_disable/action',
        data: {
          id: e.currentTarget.id,
          edu_session: session_code_value
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        method: "POST",
        success(res) {
          wx.showModal({
            title: '提示',
            content: '设置成功',
            success(res) {
              that.onLoad()
            }
          })
          that.onLoad()
        }
      })
    }
  },
  goAddfacedetail: function () {
    wx.navigateTo({
      url: '../addfacedetail/addfacedetail',
    })
  },
  goaddrelativeface: function () {
    wx.navigateTo({
      url: '../addrelativeface/addrelativeface',
    })
  },
  onUnload: function () {
    wx.redirectTo({
      url: '../index/index'
    })
    wx.navigateTo({
      url: '../index/index'
    })
    wx.switchTab({
      url: '../index/index'
    })
  }
})