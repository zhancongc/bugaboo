// pages/rankinglist/rankinglist.js
Page({
  data: {
    current: 'tab1',
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