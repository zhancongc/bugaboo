// pages/composition/composition.js
const app = getApp()

Page({
  /**
   * 页面的初始数据
   */
  data: {
    compositionSrc: '',
    compositionType: 0,
    compositionAngle: 0,
    compositionDescription: '',
    objectCompositionAngle: {
      0: '',
      90: 'angle90',
      180: 'angle180',
      270: 'angle270'
    }
  },
  rotate: function (e) {
    console.log('旋转了90度');
    var temp = (this.data.compositionAngle + 90) % 360;
    this.setData({
      compositionAngle: temp
    });
  },
  setDescription: function (e) {
    console.log(e.detail.value);
    this.setData({
      compositionDescription: e.detail.value
    })
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
      title: '上传中...',
      icon: 'loading',
      mask: true,
      duration: 20000
    });
    var sessionId = app.globalData.sessionId;
    if (sessionId) {
      wx.uploadFile({
        url: 'https://bugaboo.drivetogreen.com/user/composition/upload',
        filePath: that.data.compositionSrc,
        name: 'composition',
        header: {
          'Content-Type': 'multipart/form-data',
          'Session-Id': sessionId,
        },
        formData: {
          'composition_type': that.data.compositionType,
          'composition_angle': that.data.compositionAngle,
          'composition_msg': that.data.compositionDescription
        },
        success: function (res) {
          wx.hideToast();
          try {
            var response = JSON.parse(res.data);
            console.log(response);
            if (response.constructor === Object) {
              if (response.state===1) {
                wx.showToast({
                  title: '上传成功',
                  icon: 'success',
                  mask: true,
                  duration: 1500
                });
                that.setData({
                  compositionId: response.data.composition_id,
                })
                console.log('composition_id', that.data.compositionId);
                wx.navigateTo({
                  url: '/pages/preview/preview',
                })
              } else if (response.state == 2) {
                wx.showToast({
                  title: '您已经上传过作品了',
                  icon: 'none',
                  mask: true,
                  duration: 1500
                });
                wx.navigateTo({
                  url: '/pages/preview/preview',
                })
              } else  {
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
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var tempComposition = JSON.parse(options.tempComposition);
    this.setData({
      compositionSrc: tempComposition.compositionSrc,
      compositionType: tempComposition.compositionType
    });
    console.log('compositionType', this.data.compositionType);
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
  }
})