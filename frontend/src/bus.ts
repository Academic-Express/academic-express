import { inject, onBeforeUnmount, type App } from 'vue'
import mitt, { type Emitter, type Handler } from 'mitt'

export type Events = {
  subscriptionUpdated: 'topic' | 'scholar' | 'institutions'
}

export default {
  install(app: App) {
    const emitter = mitt<Events>()
    app.provide('bus', emitter)
  },
}

export function useBus() {
  return inject('bus') as Emitter<Events>
}

export function useEvent<Key extends keyof Events>(
  type: Key,
  handler: Handler<Events[Key]>,
) {
  const bus = useBus()
  bus.on(type, handler)
  onBeforeUnmount(() => bus.off(type, handler))
}
