// pages/award/award.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    awardrecordId: 0,
    awardName: '',
    qrcode: 'https://bugaboo.drivetogreen.com/static/images/bugaboo.png',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    that.setData({
      awardrecordId: options.awardrecord_id
    });
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
    wx.showToast({
      icon: 'loading',
      title: '加载中',
      mask: true
    });
    var that = this;
    console.log('请求奖品信息');
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/user/award',
      method: 'post',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': app.globalData.sessionId
      },
      data: {
        awardrecord_id: that.data.awardrecordId
      },
      success: function (res) {
        wx.hideToast();
        var response = res.data;
        console.log(response);
        if (response.constructor === Object) {
          if (response.state==1) {
            that.setData({
              awardName: response.data.award_name,
              qrcode: response.data.qrcode_image_url
            })
          } else {
            wx.showToast({
              title: '获取奖品信息失败，请稍后重试',
              icon: 'none',
              mask: true,
              duration: 1000
            });
          }
        }
      },
      fail: function (res) { },
      complete: function (res) { }
    });
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
  toAwardList: function () {
    wx.navigateTo({
      url: '/pages/awardlist/awardlist',
    })
  },
  toIndex: function () {
    wx.navigateTo({
      url: '/pages/index/index',
    })
  },
  preview : function (e) {
    var that = this;
    wx.previewImage({
      current: that.data.qrcode,
      urls: [that.data.qrcode],
    })
  }
})