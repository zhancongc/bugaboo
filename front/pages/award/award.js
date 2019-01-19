// pages/award/award.js
const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    awardrecordId: 0,
    awardName: '',
    qrcode: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    that.setData({
      awardrecordId: options.awardrecord_id
    });
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function (e) {
    //禁止分享
    wx.showShareMenu({
      withShareTicket: false
    });
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
    console.log('请求奖品信息');
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/user/award',
      method: 'post',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': app.globalData.sessionId
      },
      data: {
        awardrecord_id: that.data.awardrecordId
      },
      success: function (res) {
        wx.hideToast();
        var response = res.data;
        console.log(response);
        if (response.constructor === Object) {
          if (response.state==1) {
            that.setData({
              awardName: response.data.award_name,
              qrcode: response.data.qrcode_image_url
            })
          } else {
            wx.showToast({
              title: '请稍后重试',
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
  toAwardList: function () {
    wx.navigateTo({
      url: '/pages/awardlist/awardlist',
    })
  },
  toIndex: function () {
    wx.navigateTo({
      url: '/pages/index/index',
    })
  },
  preview : function (e) {
    var that = this;
    wx.getSetting({
      success(res) {
        if (!res.authSetting['scope.writePhotosAlbum']) {
          wx.authorize({
            scope: 'scope.writePhotosAlbum',
            success() {
              console.log('授权成功')
            },
            fail() {
              wx.showModal({
                title: '提示',
                content: '请开启授权',
              })
            }
          })
        }
        var imgSrc = that.data.qrcode;
        wx.downloadFile({
          url: imgSrc,
          success: function (res) {
            console.log(res);
            //图片保存到本地
            wx.saveImageToPhotosAlbum({
              filePath: res.tempFilePath,
              success: function (data) {
                wx.showToast({
                  title: '保存成功',
                  icon: 'success',
                  duration: 2000
                })
              },
              fail: function (err) {
                console.log(err);
              }
            })
          }
        })
      }
    })
    /*
    wx.previewImage({
      current: that.data.qrcode,
      urls: [that.data.qrcode],
    })
    */
  }
})