import { useConfirm } from 'primevue/useconfirm'
import type { ConfirmationOptions } from 'primevue/confirmationoptions'

export function usePromiseConfirm() {
  const confirm = useConfirm()

  return {
    require(options: ConfirmationOptions): Promise<boolean> {
      return new Promise(resolve => {
        confirm.require({
          ...options,
          accept: () => resolve(true),
          reject: () => resolve(false),
        })
      })
    },

    close() {
      confirm.close()
    },
  }
}
