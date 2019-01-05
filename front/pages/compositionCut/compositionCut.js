/**
 * Created by sail on 2017/6/1.
 */

import WeCropper from '../we-cropper/we-cropper.js'
const device = wx.getSystemInfoSync()

Page({
  data: {
    wrapper: false,
    rotateI: 0,
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
      rotateI: 0,
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
        /*
        wx.previewImage({
          current: '', // 当前显示图片的http链接
          urls: [src] // 需要预览的图片http链接列表
        })*/
        var tempComposition = JSON.stringify({
          compositionSrc: this.data.compositionSrc,
          compositionType: this.data.compositionType
        });
        wx.navigateTo({
          url: '/pages/composition/composition?tempComposition=' + tempComposition,
        })
      } else {
        console.log('获取图片地址失败，请稍后重试')
      }
    })
  },
  uploadComposition: function () {
    var that = this;
    wx.showToast({
      title: '正在上传...',
      icon: 'loading',
      mask: true,
      duration: 10000
    });
    var sessionId = app.globalData.sessionId;
    if (sessionId) {
      wx.uploadFile({
        url: 'https://bugaboo.drivetogreen.com/user/composition/upload',
        filePath: that.data.compositionUrl,
        name: 'composition',
        header: {
          'Content-Type': 'multipart/form-data',
          'Session-Id': sessionId,
        },
        formData: {
          'composition_type': that.data.compositionType,
          'composition_angle': that.data.rotateI
        },
        success: function (res) {
          wx.hideToast();
          try {
            var response = JSON.parse(res.data);
            console.log(response);
            if (response.constructor === Object) {
              if (response.state) {
                wx.showToast({
                  title: '上传成功',
                  icon: 'success',
                  mask: true,
                  duration: 1500
                });
                that.setData({
                  compositionId: response.data.compositionId,
                })
                console.log('composition_id', that.data.compositionId);
                wx.navigateTo({
                  url: '/pages/preview/preview?composition_id=' + that.data.compositionId,
                })
              } else {
                wx.showToast({
                  title: '上传失败',
                  icon: 'none',
                  mask: true,
                  duration: 1500
                })
              }
            }
          }
          catch (e) {
            console.log(e);
          }
        },
        fail: function (res) {
          wx.hideToast();
          wx.showToast({
            title: '上传失败',
            duration: 1000
          })
        },
        complete: function (res) { },
      })
    } else {
      wx.showToast({
        title: '请重新打开小程序再试'
      })
    }
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
