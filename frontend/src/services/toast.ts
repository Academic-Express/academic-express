import { useToast } from 'primevue/usetoast'
import type { ToastMessageOptions } from 'primevue/toast'
import { useI18n } from 'vue-i18n'
import { AxiosError } from 'axios'

import type { ErrorResponse } from './api'

export function useCustomToast() {
  const { t } = useI18n()
  const toast = useToast()

  return {
    ...toast,

    reportError(error: unknown, options?: ToastMessageOptions) {
      options = {
        severity: 'error',
        summary: t('toast.error'),
        detail: t('toast.unknownError'),
        life: 5000,
        ...options,
      }

      if (error instanceof AxiosError && error.response?.data) {
        const data = error.response.data as ErrorResponse
        options.detail = data.detail ?? options.detail
      }

      console.error('Request failed:', error)
      toast.add(options)
    },
  }
}
