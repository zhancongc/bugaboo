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
    wx.showToast({
      icon: 'loading',
      title: '加载中',
      mask: true
    });
    var that = this;
    console.log('请求作品信息');
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/user/composition/info',
      method: 'get',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': app.globalData.sessionId
      },
      success: function (res) {
        wx.hideToast();
        var response = res.data;
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
            wx.showToast({
              title: '获取作品失败，请稍后重试',
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
      'parameter_name': 'composition_id',
      'parameter_value': that.data.compositionId,
      'next_page': '/pages/view/view'
    };
    console.log('share_data', share_data);
    return {
      title: '来自'+ this.data.nickName + '的新年祝福',
      imageUrl: this.data.compositionUrl,
      path: '/pages/authorize/authorize?share_data='+JSON.stringify(share_data),
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
  toRaffle: function () {
    wx.navigateTo({
      url: '/pages/raffle/raffle',
    })
  },
  toAuthorize: function () {
    wx.navigateTo({
      url: '/pages/authorize/authorize',
    })
  },
  toAward: function () {
    wx.navigateTo({
      url: '/pages/award/award',
    })
  },
  toAwardList: function () {
    wx.navigateTo({
      url: '/pages/awardlist/awardlist',
    })
  },
  toCompositionCut: function () {
    wx.navigateTo({
      url: '/pages/compositionCut/compositionCut',
    })
  },
  toRankingList: function () {
    var that = this;
    wx.navigateTo({
      url: '/pages/rankinglist/rankinglist?composition_type='+that.data.compositionType,
    })
  },
  toView: function () {
    wx.navigateTo({
      url: '/pages/view/view?composition_id=1',
    })
  }
})