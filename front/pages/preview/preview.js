// pages/preview/pewview.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    nickName: '',
    avatarUrl: '',
    user_id: '',
    composition_id: 0,
    compositionUrl: '',
    compositionType: 0,
    compositionAngle: 0,
    objectCompositionAngle: {
      0: '',
      90: 'angle90',
      180: 'angle180',
      270: 'angle270'
    }
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
    // 自己生成的用本地储存，看别人的用服务端请求
    var userInfo = wx.getStorageSync('userInfo');
    console.log(userInfo);
    /*
    if (options.hasOwnProperty('composition_id')) {
      ;
    } else {
      wx.request({
        url: 'https://bugaboo.drivetogreen.com/',
        method: 'get',
        header: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        success: function (res) {
          var composition_id = composition_id;
        },
        fail: function(res) {},
        complete: function (res) {}
      });
    }
    */
    var composition = wx.getStorageSync('composition');
    console.log(composition);
    this.setData({
      compositionUrl: composition.compositionUrl,
      compositionType: composition.compositionType,
      compositionAngle: composition.compositionAngle,
      nickName: userInfo.nickName,
      avatarUrl: userInfo.avatarUrl
    })
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
      path: 'pages/preview/preview?user_id='+this.data.user_id+'&composition_id='+this.data.composition_id,
      success: (res) => { },
      fail: (res) => { }
    }
  }
})