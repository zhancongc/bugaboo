//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    rankNumber: 3,
    visible1: false,
    visible2: false
  },
  onLoad: function () {
    var that = this;
    // 给app.js 定义一个方法。
    app.userLogin().then(function(res){
      var response = res.data;
      if (response.constructor === Object) {
        if (response.state) {
          app.globalData.sessionId = response.data.session_id;
          var userInfo = wx.getStorageSync('userInfo')
          if (app.globalData.canUploadUserInfo && userInfo) {
            that.saveUserInfo(userInfo);
            app.globalData.canUploadUserInfo = false;
          }
          if (response.state == 1) {
            if (response.data.activity_on){
              if (response.data.composition_id) {
                var compositionId = response.data.composition_id;
                app.globalData.compositionId = response.data.composition_id;
                wx.redirectTo({
                  url: '/pages/preview/preview?composition_id=' + compositionId,
                })
              }
            } else {
              that.setData({
                visible2: true
              })
            }
          }
        }
      }
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
      title: 'Bugaboo新年说爱你',
      path: 'pages/index/index',
      imageUrl: 'https://bugaboo.drivetogreen.com/static/images/bugaboo.jpeg',
      success: (res) => { },
      fail: (res) => { }
    }
  },
  saveUserInfo: function (userInfo) {
    var sessionId = app.globalData.sessionId;
    console.log('把用户信息发送到后端存储起来');
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/user/info/upload',
      method: 'post',
      data: {
        avatarUrl: userInfo.avatarUrl,
        city: userInfo.city,
        country: userInfo.country,
        gender: userInfo.gender,
        language: userInfo.language,
        nickName: userInfo.nickName,
        province: userInfo.province
      },
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': sessionId
      },
      success: function (res) {
        try {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            if (response.state) {
              console.log(response.msg);
            } else {
              console.log(response.msg)
            }
          }
        } catch (e) {
          console.log(e);
        }
      }
    })
  },
  handleClose1: function(e) {
    this.setData({
      visible1: false
    })
  },
  handleClose2: function (e) {
    this.setData({
      visible2: false
    })
  },
  //参加活动
  handleOpen1: function (e) {
    this.setData({
      visible1: true
    });
  },
  //参加活动
  handleOpen2: function (e) {
    this.setData({
      visible2: true
    });
  },
  //事件处理函数
  toComposition: function (e) {
    wx.navigateTo({
      url: '/pages/compositionCut/compositionCut',
    })
    this.handleClose1();
  },
  toAwardList: function(e) {
    wx.navigateTo({
      url: '/pages/awardlist/awardlist',
    })
    this.handleClose2();
  },
})
