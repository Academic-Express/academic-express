import { inject, onBeforeUnmount, type App } from 'vue'
import mitt, { type Emitter, type Handler } from 'mitt'

export type Events = {
  subscriptionUpdated: 'topic' | 'scholar' | 'institutions'
}

export const BUS = Symbol('bus')

export default {
  install(app: App) {
    const emitter = mitt<Events>()
    app.provide(BUS, emitter)
  },
}

export function useBus() {
  return inject(BUS) as Emitter<Events>
}

export function useEvent<Key extends keyof Events>(
  type: Key,
  handler: Handler<Events[Key]>,
) {
  const bus = useBus()
  bus.on(type, handler)
  onBeforeUnmount(() => bus.off(type, handler))
}
