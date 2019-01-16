// pages/awardlist/awardlist.js
var util = require("../../utils/util.js");
var app = getApp();

Page({
  data: {
    visible1: false,
    awardIndex: 0,
    raffling: false,
    raffleTimes: 0,
    awardName: {
      1: 'bugaboo限量笔记本',
      2: '50元天猫商城代金券',
      3: 'bugaboo定制保温杯',
      4: '100元天猫商城代金券',
      5: 'bugaboo限量定制健身包'
    },
    awardImage: {
      1: 'https://bugaboo.drivetogreen.com/static/images/award_notebook.png',
      2: 'https://bugaboo.drivetogreen.com/static/images/award_coupon_50.png',
      3: 'https://bugaboo.drivetogreen.com/static/images/award_bottle.png',
      4: 'https://bugaboo.drivetogreen.com/static/images/award_coupon_100.png',
      5: 'https://bugaboo.drivetogreen.com/static/images/award_bag.png'
    },
    awardsList: {},
    animationData: {}
  },
  onShow: function() {
    var that = this;
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/raffle/times',
      method: 'get',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': app.globalData.sessionId
      },
      success: function (res) {
        try {
          var response = res.data;
          console.log(response);
          if (response.constructor === Object) {
            if (response.state === 1) {
              that.setData({
                raffleTimes: response.data.raffle_times
              });
              app.globalData.raffleTimes = response.data.raffleTimes
            }
          }
        } catch (e) {
          console.log(e);
        }
      },
      fail: function (res) {
        wx.showToast({
          title: '请稍后重新再试',
        });
      }
    })
  },
  onReady: function (e) {
    //禁止分享
    wx.showShareMenu({
      withShareTicket: false
    });
  },
  raffle: function() {
    var that = this;
    //中奖index
    var runNum = 8;//旋转8周
    var duration = 4000;//时长
    // 旋转角度
    that.runDeg = that.runDeg || 0;
    that.runDeg = that.runDeg + (360 - that.runDeg % 360) + (360 * runNum - that.data.awardIndex * (360 / 6))
    //创建动画
    var animationRun = wx.createAnimation({
      duration: duration,
      timingFunction: 'ease'
    })
    animationRun.rotate(that.runDeg).step();
    that.setData({
      animationData: animationRun.export()
    });

    // 中奖提示
    setTimeout(function () {
      that.handleOpen1();
    }.bind(that), duration);
  },
  //发起抽奖
  playReward: function () {
    var that = this;
    if (!that.data.raffling && that.data.raffleTimes>0) {
      that.setData({
        raffling: true
      });
      wx.request({
        url: 'https://bugaboo.drivetogreen.com/raffle',
        method: 'get',
        header: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Session-Id': app.globalData.sessionId
        },
        success: function (res) {
          try {
            var response = res.data;
            console.log(response);
            if (response.constructor === Object) {
              if (response.state === 1) {
                that.data.raffleTimes -= 1;
                that.setData({
                  raffleTimes: that.data.raffleTimes,
                  awardIndex: response.data.award_id
                })
                that.raffle();
                that.setData({
                  raffling: false
                });
              }
            }
          } catch (e) {
            console.log(e);
          }
        },
        fail: function (res) {
          wx.showToast({
            title: '请稍后重新再试',
          });
          that.setData({
            raffling: false
          });
        }
      })
    } else {
      wx.showModal({
        title: '提示',
        content: '您没有抽奖次数',
      })
    }
  },
  handleOpen1: function () {
    this.setData({
      visible1: true
    })
  },
  handleClose1: function() {
    this.setData({
      visible1: false
    })
  },
  toIndex: function() {
    wx.navigateTo({
      url: '/pages/index/index',
    })
  },
  toAwardList: function(){
    this.handleClose1();
    wx.navigateTo({
      url: '/pages/awardlist/awardlist',
    })
  }
})
