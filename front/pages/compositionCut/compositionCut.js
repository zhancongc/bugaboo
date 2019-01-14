/**
 * Created by sail on 2017/6/1.
 */

import WeCropper from '../we-cropper/we-cropper.js'
const device = wx.getSystemInfoSync()

Page({
  data: {
    wrapper: false,
    visible1: false,
    modalTitle: '上传规则',
    rotateI: 0,
    compositionSrc: '',
    gameGroupIndex: 0,
    selected: 1, // 1 bugaboo用户， 0不是
    cropperOpt: {
      id: 'cropper',
      rotateI: 0,
      width: device.windowWidth,
      height: device.windowWidth,
      scale: 2.5,
      zoom: 8
    }
  },
  handleOpen1: function() {
    this.setData({
      visible1: true
    })
  },
  handleClose1: function() {
    this.setData({
      visible1: false
    })
  },
  select: function (e) {
    var that = this;
    var temp = e.currentTarget.dataset.selected;
    if (that.data.selected !== parseInt(temp)) {
      that.setData({
        selected: parseInt(e.currentTarget.dataset.selected)
      })
    }
  },
  choosePhotograph: function (e) {
    var that = this;
    wx.chooseImage({
      count: 1,
      sizeType: ['compress'],
      sourceType: ['album', 'camera'],
      success: function (res) {
        var tempFilesSize = res.tempFiles[0].size;
        if (tempFilesSize <= 5000000) {   //图片小于或者等于5M时 可以执行获取图片
          var tempFilePath = res.tempFilePaths[0]; //获取图片
          var tempComposition = {
            compositionUrl: tempFilePath,
            compositionType: that.data.selected
          };
          wx.navigateTo({
            url: '/pages/compositionCut/compositionCut?tempComposition=' + JSON.stringify(tempComposition)
          })
        } else {    //图片大于5M，弹出一个提示框
          wx.showToast({
            title: '上传图片不能大于5M!',  //标题
            icon: 'none'       //图标 none不使用图标，详情看官方文档
          })
        }
      },
    })
  },
  touchStart(e) {
    this.wecropper.touchStart(e)
  },
  touchMove(e) {
    this.wecropper.touchMove(e)
  },
  touchEnd(e) {
    this.wecropper.touchEnd(e)
  },
  getCropperImage() {
    var that = this;
    this.wecropper.getCropperImage((src) => {
      if (src) {
        console.log(src);
        that.setData({
          compositionSrc: src
        })
        var tempComposition = JSON.stringify({
          compositionSrc: that.data.compositionSrc,
          compositionType: that.data.selected
        });
        wx.navigateTo({
          url: '/pages/composition/composition?tempComposition=' + tempComposition,
        })
      } else {
        console.log('获取图片地址失败，请稍后重试')
      }
    })
  },
  uploadTap() {
    const self = this;
    wx.chooseImage({
      count: 1, // 默认9
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success(res) {
        self.handleClose1();
        const src = res.tempFilePaths[0];
        self.wecropper.pushOrign(src);
        self.setData({
          wrapper: true
        })
      },
    })
  },
  // 图片旋转
  rotateImg() {
    const self = this;
    let rotateI = this.data.rotateI + 1;
    this.setData({
      rotateI: rotateI
    })
    // 将旋转的角度传递给插件
    self.wecropper.updateCanvas(rotateI)
  },
  onLoad(options) {
    const { cropperOpt } = this.data;
    new WeCropper(cropperOpt)
      .on('ready', function (ctx) {
        console.log(`wecropper is ready for work!`)
      })
      .on('beforeImageLoad', (ctx) => {
        console.log(`before picture loaded, i can do something`)
        console.log(`current canvas context:`, ctx)
        wx.showToast({
          title: '上传中',
          icon: 'loading',
          duration: 20000
        })
      })
      .on('imageLoad', (ctx) => {
        console.log(`picture loaded`)
        console.log(`current canvas context:`, ctx)
        wx.hideToast()
      })
  }
})
