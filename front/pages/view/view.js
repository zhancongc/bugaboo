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
    canFollow: false,
    followTimes: 0,
    avatarList: [{
      avatarUrl: 'https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiboeh23vhCNueUvhwibepopNhqzTNjPB7EhcosK1bnicKFHUicB0DODnD6FwgYAmayLoeL82DmoicBibQ/132'
    }]
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
            if (response.state) {
              that.setData({
                authorId: response.data.user_id,
                nickName: response.data.nickName,
                avatarUrl: response.data.avatarUrl,
                compositionId: response.data.composition_id,
                compositionUrl: response.data.composition_url,
                compositionType: response.data.composition_type,
                canFollow: response.data.can_follow,
                avatarList: response.data.followers,
                followTimes: response.data.follow_times
              })
            } else {
              wx.showToast({
                title: '获取作品失败，请稍后重试',
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
      title: this.data.nickName + '的Bugaboo新年祝福',
      imageUrl: this.data.compositionUrl,
      path: 'pages/view/view?composition_id=' + this.data.compositionId,
      success: (res) => { },
      fail: (res) => { }
    }
  },
  followOwner:function () {
    var that = this;
    var canFollow = app.globalData.canFollow;
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
              app.globalData.canFollow = true;
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
    if (that.data.authorId == app.globalData.userId) {
      wx.showModal({
        title: '提示',
        content: '不能给自己祝福',
      });
      return ;
    }
    var canFollow = that.data.canFollow;
    if (canFollow) {
      that.followOwner();
    } else {
      wx.showModal({
        title: '提示',
        content: '一个作品你只能祝福一次',
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
  toRankingList1: function() { 
    var that = this;
    wx.navigateTo({
      url: '/pages/rankinglist/rankinglist?composition_type='+that.data.compositionType,
    })
  },
  toRankingList2: function () {
    var that = this;
    wx.navigateTo({
      url: '/pages/rankinglist/rankinglist?composition_type=' + that.data.compositionType + '&tab=' + 'tab2',
    })
  },
  getUserInfo: function (e) {
    var that = this;
    var userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      that.handleOpen1();
    } else {
      console.log(e.detail.userInfo)
      if (e.detail.userInfo) {
        //用户按了授权按钮
        console.log('用户按了授权按钮');
        app.globalData.canUploadUserInfo = true;
        that.saveUserInfo(userInfo);
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
            console.log(response.msg)
          }
          app.globalData.canUploadUserInfo = false;
          wx.setStorage({
            key: 'userInfo',
            data: userInfo,
          });
        } catch (e) {
          console.log(e);
        }
      }
    })
  }
});


