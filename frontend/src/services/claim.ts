import { inject, provide, ref } from 'vue'
import type { ResourceClaim } from './api'

export const AUTHOR_IDS = Symbol('claim:authorIds')

export function useClaim() {
  const authorIds = ref<number[]>([])
  const onClaimsUpdated = (claims: ResourceClaim[]) => {
    authorIds.value = claims.map(claim => claim.user.id)
  }

  provide(AUTHOR_IDS, authorIds)

  return { onClaimsUpdated }
}

export function useClaimAuthorIds() {
  const authorIds = inject<number[]>(AUTHOR_IDS)!
  return { authorIds }
}
