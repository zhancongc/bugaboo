// pages/rankinglist/rankinglist.js
const app = getApp()
Page({
  data: {
    current: 'tab1',
    tabTitle: 'Bugaboo用户组',
    compositionType: 1,
    /* avatarUrl: 'https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132',
      nickName: '詹聪聪',
      follow_times: 55 */
    gold: {
      avatarUrl: '',
      nickName: '',
      follow_times: 0
    },
    silver: {
      avatarUrl: '',
      nickName: '',
      follow_times: 0
    },
    copper: {
      avatarUrl: '',
      nickName: '',
      follow_times: 0
    },
    topFifty: [],
    followMe: []
  },
  handleChange({ detail }) {
    this.setData({
      current: detail.key
    });
  },
  onLoad: function (options) {
    var that = this;
    console.log('options', options);
    var title = options.composition_type == 1 ? 'Bugaboo用户组' :'非Bugaboo用户组';
    if (options.hasOwnProperty('composition_type')) {
      that.setData({
        tabTitle: title,
        compositionType: options.composition_type
      });
    }
    if (options.hasOwnProperty('tab')) {
      that.setData({
        current: options.tab
      });
    }
  },
  onShow: function () {
    var that = this;
    if (that.data.current=='tab1') {
      that.showRank();
    } else {
      that.showFollow();
    }
  },
  onReady: function (e) {
  },
  onHide: function () {

  },
  onUnload: function () {

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
  toPreview: function() {
    wx.navigateTo({
      url: '/pages/preview/preview'
    })
  },
  showRank : function () {
    var that = this;
    wx.showLoading({
      title: '加载中',
      mask: true
    });
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/rankinglist',
      method: 'post',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': app.globalData.sessionId
      },
      data: {
        ranking_list_type: that.data.compositionType
      },
      success: function (res) {
        wx.hideLoading();
        try {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            if (response.state === 1) {
              if (response.data.length >3) {
                that.setData({
                  gold: response.data[0],
                  silver: response.data[1],
                  copper: response.data[2],
                  topFifty: response.data.slice(3, 50)
                })
              }
            }
          }
        } catch (e) {
          console.log(e);
        }
      },
      fail: function (res) {
        wx.hideLoading();
        wx.showToast({
          title: '请稍后重新再试',
        })
      }
    })
  },
  showFollow: function () {
    var that = this;
    wx.showLoading({
      title: '加载中',
      mask: true
    });
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/user/followers',
      method: 'get',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': app.globalData.sessionId
      },
      success: function (res) {
        wx.hideLoading();
        try {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            if (response.state === 1) {
              if (response.data.length > 0) {
                that.setData({
                  followMe: response.data
                })
              }
            }
          }
        } catch (e) {
          console.log(e);
        }
      },
      fail: function (res) {
        wx.hideLoading();
        wx.showToast({
          title: '请稍后重新再试',
        })
      }
    })
  },
  toTab1: function (e) {
    var that = this;
    if (that.data.current == 'tab2') {
      that.setData({
        current: 'tab1'
      })
      console.log('current tab : tab1');
      if (that.data.topFifty.length === 0) {
        that.showRank();
      }
    }
  },
  toTab2: function(e) {
    var that = this;
    if (that.data.current == 'tab1') {
      that.setData({
        current: 'tab2'
      });
      console.log('current tab : tab2');
      if (that.data.followMe.length === 0) {
        that.showFollow();
      } 
    }
  }
})