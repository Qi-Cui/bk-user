<script setup lang="ts">
import { Message } from 'bkui-vue';
import en from 'bkui-vue/dist/locale/en.esm';
import zhCn from 'bkui-vue/dist/locale/zh-cn.esm';
import { computed, ref, watch  } from 'vue';
import { useRoute } from 'vue-router';

import { getPlatformConfig, setDocumentTitle, setShortcutIcon } from '@blueking/platform-config';

import HeaderBox from './views/MainHeader.vue';

import { currentUser } from '@/http';
import { locale as i18nLocal, t } from '@/language/index';
import { platformConfig, useUser } from '@/store';
import Password from '@/views/reset-password/index.vue';
import ResetPassword from '@/views/reset-password/newPassword.vue';

const route = useRoute();

const showName = ref(null);
// 判断是否是重置密码的路由
watch(() => route.name, (val) => {
  if (val === 'password' || val === 'resetPassword') {
    isLoading.value = false;
    return;
  }
  currentUser()
    .then((res) => {
      user.setUser(res.data);
    })
    .catch(() => {
      Message(t('获取用户信息失败，请检查后再试'));
    })
    .finally(() => {
      isLoading.value = false;
    });
});

// 加载完用户数据才会展示页面
const isLoading = ref(true);
// 获取用户数据
const user = useUser();

const currentLang = ref(i18nLocal.value);
// 多语言注入, 此处引用组件库内置多语言配置
const localeData = {
  'zh-cn': zhCn,
  en,
};

const locale = computed(() => localeData[currentLang.value]);

const platformConfigData = platformConfig();
const url = `${window.BK_SHARED_RES_URL}/bk_user/base.js`;  // url 远程配置文件地址
const defaults = {
  name: '用户管理',
  nameEn: 'User Management',
  productName: '蓝鲸用户管理',
  productNameEn: 'BK User Management',
  brandName: '蓝鲸智云',
  brandNameEn: 'Tencent BlueKing',
  version: '3.0',
};

const getConfigData = async () => {
  const config =  await getPlatformConfig(url, defaults);
  setShortcutIcon(config.favicon); // 设置favicon
  setDocumentTitle(config.i18n); // 设置document.title
  platformConfigData.update(config);
};
getConfigData();
</script>

<template>
  <div>
    <bk-config-provider :locale="locale">
      <Password v-if="showName === 'password'" />
      <ResetPassword v-else-if="showName === 'resetPassword'" />
      <bk-loading
        v-else
        :loading="isLoading"
        :class="{
          'main-loading': isLoading
        }"
      >
        <HeaderBox v-if="!isLoading" />
      </bk-loading>
    </bk-config-provider>
  </div>
</template>

<style lang="less" scoped>
  .main-loading {
    margin-top: 25vw;
  }
</style>
