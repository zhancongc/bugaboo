//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
  },
  onLoad: function () {

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
    //如果有作品直接到自己的作品，如果没有就是参加活动
    var session_id = wx.getStorageSync('session_id');
    if (session_id) {
      // 判断是否有作品
      wx.request({
        url: 'https://bugaboo.drivetogreen.com/user/composition/info',
        method: 'get',
        header: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Session-Id': session_id
        },
        success: function (res) {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            if (response.state === 1) {
              wx.redirectTo({
                url: '/pages/preview/preview?composition_id=' + response.data.composition_id
              })
            } else if (response.state === 0) {
              wx.showToast({
                title: '获取用户信息失败，请重试',
                icon: 'none',
                mask: true,
                duration: 1000
              });
            }
          }
        },
        fail: function (res) { },
        complete: function (res) { }
      })
    } else {
      wx.showToast({
        title: '请重新打开小程序再试'
      })
    }
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
    // 首先获取user_id和composition_id
    return {
      title: 'Bugaboo助力活动',
      path: 'pages/index/index',
      success: (res) => { },
      fail: (res) => { }
    }
  },
  //事件处理函数
  toComposition: function (e) {
    wx.navigateTo({
      url: '/pages/composition/composition',
    })
  },
})
