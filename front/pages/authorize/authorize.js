// pages/authorize/authorize.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    parameter_name: '',
    parameter_value: '',
    nextPage: '/pages/index/index'
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
    }
    console.log('next_page', app.globalData.next_page)
  },
  getUserInfo: function (e) {
    console.log(e.detail.userInfo)
    if (e.detail.userInfo) {
      //用户按了授权按钮
      wx.setStorageSync('userInfo', e.detail.userInfo);
      app.globalData.canUploadUserInfo = true;
      wx.navigateTo({
        url: app.globalData.nextPage + '?' + app.globalData.parameter_name + '=' + app.globalData.parameter_value,
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
    var that = this;
    var path = '/pages/view/view';
    if (app.globalData.next_page == path){
      app.userLogin().then(function (res) {
        var response = res.data;
        if (response.constructor === Object) {
          if (response.state==1) {
            app.globalData.sessionId = response.data.session_id;
            if (response.data.activity_on) {
              if (response.data.composition_id) {
                var compositionId = response.data.composition_id;
                app.globalData.compositionId = response.data.composition_id;
                wx.redirectTo({
                  url: '/pages/preview/preview',
                })
              }
            } else {
              that.setData({
                visible2: true
              })
            }
          }
        }
        wx.navigateTo({
          url: path+'?'+app.globalData.parameter_name+'='+app.globalData.parameter_value,
        })
      })
    } else {
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
  }
})