// pages/inform/inform.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    receiver: '',
    phone: '',
    address: '',
    compositionId: 0,
    compositionType: 1
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

  },
  setName: function (e) {
    console.log(e.detail.value);
    this.setData({
      receiver: e.detail.value
    })
  },
  setPhone: function (e) {
    console.log(e.detail.value);
    this.setData({
      phone: e.detail.value
    })
  },
  setAddress: function (e) {
    console.log(e.detail.value);
    this.setData({
      address: e.detail.value
    })
  },
  commit: function(){
    //检查信息是否完整
    var that = this;
    that.inform();
  },
  inform: function(){
    var that = this;
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/user/composition',
      method: 'post',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': sessionId
      },
      data: {
        composition_id: this.data.compositionId
      },
      success: function (res) {
        wx.hideToast();
        var response = res.data;
        console.log(response);
        if (response.constructor === Object) {
          var viewer;
          if (response.state) {
            that.setData({
              userId: response.data.user_id,
              nickName: response.data.nickName,
              avatarUrl: response.data.avatarUrl,
              compositionId: response.data.composition_id,
              compositionUrl: response.data.composition_url,
              compositionType: response.data.composition_type
            })
          } else {
            wx.showToast({
              title: '获取助力作品失败，请稍后重试',
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
  }
})