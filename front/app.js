//app.js
App({
  onLaunch: function () {

  },
  userLogin: function () {
    var that = this;
    return new Promise(function (resolve, reject) {
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
                      that.globalData.userId = response.data.user_id,
                      that.globalData.sessionId = response.data.session_id;
                      that.globalData.activityOn = response.data.activity_on;
                      that.globalData.raffleTimes = response.data.raffle_times;
                      if (response.state == 1) {
                        var compositionId = response.data.composition_id;
                        that.globalData.compositionId = response.data.composition_id;
                      }
                      resolve(res);
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
    })
  },
  globalData: {
    // wxlogin
    userId: 0,
    sessionId: '',
    activityOn: false,
    canUploadUserInfo: false,
    raffleTimes: false,
    // preview & view
    compositionId: 0
  }
})