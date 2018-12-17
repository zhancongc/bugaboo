// pages/compositionCut/compositionCut.js
const qiniuUploader = require("../../utils/qiniuUploader");

Page({

  /**
   * 页面的初始数据
   */
  data: {
    compositionId : 0,
    compositionUrl: '',
    compositionType: 0,
    compositionAngle: 0,
    objectCompositionAngle: {
      0: '',
      90: 'angle90',
      180: 'angle180',
      270: 'angle270'
    }
  },
  /**
 * 生命周期函数--监听页面加载
 */
  onLoad: function (options) {
    var tempComposition = JSON.parse(options.tempComposition);
    this.setData({
      compositionUrl: tempComposition.compositionUrl,
      compositionType: tempComposition.compositionType,
      compositionAngle: tempComposition.compositionAngle
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

  },
  rotate: function (e) {
    var temp = (this.data.compositionAngle + 90) % 360;
    this.setData({
      compositionAngle: temp
    })
    this.data.compositionAngle+90
  },
  choosePhotograph: function (e) {
    var that = this;
    wx.chooseImage({
      count: 1,
      sizeType: ['compress'],
      sourceType: ['album', 'camera'],
      success: function (res) {
        var tempFilesSize = res.tempFiles[0].size;
        if (tempFilesSize <= 5000000) {   //图片小于或者等于5M时 可以执行获取图片
          var tempFilePath = res.tempFilePaths[0]; //获取图片
          that.setData({
            compositionUrl: tempFilePath,
            compositionType: that.data.compositionType,
            compositionAngle: that.data.composition_angle
          });
          that.drawCanvas();
        } else {    //图片大于5M，弹出一个提示框
          wx.showToast({
            title: '上传图片不能大于5M!',  //标题
            icon: 'none'       //图标 none不使用图标，详情看官方文档
          })
        }
      },
    })
  },
  drawCanvas: function () {
    var that = this;
    const ctx = wx.createCanvasContext('attendCanvasId');
    ctx.drawImage(that.data.compositionUrl, 0, 0, 94, 96);
    ctx.draw();
    this.prodImageOpt();
    wx.canvasToTempFilePath({
      canvasId: 'attendCanvasId',
      success: function success(res) {
        that.setData({
          compositionUrl: res.tempFilePath
        });
      }
    });
  },
  toPreview: function () {
    var that = this;
    wx.showModal({
      title: '注意',
      content: '作品一经提交便不能修改，确认提交吗？',
      success(res) {
        if (res.confirm) {
          console.log('用户点击确定');
          that.uploadComposition()
        } else if (res.cancel) {
          console.log('用户点击取消');
        }
      }
    })
  },
  uploadComposition: function () {
    var that = this;
    wx.showToast({
      title: '正在上传...',
      icon: 'loading',
      mask: true,
      duration: 3000
    });
    var session_id = wx.getStorageSync('session_id');
    console.log(session_id);
    if (session_id) {
      wx.uploadFile({
        url: 'https://bugaboo.drivetogreen.com/user/composition/upload',
        filePath: that.data.compositionUrl,
        name: 'composition',
        header: {
          'Content-Type': 'multipart/form-data',
          'Session-Id': session_id,
        },
        formData: {
          'composition_type': that.data.gameGroupIndex,
          'composition_angle': that.data.composition_angle
        },
        success: function (res) {
          wx.hideToast();
          try {
            var response = JSON.parse(res.data);
            console.log(response);
            if (response.constructor === Object) {
              if (response.state) {
                wx.showToast({
                  title: '上传成功',
                  icon: 'success',
                  mask: true,
                  duration: 1500
                });
                that.setData({
                  compositionId: response.data.composition_id,
                })
                wx.navigateTo({
                  url: 'pages/preview/preview?composition_id=' + that.data.compositionId,
                })
              } else {
                wx.showToast({
                  title: '上传失败',
                  icon: 'none',
                  mask: true,
                  duration: 1500
                })
              }
            }
          }
          catch (e) {
            console.log(e);
          }
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
    } else {
      wx.showToast({
        title: '请重新打开小程序再试'
      })
    }

  }
})