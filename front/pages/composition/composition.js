// pages/composition/composition.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    images: [],
    imageName: '',
    gameGroupIndex: 0,
    gameGroup: ['婴儿车组', '非婴儿车组'],
    objectGameGroup: [{
      0:'婴儿车组'},{
      1:'非婴儿车组'
    }],
  },
  bindPickerChange: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      gameGroupIndex: e.detail.value
    })
  },
  uploadPhotograph: function (e) {
    var that = this;
    wx.chooseImage({
      count: 1,
      sizeType: ['compress'],
      sourceType: ['album', 'camera'],
      success: function(res) {
        var tempFilesSize = res.tempFiles[0].size;
        if (tempFilesSize <= 3000000) {   //图片小于或者等于5M时 可以执行获取图片
          var tempFilePaths = res.tempFilePaths[0]; //获取图片
          that.data.images.push(tempFilePaths);   //添加到数组
          that.setData({
            images: that.data.images
          });
          wx.showToast({
            title: '正在上传...',
            icon: 'loading',
            mask: true,
            duration: 3000
          });
          wx.uploadFile({
            url: 'https://wx.bestbwzs.com/images',
            filePath: images[0],
            name: that.imageName,
            header: 'Content-Type": "multipart/form-data',
            formData: {
              photographType: that.data.gameGroupIndex
            },
            success: function (res) {
              wx.hideToast()
              that.setData({
                photographId : res.data['photographId']
              })
              wx.navigateTo({
                url: '/pages/preview/preview?photographId='+that.data.photographId,
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
        } else {    //图片大于5M，弹出一个提示框
          wx.showToast({
            title: '上传图片不能大于2M!',  //标题
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
    this.setData({
      imageName: app.globalData.userInfo.nickName + '的作品'
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

  }
})