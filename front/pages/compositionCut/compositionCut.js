/**
 * Created by sail on 2017/6/1.
 */

import WeCropper from '../we-cropper/we-cropper.js'
const device = wx.getSystemInfoSync()

Page({
  data: {
    wrapper: false,
    compositionSrc: '',
    compositionType: 0,
    gameGroupIndex: 0,
    gameGroup: ['非婴儿车组', '婴儿车组'],
    objectGameGroup: [{
      0: '非婴儿车组'
    }, {
      1: '婴儿车组'
    }],
    cropperOpt: {
      id: 'cropper',
      width: device.windowWidth,
      height: device.windowWidth,
      scale: 2.5,
      zoom: 8
    }
  },
  bindPickerChange: function (e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      gameGroupIndex: e.detail.value
    })
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
            compositionType: that.data.gameGroupIndex
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
        wx.previewImage({
          current: '', // 当前显示图片的http链接
          urls: [src] // 需要预览的图片http链接列表
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
        const src = res.tempFilePaths[0];
        self.wecropper.pushOrign(src);
        self.setData({
          wrapper: true
        })
      }
    })
  },
  onLoad(options) {
    /*
    var tempComposition = JSON.parse(options.tempComposition);
    this.setData({
      compositionUrl: tempComposition.compositionUrl,
      compositionType: tempComposition.compositionType
    });
    */
    const { cropperOpt } = this.data.cropperOpt;
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
