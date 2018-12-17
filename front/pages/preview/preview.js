// pages/preview/pewview.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userId: '',
    nickName: '',
    avatarUrl: '',
    compositionId: 0,
    compositionUrl: '',
    compositionType: 0
  },
  uploadPhotograph: function () {
    wx.showToast({
      title: '正在上传...',
      icon: 'loading',
      mask: true,
      duration: 3000
    });
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options);
    // 向服务端请求别人的nickName,avatarUrl,composition_id
    if (options.hasOwnProperty('composition_id')) {
      var session_id = wx.getStorageSync('session_id');
      wx.request({
        url: 'https://bugaboo.drivetogreen.com/user/composition',
        method: 'post',
        header: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Session-Id': session_id
        },
        data: {
          composition_id: options.composition_id
        },
        success: function (res) {
          try {
            var response = JSON.parse(res.data);
            console.log(response);
            if (response.constructor === Object) {
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
                console.log(response);
                wx.showToast({
                  title: '获取助力作品失败，请稍后重试',
                  icon: 'none',
                  mask: true,
                  duration: 1500
                });
              }
            }
          } catch (e) {

          }
          var composition_id = composition_id;
        },
        fail: function(res) {},
        complete: function (res) {}
      });
    } else {
      wx.showToast({
        title: '获取不到作品信息',
        icon: 'none',
        mask: true,
        duration: 1000
      });
      wx.navigateTo({
        url: '/pages/index/index',
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
      title: this.data.nickName + '的Bugaboo助力作品',
      path: 'pages/preview/preview?'+'&composition_id='+this.data.composition_id,
      success: (res) => { },
      fail: (res) => { }
    }
  }
})