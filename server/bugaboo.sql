DROP TABLE IF EXISTS `store`;
CREATE TABLE `store` (
    `store_id` INT(2) NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '门店id',
    `store_name` VARCHAR(128) COMMENT '门店名称',
    `store_city` VARCHAR(32) COMMENT '门店所在城市',
    `store_address` VARCHAR(256) COMMENT '门店地址',
    `store_phone` VARCHAR(32) COMMENT '门店电话'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海古北门店', '上海', '上海市黄金城道623号', '021 6236 2363');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海华山路门店', '上海', '上海市华山路620-1号', '021 6288 7620');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海浦东嘉里城', '上海', '上海市花木路1378号浦东嘉里城1209b店铺', '021 5043 2161');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海静安嘉里中心', '上海', '上海市南京西路1515号嘉里中心n4-07店铺', '021 6245 8302');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海港汇恒隆广场', '上海', '上海市虹桥路1号港汇恒隆广场北楼四楼458', '021 5466 9295');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海月星环球港', '上海', '上海市中山北路3300号上海月星环球港L3111商铺', '021 6212 9719');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海合生汇商场', '上海', '上海市杨浦区翔殷路1099号上海合生汇国际广场3层21号商铺', '021 6566 1311');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海万象城', '上海', '上海市吴中路1551号上海万象城L415商铺', '021 5433 2102');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海浦东嘉里城', '上海', '上海市花木路1378号浦东嘉里城地下一层B136/137店铺', '021 6836 8988');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海静安嘉里中心', '上海', '上海市南京西路1515号嘉里中心四层N4-02店铺', '021 6025 0577');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('上海丁香国际', '上海', '浦东新区丁香路858号 丁香国际商业中心 L212&L213', '021 6858 3669');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('北京将台路门店', '北京', '北京市朝阳区将台路2号 和乔丽晶一层底商', '010 8450 1589');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('北京朝阳大悦城', '北京', '北京市朝阳区朝阳北路101号朝阳大悦城5F-05', '010 8552 7509');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('北京金源新燕莎', '北京', '北京市海淀区远大路1号金源新燕莎L4-4101店铺', '010 8843 7137');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('北京侨福芳草地', '北京', '北京市朝阳区东大桥路9号楼侨福芳草地二层(02)L2-29', '010 5690 7311');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('北京荟聚购物中心', '北京', '北京市，大兴区，欣宁街15号1号楼荟聚中心L13层4-03-83-SU号', '010 5095 4023');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('北京华润五彩城', '北京', '北京市海淀区清河中街68号华润五彩城L464B', '010 6292 8458');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('北京蓝色港湾商区', '北京', '北京市朝阳区朝阳公园路6号院蓝色港湾国际商区2号楼1层VDM-20', '010 5905 6905');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('北京顺义店', '北京', '北京市顺义区安泰大街9号院祥云小镇5号楼102店铺', '010 6040 7001');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('成都新世纪环球中心', '成都', '成都市武侯区天府大道北段1700号新世纪环球中心东区3栋3层3FB02/04/06', '028 6873 1868');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('成都IFS', '成都', '成都市锦江区红星路三段1号国际金融中心LG214a', '028 8674 9611');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('成都银泰In99', '成都', '成都市高新区天府大道北段1199号成都银泰商场L548商铺', ' 028 6523 1636 ');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('成都大悦城', '成都', '成都市武侯区大悦路518号大悦城3F-076', '028 6650 3655');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('成都悠方店', '成都', '成都市交子大道300号悠方购物中心409+410', '028 6129 5670');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('成都金牛凯德广场', '成都', '成都市金牛区交大路183号金牛凯德广场四楼B04-31店铺', '137 3085 8001');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('深圳万象城', '深圳', '深圳市罗湖区宝安南路1881号华润中心万象城4楼472室 ', '0755 8269 0091');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('深圳万象天地', '深圳', '深圳市南山区粤海街道深南大道9668号华润万象天地 SL4 SL438 号商铺', '0755 8668 8710');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('深圳万象天地', '深圳', '深圳市南山区粤海街道深南大道9668号华润万象天地 SL4 SL421 号商铺', '0755 8668 0120');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('广州IGC天汇广场', '广州', '广州市天河区珠江新城兴民路222号天汇广场igc四层422铺 ', '020 3727 7551');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('天津奥城门店', '天津', '天津市南开区时代奥城C7-101店铺', '022 8796 5501');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('天津鲁能城店', '天津', '天津市南开区水上公园东路鲁能城购物中心3f-17', '022 5990 5501');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('郑州丹尼斯大卫城', '郑州', '河南省郑州市二七区二七路太康路交叉口丹尼斯大卫城9楼', '0371 5507 8982');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('郑州丹尼斯三天地', '郑州', '河南省郑州市金水区商务西三街中段丹尼斯三天地B1层', '0371 5507 8981');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('沈阳万象城', '沈阳', '沈阳市和平区青年大街288号沈阳华润万象城6层L607', '024 3137 9619');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('宁波和义大道购物中心', '宁波', '宁波市和义路66号和义大道购物中心三层3021商铺', '0574 8730 5108 ');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('苏州圆融星空广场', '苏州', '苏州工业园区旺墩路269号圆融星座天空区3F/3280', '153 7186 1967');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('苏州高铁新城圆融广场', '苏州', '苏州相城区高铁新城南天成路110号圆融广场购物中心2楼2100商铺', '153 5880 8720');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('苏州久光百货', '苏州', '苏州市工业园区旺墩路168号苏州久光百货蓝区三楼i-lollipop专柜', '');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('杭州大厦', '杭州', '杭州市武林广场1号杭州大厦B座6楼', '0571 2899 5541');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('杭州万象城', '杭州', '杭州市江干区富春路701号万象城436', '0571 2892 8936');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('杭州万象汇', '杭州', '杭州市萧山区萧山区北干街道金城路927号杭州万象汇4楼457号', '157 2495 8326');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('杭州嘉里中心', '杭州', '杭州市下城区延安路385号嘉里中心3幢L503', '0571 2810 6368');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('杭州大悦城', '杭州', '杭州市拱墅区莫干山路与隐秀路交汇处杭州大悦城L3-38 ', '130 0367 9880');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('合肥银泰中心', '合肥', '安徽省合肥市长江中路98号合肥银泰中心5楼MOTOBABY专柜', '130 8282 6969');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('重庆时代广场', '重庆', '重庆市渝中区邹容路100号L514号', '023 6310 2320');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('重庆IFS', '重庆', '重庆市江北城北大街38号国金中心L108号商铺', '023 6707 1893');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('江阴新一城商业广场', '江阴', '江阴市澄江中路87-89号新一城商业广场购物中心3楼   ', '189 6152 5585');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('武汉万达广场', '武汉', '武汉市武昌区水果湖沙湖大道18号3F-28-2', '027 8783 4399');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('武汉K11', '武汉', '武汉市洪山区东湖开发区关山大道349号光谷K11购物艺术中心L2层211', '027 8778 6338');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('哈尔滨卓展购物中心', '哈尔滨', '哈尔滨市道里区安隆街106号 卓展购物中心五层Tomato Family', '186 0460 5799');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('长沙国金中心', '长沙', '长沙市芙蓉区解放路国金中心IFS LG232-233商铺', '0731 8990 9500');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('长春卓展购物中心', '长春', '长春市朝阳区重庆路1255号卓展购物中心A座6层i-Lollipop商铺 ', '');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('青岛华润万象城', '青岛', '青岛市市南区山东路6号甲华润中心万象城L-409号商铺', '0532 5576 8732');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('南京德基广场', '南京', '南京市中山路18号德基广场六层F635号', '025 8677 7680');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('无锡恒隆广场', '无锡', '无锡市梁溪区人民中路139号无锡恒隆广场商场3楼301&302铺位 ', '0510 8274 0320');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('大连恒隆广场', '大连', '大连市西岗区五四路66号恒隆广场5F 551号', '0411 3905 8814');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('西安中大国际商业中心', '西安', '西安市雁塔区高新路72号中大国际商业中心L411', '029 8881 7868');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('西安中大国际店', '西安', '西安市碑林区南大街30号中大国际店六层A620', '029 8720 3594');
