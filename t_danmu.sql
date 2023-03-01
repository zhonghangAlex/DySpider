/*
 Navicat Premium Data Transfer

 Source Server         : TDSQL-腾讯云数据库
 Source Server Type    : MySQL
 Source Server Version : 80022
 Source Host           : sh-cynosdbmysql-grp-dy68nzyy.sql.tencentcdb.com:20984
 Source Schema         : DY_Spider_DB

 Target Server Type    : MySQL
 Target Server Version : 80022
 File Encoding         : 65001

 Date: 01/03/2023 21:15:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_danmu
-- ----------------------------
DROP TABLE IF EXISTS `t_danmu`;
CREATE TABLE `t_danmu`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `roomId` bigint(0) NULL DEFAULT NULL COMMENT '直播间号',
  `shortId` bigint(0) NOT NULL COMMENT '评论/用户编号',
  `nickName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '用户昵称',
  `gender` int(0) NULL DEFAULT NULL COMMENT '0为未知，1为男，2为女',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户弹幕内容',
  `createTime` datetime(0) NULL DEFAULT NULL COMMENT '弹幕发布时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
