/**
 * Created by sail on 2017/6/1.
 */
import WeCropper from '../we-cropper/we-cropper.js'

const app = getApp()
const device = wx.getSystemInfoSync()
const width = device.windowWidth
const pixelRatio = device.pixelRatio

Page({
  data: {
    cropperOpt: {
      compositionUrl: '',
      compositionType: 0,
      id: 'cropper',
      themeColor: '#04b00f',
      width,
      scale: 2.5,
      zoom: 8,
      cut: {
        x: (width - 300) / 2,
        width: 300,
        height: 300
      },
      boundStyle: {
        color: '#04b00f',
        mask: 'rgba(0,0,0,0.8)',
        lineWidth: 1
      }
    }
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
    this.wecropper.getCropperImage((src) => {
      if (src) {
        console.log(src)
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
        //  获取裁剪图片资源后，给data添加src属性及其值
        self.setData({
          compositionUrl: src
        })
        self.wecropper.pushOrign(src);
      }
    })
  },
  //裁剪
  btnHandle: function () {
    //高清裁剪
    let quality = 0.7;
    if (this.data.quality) {
      quality = 1;
    }
    let _that = this;
    // 点击了裁剪按钮
    let devicePixelRatio = this.data.cropperOpt.pixelRatio
    let { imgLeft, imgTop, scaleWidth, scaleHeight } = this.wecropper // 获取图片在原画布坐标位置及宽高
    let { x, y, width, height } = this.wecropper.cut // 获取裁剪框位置及大小
    // 所有参数乘设备像素比
    imgLeft = imgLeft * devicePixelRatio
    imgTop = imgTop * devicePixelRatio
    scaleWidth = scaleWidth * devicePixelRatio
    scaleHeight = scaleHeight * devicePixelRatio
    x = x * devicePixelRatio
    y = y * devicePixelRatio
    width = width * devicePixelRatio
    height = height * devicePixelRatio
    const targetCtx = wx.createCanvasContext('hideCanvas') // 这里是目标canvas画布的id值
    targetCtx.drawImage(this.data.cropperOpt.src, imgLeft, imgTop, scaleWidth, scaleHeight) // tmp代表被裁剪图片的临时路径
    console.log("开始创建canvas");
    targetCtx.draw(false, function (e) {
      wx.canvasToTempFilePath({
        canvasId: 'hideCanvas',
        x,
        y,
        width,
        height,
        destWidth: _that.data.uploadWidth,
        destHeight: _that.data.uploadHeight,
        fileType: 'jpg',
        quality,
        success(res) {
          const tmpPath = res.tempFilePath;
          console.log("创建canvas成功");
          console.log(tmpPath);
          _that.afterGetPath(tmpPath)
        },
        fail(e) {
          console.log(e)
        }
      })
    })
  },
  afterGetPath(avatar) {
    if (avatar) {
      //  获取到裁剪后的图片
      var pages = getCurrentPages();
      if (pages.length > 1) {
        //上一个页面实例对象
        var prePage = pages[pages.length - 2];
        //关键在这里
        try {
          prePage.afterCuttingImg(avatar)
        } catch (e) {
          console.warn("please setting afterCuttingImg function to receive img url");
        }
        wx.navigateBack();
      }

    } else {
      console.log('获取图片失败，请稍后重试')
    }
  },
  onLoad(options) {
    var tempComposition = JSON.parse(options.tempComposition);
    let device = wx.getSystemInfoSync();
    let height = device.windowHeight - 50;
    this.setData({
      ["cropperOpt.height"]: height,
      ["cropperOpt.cut.y"]: (height - 300) / 2,
      compositionUrl: tempComposition.compositionUrl,
      compositionType: tempComposition.compositionType
    });
    const { cropperOpt } = this.data;
    console.log(cropperOpt);
    cropperOpt.boundStyle.color = this.data.cropperOpt.themeColor;
    this.setData({ cropperOpt });
    new WeCropper(cropperOpt)
      .on('ready', (ctx) => {
        //console.log(`wecropper is ready for work!`)
      })
      .on('beforeImageLoad', (ctx) => {
        //console.log(`before picture loaded, i can do something`)
        //console.log(`current canvas context:`, ctx)
        wx.showToast({
          title: '上传中',
          icon: 'loading',
          duration: 20000
        })
      })
      .on('imageLoad', (ctx) => {
        //console.log(`picture loaded`)
        //console.log(`current canvas context:`, ctx)
        wx.hideToast()
      })
      .on('beforeDraw', (ctx, instance) => {
        //console.log(`before canvas draw,i can do something`)
        //console.log(`current canvas context:`, ctx)
      })
      .updateCanvas()
    this.wecropper.pushOrign(tempComposition.compositionUrl);
  }
})
