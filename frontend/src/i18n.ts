import { createI18n } from 'vue-i18n'

import zhCN from './locales/zh-CN.json'

export const SUPPORTED_LOCALES = ['zh-CN']

export default createI18n({
  legacy: false,
  locale: 'zh-CN',
  fallbackLocale: 'zh-CN',
  messages: {
    'zh-CN': zhCN,
  },
})