INSERT INTO `store` ( `store_name`, `store_city`, `store_address`, `store_phone`)
VALUES ('南宁万象城', '南宁', '南宁市青秀区民族大道136号万象城L523', '0771 5349 775');

DROP TABLE IF EXISTS `award`;
CREATE TABLE `award` (
	`award_id` INT(2) NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '奖品id',
	`award_name` VARCHAR(128) COMMENT '奖品名称',
	`award_image` VARCHAR(256) COMMENT '奖品图片',
	`award_type` TINYINT(1) DEFAULT 1 COMMENT '奖品类型',
	`award_description` VARCHAR(1024) COMMENT '奖品描述'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `award` (`award_name`, `award_image`, `award_type`, `award_description`) VALUES ('保温杯', 'https://bestbwzs.com/image/bugaboo.gif', 1, '大叔范');
INSERT INTO `award` (`award_name`, `award_image`, `award_type`, `award_description`) VALUES ('笔记本', 'https://bestbwzs.com/image/bugaboo.gif', 1, '文艺范');
INSERT INTO `award` (`award_name`, `award_image`, `award_type`, `award_description`) VALUES ('背包', 'https://bestbwzs.com/image/bugaboo.gif', 1, '旅行范');
INSERT INTO `award` (`award_name`, `award_image`, `award_type`, `award_description`) VALUES ('天猫优惠券1', 'https://bestbwzs.com/image/bugaboo.gif', 2, '满2000减200');
INSERT INTO `award` (`award_name`, `award_image`, `award_type`, `award_description`) VALUES ('天猫优惠券2', 'https://bestbwzs.com/image/bugaboo.gif', 2, '满1000减100');
INSERT INTO `award` (`award_name`, `award_image`, `award_type`, `award_description`) VALUES ('天猫优惠券3', 'https://bestbwzs.com/image/bugaboo.gif', 2, '满500减50');

