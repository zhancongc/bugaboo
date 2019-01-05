//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
  },
  onLoad: function () {
    // 给app.js 定义一个方法。
    app.userInfoReadyCallback = res => {
      var response = res.data;
      console.log(response);
      if (response.constructor === Object) {
        if (response.state) {
          app.globalData.sessionId = response.data.sessionId;
          if (response.state == 1) {
            var compositionId = response.data.composition_id;
            app.globalData.compositionId = response.data.composition_id;
          }
        }
      }
    };
    var compositionId = app.globalData.compositionId;
    if (compositionId) {
      wx.redirectTo({
        url: '/pages/preview/preview?composition_id=' + compositionId,
      })
    }
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
      url: '/pages/compositionCut/compositionCut',
    })
  },
})
