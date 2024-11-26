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
  avatar: string
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
  comment: string | null
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

export interface GithubRepo {
  repo_id: string
  name: string
  full_name: string
  description: string | null
  html_url: string
  owner: GithubAccount

  created_at: string
  updated_at: string
  pushed_at: string

  homepage: string | null
  size: number
  language: string | null
  license: string | null
  topics: string[]

  stargazers_count: number
  forks_count: number
  open_issues_count: number
  network_count: number
  subscribers_count: number

  readme: string | null

  view_count: number
}

export interface GithubAccount {
  login: string
  id: number
  type: string
  avatar_url: string
}

export interface TopicSubscription {
  id: number
  topic: string
  created_at: string
  updated_at: string
}

export interface TopicSubscriptionRequest {
  topic: string
}

export interface ScholarSubscription {
  id: number
  scholar_name: string
  created_at: string
  updated_at: string
}

export interface ScholarSubscriptionRequest {
  scholar_name: string
}

export enum FeedOrigin {
  Arxiv = 'arxiv',
  Github = 'github',
}

export interface BaseFeed {
  origin: FeedOrigin
  timestamp: string
}

export interface ArxivEntryFeed extends BaseFeed {
  origin: FeedOrigin.Arxiv
  entry: ArxivEntry
}

export interface GithubRepoFeed extends BaseFeed {
  origin: FeedOrigin.Github
  repo: GithubRepo
}

export type Feed = ArxivEntryFeed | GithubRepoFeed

export type FollowFeed = Feed & {
  source: {
    scholar_names?: string[]
  }
}

export type SubscriptionFeed = Feed & {
  source: {
    topics?: string[]
  }
}

export const URLS = {
  login: '/v1/user/login',
  refreshLogin: '/v1/user/login/refresh',
  register: '/v1/user/register',
  getCurrentUser: '/v1/user/profile',
  getUserById: (userId: number) => `/v1/user/profile/${userId}`,

  getArxivEntry: (arxivId: string) => `/v1/pub/arxiv/${arxivId}`,
  getGithubRepo: (owner: string, repo: string) => `/v1/pub/gh/${owner}/${repo}`,

  getTopicSubscriptions: '/v1/sub/topics',
  subscribeTopic: '/v1/sub/topics',
  unsubscribeTopic: (id: number) => `/v1/sub/topics/${id}`,
  getScholarSubscriptions: '/v1/sub/scholars',
  subscribeScholar: '/v1/sub/scholars',
  unsubscribeScholar: (id: number) => `/v1/sub/scholars/${id}`,

  getFollowFeed: '/v1/feed/follow',
  getSubscriptionFeed: '/v1/feed/subscription',
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

export function getGithubRepo(owner: string, repo: string) {
  return client.get<GithubRepo>(URLS.getGithubRepo(owner, repo))
}

export function getTopicSubscriptions() {
  return client.get<TopicSubscription[]>(URLS.getTopicSubscriptions)
}

export function subscribeTopic(payload: TopicSubscriptionRequest) {
  return client.post<TopicSubscription>(URLS.subscribeTopic, payload)
}

export function unsubscribeTopic(id: number) {
  return client.delete<void>(URLS.unsubscribeTopic(id))
}

export function getScholarSubscriptions() {
  return client.get<ScholarSubscription[]>(URLS.getScholarSubscriptions)
}

export function subscribeScholar(payload: ScholarSubscriptionRequest) {
  return client.post<ScholarSubscription>(URLS.subscribeScholar, payload)
}

export function unsubscribeScholar(id: number) {
  return client.delete<void>(URLS.unsubscribeScholar(id))
}

export function getFollowFeed() {
  return client.get<FollowFeed[]>(URLS.getFollowFeed)
}

export function getSubscriptionFeed() {
  return client.get<SubscriptionFeed[]>(URLS.getSubscriptionFeed)
}
