// pages/awardlist/awardlist.js
var util = require("../../utils/util.js");
var app = getApp();

Page({

  //奖品配置
  awardsConfig: {
    chance: true,
    awards: [
      { 'index': 0, 'name': '谢谢参与' },
      { 'index': 1, 'name': '优惠券1' },
      { 'index': 2, 'name': '笔记本' },
      { 'index': 3, 'name': '优惠券2' },
      { 'index': 4, 'name': '保温杯' },
      { 'index': 5, 'name': '优惠券3' }
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
    //中奖index
    var awardIndex = 4;
    var runNum = 8;//旋转8周
    var duration = 4000;//时长

    // 旋转角度
    this.runDeg = this.runDeg || 0;
    this.runDeg = this.runDeg + (360 - this.runDeg % 360) + (360 * runNum - awardIndex * (360 / 6))
    //创建动画
    var animationRun = wx.createAnimation({
      duration: duration,
      timingFunction: 'ease'
    })
    animationRun.rotate(this.runDeg).step();
    this.setData({
      animationData: animationRun.export(),
      btnDisabled: 'disabled'
    });

    // 中奖提示
    var awardsConfig = this.awardsConfig;
    setTimeout(function () {
      wx.showModal({
        title: '恭喜',
        content: '获得' + (awardsConfig.awards[awardIndex].name),
        showCancel: false
      });
      this.setData({
        btnDisabled: ''
      });
    }.bind(this), duration);
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
