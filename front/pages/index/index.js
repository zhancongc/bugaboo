//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    rankNumber: 99,
    visible1: false,
    visible2: false
  },
  onLoad: function (options) {
    var that = this;
    console.log(app.globalData);
    that.setData({ rankNumber: app.globalData.rankNumber });
    rankNumber: app.globalData.rankNumber
    var userInfo = wx.getStorageSync('userInfo')
    if (app.globalData.canUploadUserInfo===true && userInfo) {
      that.saveUserInfo(userInfo);
      app.globalData.canUploadUserInfo = false;
    }
    if (app.globalData.activityOn) {
      console.log('我的作品id', app.globalData.myCompositionId);
      if (app.globalData.myCompositionId) {
        wx.redirectTo({
          url: '/pages/preview/preview',
        });
      }
    } else {
      that.setData({
        visible2: true
      })
    }
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function (e) {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    app.nextPageInit();
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
    var that = this;
    var share_data = {
      'parameter_name': 'a',
      'parameter_value': '1',
      'next_page': '/pages/index/index'
    };
    console.log('share_data: ', '/pages/authorize/authorize?share_data=' + JSON.stringify(share_data));
    return {
      title: '送你神秘新年礼物，更有送祝福抽大奖活动',
      imageUrl: 'https://bugaboo.drivetogreen.com/static/images/share.jpg',
      path: '/pages/authorize/authorize?share_data=' + JSON.stringify(share_data),
      success: (res) => {
        wx.showToast({
          title: '分享成功',
        });
      },
      fail: (res) => {
        wx.showToast({
          title: '分享失败',
        })
      }
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
  //参加活动2
  handleOpen2: function (e) {
    this.setData({
      visible2: true
    });
  },
  //事件处理函数
  toComposition: function (e) {
    this.handleClose1();
    if (app.globalData.activityOn) {
      wx.navigateTo({
        url: '/pages/compositionCut/compositionCut',
      })
    } else {
      this.handleOpen2()
    }
  },
  toAwardList: function(e) {
    wx.navigateTo({
      url: '/pages/awardlist/awardlist',
    })
    this.handleClose2();
  },
  toRankingList: function (e) {
    wx.navigateTo({
      url: '/pages/rankinglist/rankinglist?composition_type='+'0',
    })
    this.handleClose2();
  },
  toIntro: function (e) {
    wx.navigateTo({
      url: '/pages/intro/intro',
    })
  },
  toAwardIntro: function (e) {
    wx.navigateTo({
      url: '/pages/awardIntro/awardIntro',
    })
  }
})
