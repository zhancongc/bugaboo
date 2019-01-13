// pages/awardlist/awardlist.js
const app = getApp()
Page({
  /**
   * 页面的初始数据
   */
  data: {
    awards: [
      { "awardrecord_id": 1, "awardrecord_type": 1, "award_name": "bugaboo限量笔记本", "award_image": "https://bugaboo.drivetogreen.com/static//images/award_bottle.png", "award_time": "2019/01/12 12:00", 'checked': false, 'informed': false },
      { "awardrecord_id": 2, "awardrecord_type": 1, "award_name": "bugaboo定制保温杯", "award_image": "https://bugaboo.drivetogreen.com/static//images/award_bag.png", "award_time": "2019/01/12 12:00", 'checked': true, 'informed': true },
      { "awardrecord_id": 3, "awardrecord_type": 1, "award_name": "bugaboo限量定制健身包", "award_image": "https://bugaboo.drivetogreen.com/static//images/award_notebook.png", "award_time": "2019/01/12 12:00", 'checked': false, 'informed': true },
      { "awardrecord_id": 4, "awardrecord_type": 2, "award_name": "50元天猫商城代金券", "award_image": "https://bugaboo.drivetogreen.com/static//images/award_coupon_50.png", "award_time": "2019/01/12 12:00", 'checked': true, 'informed': true },
      { "awardrecord_id": 5, "awardrecord_type": 2, "award_name": "100元天猫商城代金券", "award_image": "https://bugaboo.drivetogreen.com/static//images/award_coupon_100.png", "award_time": "2019/01/12 12:00", 'checked': false, 'informed': false },
      { "awardrecord_id": 6, "awardrecord_type": 3, "award_name": "一等奖", "award_image": "https://bugaboo.drivetogreen.com/static//images/award_golden.png", "award_time": "2019/01/12 12:00", 'checked': false, 'informed': false },
      { "awardrecord_id": 7, "awardrecord_type": 4, "award_name": "二等奖", "award_image": "https://bugaboo.drivetogreen.com/static//images/award_silver.png", "award_time": "2019/01/12 12:00", 'checked': false, 'informed': false }
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
  onReady: function () {},

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {},

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {},

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
  onPullDownRefresh: function () {},

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {  },
  toInform: function (e) {
    console.log(e.target.dataset);
    wx.navigateTo({
      url: '/pages/inform/inform?awardrecord_id=' + e.target.dataset.awardrecord_info[0] +'&awardrecord_type='+e.target.dataset.awardrecord_info[1],
    })
  },
  toAward: function (e) {
    console.log(e.target.dataset);
    wx.navigateTo({
      url: '/pages/award/award?awardrecord_id=' + e.target.dataset.awardrecord_id,
    })
  }
})