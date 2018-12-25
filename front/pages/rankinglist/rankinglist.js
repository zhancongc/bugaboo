// pages/rankinglist/rankinglist.js
Page({
  data: {
    winWidth: 0,
    winHeight: 0,
    currentTab: 0,
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
  onLoad: function (options) {

  },
  onReady: function () {
    var that = this;
    wx.getSystemInfo({
      success: function (res) {
        that.setData({
          winWidth: res.windowWidth,
          winHeight: res.windowHeight
        });
      }
    });
  },
  // 滑动切换tab
  bindChange: function (e) {
    var that = this;
    that.setData({
      currentTab: e.detail.current
    });
    var title = that.data.currentTab == 0 ? 'TOP50助力排行榜' : '获得好友的助力';
    wx.setNavigationBarTitle({
      title: title
    })
  },
  // 点击tab切换
  swichNav: function (e) {
    var that = this;
    if (this.data.currentTab === e.target.dataset.current) {
      return false;
    } else {
      that.setData({
        currentTab: e.target.dataset.current
      })
    }
  },
  onShow: function () {

  },
  onHide: function () {

  },
  onUnload: function () {

  },
  toPreview: function() {
    wx.navigateTo({
      url: '/pages/preview/preview?composition_id=1'
    })
  }
})