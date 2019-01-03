// pages/authorize/authorize.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {

  },
  getUserInfo: function (e) {
    console.log(e.detail.userInfo)
    if (e.detail.userInfo) {
      //用户按了授权按钮
      this.saveUserInfo(e.detail.userInfo);
      wx.setStorage({
        key: 'userInfo',
        data: e.detail.userInfo,
      });
      wx.navigateTo({
        url: '/pages/index/index',
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
    // 查看是否授权
    wx.getSetting({
      success: function (res) {
        if (res.authSetting['scope.userInfo']) {
          console.log(res.authSetting['scope.userInfo']);
          wx.navigateTo({
            url: '/pages/index/index',
          })
        }
      }
    })
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    wx.getSetting({
      success: function (res) {
        if (res.authSetting['scope.userInfo']) {
          console.log(res.authSetting['scope.userInfo']);
          wx.redirectTo({
            url: '/pages/index/index',
          })
        }
      }
    })
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})