import client from './axios'

export interface ErrorDetail {
  detail: string
  code: string
}

export interface ErrorResponse extends ErrorDetail {
  fields?: Record<string, ErrorDetail[]>
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RefreshRequest {
  refresh: string
}

export interface TokenPair {
  access: string
  refresh: string
}

export interface RegisterRequest {
  username: string
  password: string
  nickname: string
  email: string
  phone: string
  url?: string
}

export interface User {
  id: number
  username: string
  nickname: string
  url: string
  scholar_url: string
  intro: string
  view_count: number
  date_joined: string
}

export interface UserDetail extends User {
  email: string
  phone: string
  last_login: string
}

export interface PatchProfileRequest {
  nickname: string
  url: string
  email: string
  phone: string
}

export interface ArxivEntry {
  arxiv_id: string
  title: string
  summary: string
  authors: ArxivAuthor[]
  comment: string
  published: string
  updated: string
  primary_category: string
  categories: string[]
  link: string
  pdf: string
  slug: string
  view_count: number
  citation_count: number
}

export interface ArxivAuthor {
  name: string
  affiliation?: string
}

export const URLS = {
  login: '/v1/user/login',
  refreshLogin: '/v1/user/login/refresh',
  register: '/v1/user/register',
  getCurrentUser: '/v1/user/profile',
  getUserById: (userId: number) => `/v1/user/profile/${userId}`,
  getArxivEntry: (arxivId: string) => `/v1/pub/arxiv/${arxivId}`,
}

export function login(payload: LoginRequest) {
  return client.post<TokenPair>(URLS.login, payload)
}

export function refreshLogin(payload: RefreshRequest) {
  return client.post<TokenPair>(URLS.refreshLogin, payload)
}

export function register(payload: RegisterRequest) {
  return client.post<UserDetail>(URLS.register, payload)
}

export function getCurrentUser() {
  return client.get<UserDetail>(URLS.getCurrentUser)
}

export function getUserById(userId: number) {
  return client.get<User>(URLS.getUserById(userId))
}

export function patchProfile(payload: PatchProfileRequest) {
  return client.patch<UserDetail>(URLS.getCurrentUser, payload)
}

export function getArxivEntry(arxivId: string) {
  return client.get<ArxivEntry>(URLS.getArxivEntry(arxivId))
}
