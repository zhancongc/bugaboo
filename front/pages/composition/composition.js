// pages/composition/composition.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    imageName: '',
    gameGroupIndex: 0,
    gameGroup: ['非婴儿车组', '婴儿车组'],
    objectGameGroup: [{
      0: '非婴儿车组'},{
      1: '婴儿车组'
    }]
  },
  bindPickerChange: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      gameGroupIndex: e.detail.value
    })
  },
  choosePhotograph: function (e) {
    var that = this;
    wx.chooseImage({
      count: 1,
      sizeType: ['compress'],
      sourceType: ['album', 'camera'],
      success: function(res) {
        var tempFilesSize = res.tempFiles[0].size;
        if (tempFilesSize <= 5000000) {   //图片小于或者等于5M时 可以执行获取图片
          var tempFilePath = res.tempFilePaths[0]; //获取图片
          var tempComposition = {
              compositionUrl: tempFilePath,
              compositionType: that.data.gameGroupIndex
          };
          wx.navigateTo({
            url: '/pages/compositionCut/compositionCut?tempComposition='+JSON.stringify(tempComposition)
          })
        } else {    //图片大于5M，弹出一个提示框
          wx.showToast({
            title: '上传图片不能大于5M!',  //标题
            icon: 'none'       //图标 none不使用图标，详情看官方文档
          })
        }
      },
    })
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

  }
})