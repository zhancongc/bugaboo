// pages/inform/inform.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    receiver: '',
    storeId: 0,
    phone: '',
    address: '',
    compositionId: 0,
    compositionType: 0,
    storeIndex: 0,
    storeArray: ['请先选择城市'],
    cityIndex: 0,
    cityArray: ['请选择城市', '上海', '北京', '成都', '深圳', '广州', '天津', '郑州', '沈阳', '宁波','苏州', '杭州', '合肥', '重庆', '江阴', '武汉', '哈尔滨', '长沙', '长春', '青岛', '南京', '无锡', '大连', '西安', '南宁'],
    objectArray: [
      {
        id: 0, name: '请选择城市', store: [],
      },
      {
        id: 1, name: '上海', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 1, store_name: '上海古北门店' },
          { store_id: 2, store_name: '上海华山路门店' },
          { store_id: 3, store_name: '上海浦东嘉里城' },
          { store_id: 4, store_name: '上海静安嘉里中心' },
          { store_id: 5, store_name: '上海港汇恒隆广场' },
          { store_id: 6, store_name: '上海月星环球港' },
          { store_id: 7, store_name: '上海合生汇商场' },
          { store_id: 8, store_name: '上海万象城' },
          { store_id: 9, store_name: '上海丁香国际' }
        ]
      },
      {
        id: 2, name: '北京', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 10, store_name: '北京将台路门店' },
          { store_id: 11, store_name: '北京朝阳大悦城' },
          { store_id: 12, store_name: '北京金源新燕莎' },
          { store_id: 13, store_name: '北京侨福芳草地' },
          { store_id: 14, store_name: '北京荟聚购物中心' },
          { store_id: 15, store_name: '北京华润五彩城' },
          { store_id: 16, store_name: '北京蓝色港湾商区' },
          { store_id: 17, store_name: '北京顺义店' }
        ]
      },
      {
        id: 3, name: '成都', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 18, store_name: '成都新世纪环球中心' },
          { store_id: 19, store_name: '成都IFS' },
          { store_id: 20, store_name: '成都银泰In99' },
          { store_id: 21, store_name: '成都大悦城' },
          { store_id: 22, store_name: '成都悠方店' },
          { store_id: 23, store_name: '成都金牛凯德广场' }
        ]
      },
      {
        id: 4, name: '深圳', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 24, store_name: '深圳万象城' },
          { store_id: 25, store_name: '深圳万象天地' }]
      },
      {
        id: 5, name: '广州', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 26, store_name: '广州IGC天汇广场' }
        ]
      },
      {
        id: 6, name: '天津', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 27, store_name: '天津奥城门店' },
          { store_id: 28, store_name: '天津鲁能城店' }]
      },
      {
        id: 7, name: '郑州', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 29, store_name: '郑州丹尼斯大卫城' },
          { store_id: 30, store_name: '郑州丹尼斯三天地' }]
      },
      {
        id: 8, name: '沈阳', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 31, store_name: '沈阳万象城' }]
      },
      {
        id: 9, name: '宁波', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 32, store_name: '宁波和义大道购物中心' }]
      },
      {
        id: 10, name: '苏州', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 33, store_name: '苏州圆融星空广场' },
          { store_id: 34, store_name: '苏州高铁新城圆融广场' },
          { store_id: 35, store_name: '苏州久光百货' }]
      },
      {
        id: 11, name: '杭州', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 36, store_name: '杭州大厦' },
          { store_id: 37, store_name: '杭州万象城' },
          { store_id: 38, store_name: '杭州万象汇' },
          { store_id: 39, store_name: '杭州嘉里中心' },
          { store_id: 40, store_name: '杭州大悦城' }]
      },
      {
        id: 12, name: '合肥', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 41, store_name: '合肥银泰中心' }]
      },
      {
        id: 13, name: '重庆', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 42, store_name: '重庆时代广场' },
          { store_id: 43, store_name: '重庆IFS' }]
      },
      {
        id: 14, name: '江阴', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 44, store_name: '江阴新一城商业广场' }]
      },
      {
        id: 15, name: '武汉', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 45, store_name: '武汉万达广场' },
          { store_id: 46, store_name: '武汉K11' }]
      },
      {
        id: 16, name: '哈尔滨', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 47, store_name: '哈尔滨卓展购物中心' }]
      },
      {
        id: 17, name: '长沙', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 48, store_name: '长沙国金中心' }]
      },
      {
        id: 18, name: '长春', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 49, store_name: '长春卓展购物中心' }]
      },
      {
        id: 19, name: '青岛', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 50, store_name: '青岛华润万象城' }]
      },
      {
        id: 20, name: '南京', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 51, store_name: '南京德基广场' }]
      },
      {
        id: 21, name: '无锡', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 52, store_name: '无锡恒隆广场' }]
      },
      {
        id: 22, name: '大连', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 53, store_name: '大连恒隆广场' }]
      },
      {
        id: 23, name: '西安', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 54, store_name: '西安中大国际商业中心' },
          { store_id: 55, store_name: '西安中大国际店' }]
      },
      {
        id: 24, name: '南宁', store: [
          { store_id: 0, store_name: '请选择门店' },
          { store_id: 56, store_name: '南宁万象城' }]
      }
    ]
  },
  bindCityPickerChange(e) {
    console.log('picker发送选择改变，携带值为', e.detail.value);
    if (e.detail.value){
      var stores= this.data.objectArray[e.detail.value].store;
      var temp = [];
      for(var i in stores) {
        temp.push(stores[i].store_name)
      }
      console.log('store_names: ', temp);
      this.setData({
        cityIndex: e.detail.value,
        storeArray: temp
      });
    } else {
      this.setData({
        cityIndex: e.detail.value,
        storeArray: ['请先选择城市']
      });
    }
  },
  bindStorePickerChange(e) {
    var that = this;
    if (that.data.cityIndex) {
      console.log('picker发送选择改变，携带值为', e.detail.value)
      console.log('store object', that.data.objectArray[that.data.cityIndex].store[e.detail.value].store_id);
      that.setData({
        storeIndex: e.detail.value,
        storeId: that.data.objectArray[that.data.cityIndex].store[e.detail.value].store_id
      })
    } else {
      wx.showModal({
        title: '提示',
        content: '请先选择城市',
      })
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    console.log(options);
    that.setData({
      awardrecordId: options.awardrecord_id,
      awardrecordType: options.awardrecord_type
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
  setName: function (e) {
    console.log(e.detail.value);
    this.setData({
      receiver: e.detail.value
    })
  },
  setPhone: function (e) {
    console.log(e.detail.value);
    this.setData({
      phone: e.detail.value
    })
  },
  setAddress: function (e) {
    console.log(e.detail.value);
    this.setData({
      address: e.detail.value
    })
  },
  commit: function(){
    //检查信息是否完整
    var that = this;
    if (that.data.receiver) {
      console.log(that.data.receiver);
    } else {
      wx.showModal({
        title: '提示',
        content: '姓名不能为空',
      });
      return ;
    }
    if (that.data.phone && that.data.phone !== '0' && that.data.phone.length === 11) {
      console.log(that.data.phone);
    } else {
      wx.showModal({
        title: '提示',
        content: '请填写正确中国大陆手机号',
      });
      return ;
    }
    if (that.data.awardrecorydpe == 1 || that.data.awardrecordType == 2 || that.data.address) {
        console.log(that.data.storeId);
    } else {
      wx.showModal({
        title: '提示',
        content: '门店信息不能为空',
      });
      return;
    }
    if (that.data.awardrecorydpe == 3 || that.data.awardrecordType == 4 || that.data.storeId) {
      if (that.data.cityIndex && that.data.storeIndex) {
        console.log(that.data.storeId);
      } else {
        wx.showModal({
          title: '提示',
          content: '门店信息不能为空',
        });
        return ;
      }
    }
    that.inform();
  },
  inform: function(){
    var that = this;
    wx.request({
      url: 'https://bugaboo.drivetogreen.com/user/award/inform',
      method: 'post',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Session-Id': sessionId
      },
      data: {
        awardrecord_id: that.data.awardrecordId,
        receiver: that.data.receiver,
        phone: that.data.phone,
        store_id: that.data.storeId,
        address: that.data.address
      },
      success: function (res) {
        wx.hideToast();
        var response = res.data;
        console.log(response);
        if (response.constructor === Object) {
          var viewer;
          if (response.state) {
            wx.showToast({
              title: '提交成功',
              icon: 'none',
              mask: true,
              duration: 1000
            });
            if (that.data.awardrecordType == 1) {
              wx.navigateTo({
                url: '/pages/express/express',
              })
            } else if (that.data.awardrecordType > 1) {
              wx.navigateTo({
                url: '/pages/award/award?awardrecord_id='+that.data.awardrecordId,
              })
            } 
          } else {
            wx.showToast({
              title: '提交失败，请稍后重试',
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
  }
})