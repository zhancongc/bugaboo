// pages/awardlist/awardlist.js
var util = require("../../utils/util.js");
var app = getApp();

Page({
  awardIndex: 0,
  //奖品配置
  awardsConfig: {
    chance: true,
    awards: [
      { 'index': 0, 'name': '谢谢参与' },
      { 'index': 1, 'name': '优惠券1' },
      { 'index': 2, 'name': '笔记本' },
      { 'index': 3, 'name': '优惠券2' },
      { 'index': 4, 'name': '保温杯' },
      { 'index': 5, 'name': '优惠券3' },
      { 'index': 6, 'name': '谢谢参与' }
    ]
  },

  data: {
    awardsList: {},
    animationData: {},
    btnDisabled: '',
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

  //发起抽奖
  playReward: function () {
    var that = this;
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
              that.setData({
                awardIndex: response.data.award_id
              })
              //中奖index
              var runNum = 8;//旋转8周
              var duration = 4000;//时长
              // 旋转角度
              that.runDeg = that.runDeg || 0;
              that.runDeg = that.runDeg + (360 - that.runDeg % 360) + (360 * runNum - that.data.awardIndex * (360 / 7))
              var sessionId = wx.getStorageSync('sessionId');
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
