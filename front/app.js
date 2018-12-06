//app.js
App({
  onLaunch: function () {
    var userInfo = wx.getStorageInfoSync('userInfo');
    if (userInfo) {
      wx.navigateTo({
        url: '/pages/index/index',
      })
    } else {
      // 未授权，跳转到授权页面
      wx.navigateTo({
        url: '/pages/authorize/authorize',
      })
    }

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        /*
        if (res.code) {
          wx.request({
            url: 'https://wx.bestbwzs.com/login',
            method: 'POST',
            data: { code: res.code },
            header: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            success: function (res) {
              console.log(res.data);
              var sessionId = wx.getStorageSync('sessionId')
              sessionId = res.data.sessionId;
              wx.setStorageSync('sessionId', sessionId);
            }
          })
        } else {
          console.log('login failed: ' + res.errMsg)
        }
        */
      }
    })
  },
  globalData: {
    userInfo: null
  }
})