//app.js
App({
  onLaunch: function () {
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
              try {
                var response = res.data;
                console.log(response);
                if (response.constructor === Object) {
                  if (response.state) {
                    wx.setStorage({
                      key: 'sessionId',
                      data: response.data.session_id,
                    });
                    wx.setStorage({
                      key: 'canRaffle',
                      data: response.data.can_raffle,
                    });
                    wx.setStorage({
                      key: 'canFollow',
                      data: response.data.can_follow,
                    });
                    if (response.state == 1) {
                      var compositionId = response.data.composition_id;
                      wx.setStorage({
                        key: 'compositionId',
                        data: compositionId,
                      })
                    }
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
    });
  },
  globalData: {
    userInfo: null
  }
})