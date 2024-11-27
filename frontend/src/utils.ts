export function isUrlAbsolute(url: string) {
  return url.includes('://') || url.startsWith('//')
}
