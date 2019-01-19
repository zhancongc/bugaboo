// pages/authorize/authorize.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    loaded: false,
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    console.log("options", options);
    if (options.hasOwnProperty('share_data')) {
      var response = JSON.parse(options.share_data);
      console.log(response);
      if (response.constructor === Object) {
        app.globalData.parameter_name = response.parameter_name;
        app.globalData.parameter_value = response.parameter_value;
        app.globalData.next_page = response.next_page;
      }
      if (response.next_page==='/pages/raffle/raffle') {
        app.userLogin();
      }
    }
  },
  onReady: function (e) {
    //禁止分享
    wx.showShareMenu({
      withShareTicket: false
    });
  },
  getUserInfo: function (e) {
    console.log(e.detail.userInfo)
    if (e.detail.userInfo) {
      //用户按了授权按钮
      wx.setStorageSync('userInfo', e.detail.userInfo);
      app.globalData.canUploadUserInfo = true;
      wx.navigateTo({
        url: app.globalData.next_page + '?' + app.globalData.parameter_name + '=' + app.globalData.parameter_value,
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
  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    wx.showLoading({
      title: '加载中',
    })
    var that = this;
    var path = '/pages/view/view';
    app.userLogin().then(function (res) {
      // 通信完毕
      app.globalData.loaded = true;
      console.log('next_page', app.globalData.next_page);
      if (app.globalData.next_page == path) {
        wx.hideLoading();
        wx.navigateTo({
          url: path + '?' + app.globalData.parameter_name + '=' + app.globalData.parameter_value,
        })
      } else {
        wx.getSetting({
          success: function (res) {
            if (res.authSetting['scope.userInfo']) {
              console.log(res.authSetting['scope.userInfo']);
              wx.hideLoading();
              wx.redirectTo({
                url: app.globalData.next_page,
              })
            } else {
              wx.hideLoading();
              // 不跳转就显示授权
              that.setData({
                loaded: true
              });
            }
          }
        })
      }
    })
  }
})