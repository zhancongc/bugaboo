// pages/preview/pewview.js
const { $Message } = require('../../dist/base/index');
const { $Toast } = require('../../dist/base/index');
const app = getApp()

Page({
  /**
   * 页面的初始数据
   */
  data: {
    visible1: false,
    authorId: 0,
    nickName: '',
    avatarUrl: '',
    compositionId: 0,
    compositionUrl: '',
    compositionType: 0,
    followTimes: 0
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    if (options.hasOwnProperty('composition_id')) {
      var sessionId = app.globalData.sessionId;
      console.log('请求作品信息', sessionId);
      wx.request({
        url: 'https://bugaboo.drivetogreen.com/user/composition',
        method: 'post',
        header: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Session-Id': sessionId
        },
        data: {
          composition_id: options.composition_id
        },
        success: function (res) {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            var viewer;
            if (response.state) {
              that.setData({
                authorId: response.data.user_id,
                nickName: response.data.nickName,
                avatarUrl: response.data.avatarUrl,
                compositionId: response.data.composition_id,
                compositionUrl: response.data.composition_url,
                compositionType: response.data.composition_type
              })
            } else {
              wx.showToast({
                title: '获取助力作品失败，请稍后重试',
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
    } else {
      wx.showToast({
        title: '获取不到作品信息',
        icon: 'none',
        mask: true,
        duration: 1000
      });
      wx.navigateTo({
        url: '/pages/index/index',
      })
    }
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
    // 首先获取user_id和composition_id
    return {
      title: this.data.nickName + '的Bugaboo助力作品',
      imageUrl: this.data.compositionUrl,
      path: 'pages/view/view?composition_id=' + this.data.compositionId,
      success: (res) => { },
      fail: (res) => { }
    }
  },
  handleOpen1() {
    var that = this;
    var canFollow = wx.getStorageSync('canFollow');
    if (canFollow){
      var sessionId = app.globalData.sessionId;
      wx.request({
        url: 'https://bugaboo.drivetogreen.com/user/follow',
        method: 'post',
        data: { composition_id: this.data.compositionId },
        header: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Session-Id': sessionId
        },
        success: function (res) {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            if (response.state == 1){
              wx.setStorage({
                key: 'canFollow',
                data: true,
              });
              that.setData({
                visible1: true
              });
            } else if (response.state == 2) {
              $Toast({
                content: '不能给自己送祝福',
                type: 'warning'
              });
            } else {
              $Toast({
                content: response.msg,
                type: 'error'
              });
            }
          }
        },
        fail: function(res) {
          $Toast({
            content: '请稍后重新打开小程序再试',
            type: 'error'
          });
        }
      })
    }else {
      $Toast({
        content: '每个用户只能送一次祝福',
        type: 'warning'
      });
    }
  },
  handleClick({ detail }) {
    this.setData({
      visible3: false
    });
  },
  handleOpen1: function () {
    var that = this;
    var canFollow = wx.getStorageSync('canFollow');
    if (canFollow) {
      if (app.globalData.userId === that.data.authorId) {
        wx.showModal({
          title: '提示',
          content: '不能给自己祝福',
        })
      } else {
        that.setData({
          visible1: true
        });
      }
    } else {
      wx.showModal({
        title: '提示',
        content: '您没有抽奖次数',
      })
    }
  },
  handleClose1: function() {
    this.setData({
      visible1: false
    });
  },
  toIndex: function () {
    wx.navigateTo({
      url: '/pages/index/index',
    })
  },
  toAuthorize: function () {
    wx.navigateTo({
      url: '/pages/authorize/authorize',
    })
  },
  toRankingList: function() {
    wx.navigateTo({
      url: '/pages/rankinglist/rankinglist',
    })
  },
  getUserInfo: function (e) {
    var that = this;
    if (app.globalData.userInfo) {
      that.handleOpen1();
    } else {
      console.log(e.detail.userInfo)
      if (e.detail.userInfo) {
        //用户按了授权按钮
        wx.setStorageSync('userInfo', e.detail.userInfo);
        app.globalData.canUploadUserInfo = true;
        that.saveUserInfo(e.detail.userInfo);
        that.handleOpen1();
      } else {
        //用户按了拒绝按钮
        wx.showToast({
          icon: 'none',
          title: '请点击授权',
          mask: true,
          duration: 1000
        })
      }
    }
  },
  saveUserInfo: function (userInfo) {
    var sessionId = app.globalData.sessionId;
    console.log('把用户信息发送到后端存储起来');
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/user/info/upload',
      method: 'post',
      data: {
        avatarUrl: userInfo.avatarUrl,
        city: userInfo.city,
        country: userInfo.country,
        gender: userInfo.gender,
        language: userInfo.language,
        nickName: userInfo.nickName,
        province: userInfo.province
      },
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': sessionId
      },
      success: function (res) {
        try {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            if (response.state) {
              console.log(response.msg);
            } else {
              console.log(response.msg)
            }
          }
          app.globalData.canUploadUserInfo = false;
        } catch (e) {
          console.log(e);
        }
      }
    })
  }
});


