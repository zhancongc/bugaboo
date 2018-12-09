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
    wx.uploadFile({
      url: 'https://wx.bestbwzs.com/upload/images',
      filePath: images[0],
      name: that.imageName,
      header: 'Content-Type": "multipart/form-data',
      formData: {
        photographType: that.data.gameGroupIndex
      },
      success: function (res) {
        wx.hideToast()
        that.setData({
          photographId: res.data['photographId']
        })
        wx.navigateTo({
          url: '/pages/preview/preview?photographId=' + that.data.photographId,
        })
      },
      fail: function (res) {
        wx.hideToast();
        wx.showToast({
          title: '上传失败',
          duration: 1000
        })
      },
      complete: function (res) { },
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 自己生成的用本地储存，看别人的用服务端请求
    var userInfo = wx.getStorageSync('userInfo');
    console.log(userInfo);
    var composition = JSON.parse(options.composition);
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