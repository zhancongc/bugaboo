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
                    if (response.state == 1) {
                      that.globalData.userId = response.data.user_id,
                        that.globalData.sessionId = response.data.session_id;
                      that.globalData.activityOn = response.data.activity_on;
                      that.globalData.raffleTimes = response.data.raffle_times;
                      that.globalData.myCompositionId = response.data.composition_id;
                      that.globalData.myAvatarUrl = response.data.avatarUrl;
                      resolve(res);
                      that.globalData.myNickName = response.data.nickName;
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
  nextPageInit: function () {
    this.globalData.parameter_name = 'a';
    this.globalData.parameter_value = '1';
    this.globalData.next_page = '/pages/index/index';
  },
  globalData: {
    // wxlogin
    userId: 0,
    sessionId: '',
    activityOn: true,
    canUploadUserInfo: false,
    raffleTimes: false,
    //loading
    loaded: false,
    // preview & view
    myCompositionId: 0,
    myAvatarUrl: '',
    myNickName: '',
    //share
    parameter_name: 'a',
    parameter_value: '1',
    next_page: '/pages/index/index'
  }
})