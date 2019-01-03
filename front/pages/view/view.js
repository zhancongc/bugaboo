// pages/preview/pewview.js
const app = getApp()

Page({
  /**
   * 页面的初始数据
   */
  data: {
    visible1: false,
    userId: '',
    nickName: '',
    avatarUrl: '',
    compositionId: 0,
    compositionUrl: '',
    compositionType: 0
  },
  onClose(event) {
    if (event.detail === 'confirm') {
      // 异步关闭弹窗
      setTimeout(() => {
        this.setData({
          show: false
        });
      }, 1000);
    } else {
      this.setData({
        show: false
      });
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    if (options.hasOwnProperty('composition_id')) {
      var sessionId = wx.getStorageSync('sessionId');
      console.log('请求作品信息');
      wx.request({
        url: 'https://bugaboo.drivetogreen.com/user/composition',
        method: 'post',
        header: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Session-Id': sessionId
        },
        data: {
          composition_id: options.composition_id
        },
        success: function (res) {
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
      imageUrl: this.data.compositionUrl,
      path: 'pages/view/view?composition_id=' + this.data.compositionId,
      success: (res) => { },
      fail: (res) => { }
    }
  },
  toIndex: function () {
    wx.navigateTo({
      url: '/pages/index/index',
    })
  },
  handleOpen1() {
    this.setData({
      visible1: true
    });
  },

  handleClose1() {
    this.setData({
      visible1: false
    });
  },
  follow: function () {
    this.handleClose1();
  }
});


