// pages/authorize/authorize.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    nextPage: '/pages/index/index'
  },
  getUserInfo: function (e) {
    var that = this;
    console.log(e.detail.userInfo)
    if (e.detail.userInfo) {
      //用户按了授权按钮
      this.saveUserInfo(e.detail.userInfo);
      wx.setStorage({
        key: 'userInfo',
        data: e.detail.userInfo,
      });
      wx.navigateTo({
        url: that.data.nextPage,
      })
    } else {
      //用户按了拒绝按钮
      wx.showToast({
        icon: 'none',
        title: '请点击授权',
        mask: true,
        duration: 1000
      })
    }
  },
  saveUserInfo: function (userInfo) {
    var sessionId = wx.getStorageSync('sessionId');
    console.log('把用户信息发送到后端存储起来');
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/user/info/upload',
      method: 'post',
      data: {
        avatarUrl: userInfo.avatarUrl,
        city: userInfo.city,
        country: userInfo.country,
        gender: userInfo.gender,
        language: userInfo.language,
        nickName: userInfo.nickName,
        province: userInfo.province
      },
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': sessionId
      },
      success: function (res) {
        try {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            if (response.state) {
              console.log(response.msg);
            } else {
              console.log(response.msg)
            }
          }
        } catch (e) {
          console.log(e);
        }
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    var next_page = that.data.nextPage;
    if (options.hasOwnProperty('share_data')) {
      var response = JSON.parse(options.share_data);
      console.log(response);
      if (response.constructor === Object) {
        var parameter_name = response.parameter_name;
        var parameter_value = response.parameter_value;
        next_page = response.next_page + '?' + parameter_name + '=' + parameter_value;
        that.setData({
          nextPage: next_page
        })
      }
    }
    console.log('next_page', next_page)
  },
  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var that = this;
    wx.getSetting({
      success: function (res) {
        if (res.authSetting['scope.userInfo']) {
          console.log(res.authSetting['scope.userInfo']);
          wx.redirectTo({
            url: that.data.nextPage,
          })
        }
      }
    })
  }
})