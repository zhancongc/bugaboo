// pages/awardlist/awardlist.js
var util = require("../../utils/util.js");
var app = getApp();

Page({
  //奖品配置
  awardsConfig: {
    raffleTimes: 0,
    chance: true,
    awards: [
      { 'index': 0, 'name': '谢谢参与', 'image': 'https://bugaboo.drivetogreen.com/static/images/bg_prize.png' },
      { 'index': 1, 'name': '定制保温杯', 'image': '' },
      { 'index': 2, 'name': '限量笔记本', 'image': '' },
      { 'index': 3, 'name': '限量定制健身包', 'image': '' },
      { 'index': 4, 'name': '50元代金券', 'image': '' },
      { 'index': 5, 'name': '100元代金券', 'image': '' }
    ]
  },

  data: {
    awardIndex: 0,
    awardsList: {},
    animationData: {},
    btnDisabled: '',
  },
  onShow: function() {
    var that = this;
    that.setData({
      raffleTimes: app.globalData.raffleTimes
    })
  },
  onReady: function (e) {
    this.drawAwardRoundel();

    //分享
    wx.showShareMenu({
      withShareTicket: true
    });
  },

  //画抽奖圆盘
  drawAwardRoundel: function () {
    var awards = this.awardsConfig.awards;
    var awardsList = [];
    var turnNum = 1 / awards.length;  // 文字旋转 turn 值

    // 奖项列表
    for (var i = 0; i < awards.length; i++) {
      awardsList.push({ turn: i * turnNum + 'turn', lineTurn: i * turnNum + turnNum / 2 + 'turn', award: awards[i].name });
    }

    this.setData({
      btnDisabled: this.awardsConfig.chance ? '' : 'disabled',
      awardsList: awardsList
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
      animationData: animationRun.export(),
      btnDisabled: 'disabled'
    });

    // 中奖提示
    var awardsConfig = that.awardsConfig;
    setTimeout(function () {
      wx.showModal({
        title: '恭喜',
        content: '获得' + (awardsConfig.awards[that.data.awardIndex].name),
        showCancel: false
      });
      that.setData({
        btnDisabled: ''
      });
    }.bind(that), duration);
  },
  //发起抽奖
  playReward: function () {
    var that = this;
    if (app.globalData.raffleTimes>0) {
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
                app.globalData.raffleTimes -= 1;
                that.setData({
                  raffleTimes: app.globalData.raffleTimes,
                  awardIndex: response.data.award_id
                })
                that.raffle();
              }
            }
          } catch (e) {
            console.log(e);
          }
        },
        fail: function (res) {
          wx.showToast({
            title: '请稍后重新再试',
          })
        }
      })
    } else {
      wx.showModal({
        title: '提示',
        content: '您没有抽奖次数',
      })
    }
  },
  toIndex: function() {
    wx.navigateTo({
      url: '/pages/index/index',
    })
  },
  toAwardList: function(){
    wx.navigateTo({
      url: '/pages/awardlist/awardlist',
    })
  }
})
