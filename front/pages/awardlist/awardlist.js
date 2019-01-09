// pages/awardlist/awardlist.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    awards: [
      { "awardrecord_id": 1, "award_name": "奖品一", "award_image": "../../images/bugaboo.jpg", "award_time": "2019/01/12 12:00" },
      { "awardrecord_id": 2, "award_name": "奖品二", "award_image": "../../images/bugaboo.jpg", "award_time": "2019/01/12 12:00" },
      { "awardrecord_id": 3, "award_name": "奖品三", "award_image": "../../images/bugaboo.jpg", "award_time": "2019/01/12 12:00" }
    ]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

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
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/raffle',
      method: 'get',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': app.globalData.sessionId
      },
      success: function (res) {
        try {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            if (response.state == 1) {
            }
          }
        } catch (e) {
          console.log(e);
        }
      },
      fail: function (res) {
        wx.showToast({
          title: '请稍后重新再试',
        })
      }
    })
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
  toAward: function (e) {
    console.log(e.target.dataset);
    wx.navigateTo({
      url: '/pages/award/award?awardrecord_id=' + e.target.dataset.awardrecord_id,
    })
  }
})