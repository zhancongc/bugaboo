//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

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