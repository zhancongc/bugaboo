// pages/rankinglist/rankinglist.js
const app = getApp()
Page({
  data: {
    current: 'tab1',
    tabTitle: 'Bugaboo用户组',
    compositionType: 1,
    gold: {
      avatarUrl: 'https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132',
      nickName: '詹聪聪',
      follow_times: 55
    },
    silver: {
      avatarUrl: 'https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132',
      nickName: '詹聪聪',
      follow_times: 44
    },
    copper: {
      avatarUrl: 'https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132',
      nickName: '詹聪聪',
      follow_times: 33
    },
    topFifty: [
      {avatarUrl: "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132", nickName: 'zcc1', follow_times: 33, number: 4},
      { avatarUrl: "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132", nickName: 'zcc2', follow_times: 22, number: 5},
      { avatarUrl: "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132", nickName: 'zcc3', follow_times: 11, number: 6}
    ],
    followMe: [
      { avatarUrl: "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132", nickName: 'jack' },
      { avatarUrl: "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132", nickName: 'lucy' },
      { avatarUrl: "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132", nickName: 'mike' }
    ]
  },
  handleChange({ detail }) {
    this.setData({
      current: detail.key
    });
  },
  onLoad: function (options) {
    var that = this;
    console.log('options', options);
    var title = compositionType == 1 ? 'Bugaboo用户组' :'非Bugaboo用户组'
    if (options.hasOwnProperty('composition_type')) {
      that.setData({
        compositionType: options.composition_type
      })
    }
    if (options.hasOwnProperty('tab')) {
      that.setData({
        current: options.tab
      })
    }
  },
  onShow: function () {
    var that = this;
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
        try {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            if (response.state === 1) {
              
              that.setData({
                gold: response.data[0],
                silver: response.data[1],
                copper: response.data[2],
                topFifty: response.data.slice(3,50)
              })
              that.raffle();
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
  onHide: function () {

  },
  onUnload: function () {

  },
  toPreview: function() {
    wx.navigateTo({
      url: '/pages/preview/preview?composition_id=1'
    })
  },
  toTab1: function (e) {
    var that = this;
    if (that.data.current == 'tab2') {
      that.setData({
        current: 'tab1'
      })
      console.log('current tab : tab1');
    }
  },
  toTab2: function(e) {
    var that = this;
    if (that.data.current == 'tab1') {
      that.setData({
        current: 'tab2'
      });
      console.log('current tab : tab2');
    }
    
  }
})