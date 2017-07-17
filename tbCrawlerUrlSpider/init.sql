-- -------------------------------------------------
-- @date 2017-07-14
-- @author xfli
-- @notes 基础数据表
-- -------------------------------------------------

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------
-- tb_urls_crawler表
-- ------------------------------------
DROP TABLE IF EXISTS `tb_urls_crawler`;
CREATE TABLE `tb_urls_crawler` (
  `id` int(11) NOT NULL COMMENT 'tb_urls_crawler表主键id',
  `pid` int(11) NOT NULL DEFAULT 0 COMMENT '爬虫上一节点（本url由父url链接导入）',
  `url` varchar(255) NOT NULL DEFAULT '' COMMENT '本url地址',
  `depth` tinyint(4) NOT NULL DEFAULT 0 COMMENT '爬虫深度',
  `max_depth` tinyint(4) NOT NULL DEFAULT 3 COMMENT '爬虫最大深度默认为3',
  `create_time` bigint NOT NULL DEFAULT 0 COMMENT '该url写入数据库时间',
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ------------------------------------
-- tb_goods_crawler表
-- ------------------------------------
DROP TABLE IF EXISTS `tb_goods_crawler`;
CREATE TABLE `tb_goods_crawler` (
  `id` int(11) NOT NULL COMMENT 'tb_goods_crawler表主键id',
  `shop_name` varchar(255) NOT NULL DEFAULT '' COMMENT '店铺名称',
  `shop_url` varchar(255) NOT NULL DEFAULT '' COMMENT '店铺链接',
  `shop_age` int(8) NOT NULL DEFAULT 0 COMMENT '店铺年龄',
  `seller_name` varchar(255) NOT NULL DEFAULT '' COMMENT '卖家名称',
  `goods_title` varchar(255) NOT NULL DEFAULT '' COMMENT '宝贝标题',
  `goods_url` varchar(255) NOT NULL DEFAULT '' COMMENT '宝贝链接',
  `goods_commets_count` int(11) NOT NULL DEFAULT 0 COMMENT '宝贝评论数',
  `goods_sales_count` int(11) NOT NULL DEFAULT 0 COMMENT '宝贝销量数',
  `goods_img_url` varchar(255) NOT NULL DEFAULT '' COMMENT '宝贝图片链接地址',
  `goods_local_img_path` varchar(255) NOT NULL DEFAULT '' COMMENT '宝贝本地图片路径',
  `goods_old_price` varchar(255) NOT NULL DEFAULT '' COMMENT '宝贝原价',
  `goods_now_price` varchar(255) NOT NULL DEFAULT '' COMMENT '宝贝当前价格',
  `goods_details` text NOT NULL DEFAULT '' COMMENT '宝贝详情',
  `create_time` bigint NOT NULL DEFAULT 0 COMMENT '该数据写入数据库时间',
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
