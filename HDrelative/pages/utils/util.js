function formatTime(date) {
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = date.getDate()

  var hour = date.getHours()
  var minute = date.getMinutes()
  var second = date.getSeconds()

  return year + '年' + month + '月' + day + '日' + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

function formatHMS(date) {
  var hour = date.getHours()
  var minute = date.getMinutes()
  var second = date.getSeconds()

  return [hour, minute, second].map(formatNumber).join(':')
}

//提供自动化指定的时间格式
function formatDate(date) {
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = date.getDate()

  return [year, month, day].map(formatNumber).join('-')
}

function formatDateTime(date) {
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = date.getDate()

  var hour = date.getHours()
  var minute = date.getMinutes()
  var second = date.getSeconds()

  return [year, month, day].map(formatNumber).join('-') + ' ' + [hour, minute, second].map(formatNumber).join(':')
}

function getMonthFirstDay(date) {
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = '01'

  return [year, month, day].map(formatNumber).join('-')
}

function splitDateTime(date) {
  return date.substring(11);
}

function formatNumber(n) {
  n = n.toString()
  return n[1] ? n : '0' + n
}

//判断对象是否为空
function isEmpty(param) {
  if (param == null || param == undefined) {
    return true
  } else if (typeof param == 'object') {
    var tmp = JSON.stringify(param)
    if (tmp == '{}' || tmp == '[]') {
      return true
    }
  }
  return false
}
//判断字符串是否为空
function isStrBlank(str) {
  if (str == null || str == undefined || str.replace(/(^\s*)|(\s*$)/g, '').length == '0') {
    return true
  }
  return false
}

function trim(str) {
  return str.replace(/(^\s*)|(\s*$)/g, '')
}

function cloneObj(obj) {
  var newObj
  if (typeof obj == "object") {
    if (obj == null) {
      newObj = null
    } else {
      newObj = {}
      if (obj instanceof Array) {
        newObj = []
      }
      for (var key in obj) {
        var val = obj[key]
        newObj[key] = cloneObj(val)
      }
    }
  } else {
    newObj = obj
  }
  return newObj
}

function getAuthz(cb, scopeStr) {
  wx.getSetting({
    success: (res) => {
      console.log("--当前[" + scopeStr + "]授权状态：" + res.authSetting[scopeStr]);
      if (isEmpty(res.authSetting[scopeStr])) {
        if (scopeStr == 'scope.userInfo') {
          typeof cb == 'function' && cb(false)
          return
        }
        wx.authorize({
          scope: scopeStr,
          success: (res2) => {
            typeof cb == 'function' && cb(true)
          },
          fail: (res2) => {
            console.log('--wx.authorize fail')
            typeof cb == 'function' && cb(false)
          }
        })
      } else if (res.authSetting[scopeStr] != true) {
        typeof cb == 'function' && cb(false)
      } else {
        typeof cb == 'function' && cb(true)
      }
    }
  })
}

//普通request fail处理共通方法 witchInterface：请求的接口 res：fail返回的res
function reqFailToDo(witchInterface, failRes) {
  console.log('---' + witchInterface + ' [util reqFailToDo]')
  console.log(failRes)
  wx.getNetworkType({
    success: function (res) {
      var title = ''
      var image = '../../pages/image/warning.png'
      var icon = ''
      // 返回网络类型, 有效值：
      // wifi/2g/3g/4g/unknown(Android下不常见的网络类型)/none(无网络)
      var networkType = res.networkType
      if (networkType == 'none') {
        title = '网络不可用'
      } else if (failRes.errMsg) {
        if (failRes.errMsg.match(/(?=.*?fail timeout)/)) {
          title = '数据加载超时，请稍后重试'
          icon = 'none'
        } else if (failRes.errMsg.match(/(?=.*?Unable to resolve host)/) || failRes.errMsg.match(/(?=.*?failed to connect to)(?=.*?after)(?=.*?ms)/)) {
          title = '服务网络不可达'
        } else if (failRes.errMsg == 'request:fail ') {
          title = '服务器无响应，请稍后重试'
          icon = 'none'
        } else {
          title = '系统内部错误'
        }
      } else {
        title = '系统内部错误'
      }
      wx.showToast({
        title: title,
        image: title.length > 7 ? '' : image,
        icon: icon ? icon : 'loading',
        duration: 2000,
      })
    },
    fail: function (res) {
      console.log('-- util reqFailToDo fail:' + res.errMsg)
    }
  })
}

module.exports = {
  formatTime: formatTime,
  formatHMS: formatHMS,
  formatDate: formatDate,
  formatDateTime: formatDateTime,
  formatNumber: formatNumber,
  getMonthFirstDay: getMonthFirstDay,
  splitDateTime: splitDateTime,
  isEmpty: isEmpty,
  isStrBlank: isStrBlank,
  trim: trim,
  cloneObj: cloneObj,
  reqFailToDo: reqFailToDo,
  getAuthz,
  getAuthz
}