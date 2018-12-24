// pages/rankinglist/rankinglist.js
Page({
  data: {
    winWidth: 0,
    winHeight: 0,
    currentTab: 0,
    image: "",
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