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
  nickname?: string
  url?: string
  email?: string
  phone?: string
  intro?: string
}

export interface ChangePasswordRequest {
  old_password: string
  new_password: string
}

export interface UserStats {
  topic_count: number
  scholar_count: number
  collection_count: number
  claim_count: number
  comment_count: number
  history_count: number
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
  item: ArxivEntry
}

export interface GithubRepoFeed extends BaseFeed {
  origin: FeedOrigin.Github
  item: GithubRepo
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

export type HotFeed = Feed & {}

export type SearchResult = Feed & {}

export interface BaseCollection {
  id: number
  item_type: FeedOrigin
  /** arxiv_id or String(repo_id) */
  item_id: string
  created_at: string
}

export interface ArxivCollection extends BaseCollection {
  item_type: FeedOrigin.Arxiv
  item: ArxivEntry
}

export interface GithubCollection extends BaseCollection {
  item_type: FeedOrigin.Github
  item: GithubRepo
}

export type Collection = ArxivCollection | GithubCollection

export interface AddCollectionRequest {
  item_type: FeedOrigin
  /** arxiv_id or String(repo_id) */
  item_id: string
}

export interface CollectionGroup {
  id: number
  name: string
  description: string
  is_public: boolean
  created_at: string
  updated_at: string
  items: Collection[]
  items_count: number
}

export interface CreateCollectionGroupRequest {
  name: string
  description: string
  is_public: boolean
}

export interface CollectionGroupManageItemRequest {
  action: 'add' | 'remove'
  collection_ids: number[]
}

export type PatchCollectionGroupRequest = Partial<CreateCollectionGroupRequest>

export interface BaseHistory {
  id: number
  content_type: FeedOrigin
  viewed_at: string
}

export interface ArxivHistory extends BaseHistory {
  content_type: FeedOrigin.Arxiv
  entry_data: ArxivEntry
}

export interface GithubHistory extends BaseHistory {
  content_type: FeedOrigin.Github
  entry_data: GithubRepo
}

export type History = ArxivHistory | GithubHistory

export interface Comment {
  id: number
  /** arxiv_id or String(repo_id) */
  resource: string
  content: string
  author: User
  parent: number | null
  created_at: string
  updated_at: string
  vote_count: number
  user_vote: number
  replies: Comment[]
}

export interface CommentRequest {
  content: string
  parent?: number | null
}

export enum VoteAction {
  Up = 1,
  Down = -1,
  Cancel = 0,
}

export interface CommentVoteRequest {
  value: VoteAction
}

export interface ResourceClaim {
  id: number
  user: User
  resource_type: FeedOrigin
  resource_id: string
  created_at: string
}

export interface BaseUserResourceClaim {
  id: number
  user: number
  resource_type: FeedOrigin
  resource_id: string
  created_at: string
}

export interface ArxivUserResourceClaim extends BaseUserResourceClaim {
  resource_type: FeedOrigin.Arxiv
  resource: ArxivEntry
}

export interface GithubUserResourceClaim extends BaseUserResourceClaim {
  resource_type: FeedOrigin.Github
  resource: GithubRepo
}

export type UserResourceClaim = ArxivUserResourceClaim | GithubUserResourceClaim

export const URLS = {
  login: '/v1/user/login',
  refreshLogin: '/v1/user/login/refresh',
  register: '/v1/user/register',
  getCurrentUser: '/v1/user/profile',
  getAvatar: '/v1/user/avatar',
  changePassword: '/v1/user/change-password',
  getSelfStats: '/v1/user/stats',

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
  getHotFeed: '/v1/feed/hot',
  getSearchResult: '/v1/feed/search',

  collections: '/v1/collections/',
  collection: (id: number) => `/v1/collections/${id}`,
  collectionGroups: '/v1/collections/groups',
  collectionGroup: (groupId: number) => `/v1/collections/groups/${groupId}`,
  collectionGroupManageItems: (groupId: number) =>
    `/v1/collections/groups/${groupId}/manage_items`,

  history: '/v1/history',
  historyItem: (id: number) => `/v1/history/${id}/`,

  comments: (origin: FeedOrigin, resource: string) =>
    `/v1/comments/${origin}/${resource}/`,
  comment: (origin: FeedOrigin, resource: string, commentId: number) =>
    `/v1/comments/${origin}/${resource}/${commentId}/`,
  commentVote: (origin: FeedOrigin, resource: string, commentId: number) =>
    `/v1/comments/${origin}/${resource}/${commentId}/vote/`,

  resourceClaim: (origin: FeedOrigin, resource: string) =>
    `/v1/pub/claim/${origin}/${resource}`,
  getUserClaims: (userId: number) => `/v1/user/profile/${userId}/claim`,
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

export function changePassword(payload: ChangePasswordRequest) {
  return client.post<void>(URLS.changePassword, payload)
}

export function getSelfStats() {
  return client.get<UserStats>(URLS.getSelfStats)
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

export function getHotFeed() {
  return client.get<HotFeed[]>(URLS.getHotFeed)
}

export function getSearchResult(query: string) {
  return client.get<SearchResult[]>(URLS.getSearchResult, {
    params: {
      q: query,
    },
  })
}

export function uploadAvatar(file: File) {
  const formData = new FormData()
  formData.append('avatar', file)

  return client.post<UserDetail>(URLS.getAvatar, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

export function getCollections() {
  return client.get<Collection[]>(URLS.collections)
}

export function addCollection(payload: AddCollectionRequest) {
  return client.post<Collection>(URLS.collections, payload)
}

export function removeCollection(id: number) {
  return client.delete<void>(URLS.collection(id))
}

export function getCollectionGroups() {
  return client.get<CollectionGroup[]>(URLS.collectionGroups)
}

export function createCollectionGroup(payload: CreateCollectionGroupRequest) {
  return client.post<CollectionGroup>(URLS.collectionGroups, payload)
}

export function getCollectionGroup(id: number) {
  return client.get<CollectionGroup>(URLS.collectionGroup(id))
}

export function updateCollectionGroup(
  id: number,
  payload: PatchCollectionGroupRequest,
) {
  return client.patch<CollectionGroup>(URLS.collectionGroup(id), payload)
}

export function removeCollectionGroup(id: number) {
  return client.delete<void>(URLS.collectionGroup(id))
}

export function manageCollectionGroupItems(
  groupId: number,
  payload: CollectionGroupManageItemRequest,
) {
  return client.post<void>(URLS.collectionGroupManageItems(groupId), payload)
}

export function getHistory() {
  return client.get<History[]>(URLS.history)
}

export function getHistoryItem(id: number) {
  return client.get<History>(URLS.historyItem(id))
}

export function removeHistoryItem(id: number) {
  return client.delete<void>(URLS.historyItem(id))
}

export function getComments(origin: FeedOrigin, resource: string) {
  return client.get<Comment[]>(URLS.comments(origin, resource))
}

export function postComment(
  origin: FeedOrigin,
  resource: string,
  payload: CommentRequest,
) {
  return client.post<Comment>(URLS.comments(origin, resource), payload)
}

export function editComment(
  origin: FeedOrigin,
  resource: string,
  commentId: number,
  payload: Omit<CommentRequest, 'parent'>,
) {
  return client.patch<Comment>(
    URLS.comment(origin, resource, commentId),
    payload,
  )
}

export function deleteComment(
  origin: FeedOrigin,
  resource: string,
  commentId: number,
) {
  return client.delete<void>(URLS.comment(origin, resource, commentId))
}

export function voteComment(
  origin: FeedOrigin,
  resource: string,
  commentId: number,
  payload: CommentVoteRequest,
) {
  return client.post<void>(
    URLS.commentVote(origin, resource, commentId),
    payload,
  )
}

export function getResourceClaims(origin: FeedOrigin, resource: string) {
  return client.get<ResourceClaim[]>(URLS.resourceClaim(origin, resource))
}

export function claimResource(origin: FeedOrigin, resource: string) {
  return client.post<ResourceClaim>(URLS.resourceClaim(origin, resource))
}

export function unclaimResource(origin: FeedOrigin, resource: string) {
  return client.delete<void>(URLS.resourceClaim(origin, resource))
}

export function getUserClaims(userId: number) {
  return client.get<UserResourceClaim[]>(URLS.getUserClaims(userId))
}
