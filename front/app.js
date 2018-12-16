//app.js
App({
  onLaunch: function () {
    var userInfo = wx.getStorageSync('userInfo');
    console.log(userInfo);
    if (userInfo) {
      wx.reLaunch({
        url: '/pages/index/index',
      })
    } else {
      // 未授权，跳转到授权页面
      wx.reLaunch({
        url: '/pages/authorize/authorize',
      })
    }
    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        console.log(res.code);
        if (res.code) {
          wx.request({
            url: 'https://bugaboo.drivetogreen.com/user/login',
            method: 'post',
            data: { code: res.code },
            header: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            success: function (res) {
              console.log(res.data);
              try {
                var response = res.data;
                console.log(response);
                if (response.constructor === Object){
                  if (response.state) {
                    wx.setStorage({
                      key: 'session_id',
                      data: response.data,
                    })
                  } else {
                    wx.showToast({
                      title: response.msg,
                    })
                  }
                }
              } catch (e) {
                console.log(e);
              }
            },
            fail: function (res) {
              wx.showToast({
                title: '请稍后重新打开小程序再试',
              })
            }
          })
        } else {
          console.log('login failed: ' + res.errMsg)
        }
      }
    })
  },
  globalData: {
    userInfo: null
  }
})