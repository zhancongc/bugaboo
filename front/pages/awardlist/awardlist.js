// pages/awardlist/awardlist.js
const app = getApp()
Page({
  /**
   * 页面的初始数据
   */
  data: {
    /*{ "awardrecord_id": 1, "awardrecord_type": 1, "award_name": "bugaboo限量笔记本", "award_image": "https://bugaboo.drivetogreen.com/static//images/award_bottle.png", "award_time": "2019/01/12 12:00", 'checked': false, 'informed': false }*/
    awards: []
  },

  getAwardList : function () {
    var that = this;
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/user/award/list',
      method: 'get',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': app.globalData.sessionId
      },
      success: function (res) {
        var response = res.data;
        console.log(response);
        if (response.constructor === Object) {
          if (response.state) {
            if (response.data) {
              var awardList = [];
              for (var i in response.data) {
                awardList.push({
                  'awardrecord_id': response.data[i].awardrecord_id,
                  'awardrecord_type': response.data[i].awardrecord_type,
                  'award_image': response.data[i].award_image,
                  'award_name': response.data[i].award_name,
                  'award_time': response.data[i].award_time,
                  'informed': response.data[i].informed,
                  'checked': response.data[i].checked
                })
              }
              that.setData({
                awards: awardList
              })
            }
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
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    that.getAwardList();
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {},

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {},

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {},

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
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
            if (response.state == 1) {
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

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {},

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {  },
  toInform: function (e) {
    console.log(e.target.dataset.awardrecord_info);
    wx.navigateTo({
      url: '/pages/inform/inform?awardrecord_id=' + e.target.dataset.awardrecord_info[0] +'&awardrecord_type='+e.target.dataset.awardrecord_info[1],
    })
  },
  toAward: function (e) {
    console.log(e.target.dataset);
    wx.navigateTo({
      url: '/pages/award/award?awardrecord_id=' + e.target.dataset.awardrecord_id,
    })
  }
})