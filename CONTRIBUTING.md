# Contributing Guidelines

## 分支管理规范

主要参考：[GitLab Flow 介绍](https://gitlab.cn/docs/jh/topics/gitlab_flow.html)。

1. 主分支：`main`，用于日常开发和集成测试。
2. 生产分支：`production`，用于生产部署。交付部署版本时从主分支合并。
3. 发布分支：`x.y-stable`，用于稳定发布，每个发布版本都有独立的分支，发布版本时从主分支分叉。
4. 功能分支：`feature/{topic}`，每个功能都有独立的分支，功能完成后合并至主分支。功能分支的改动覆盖范围应尽量小，但需要做到 self-contained。
5. 修复分支：`hotfix/{bug-description}`，用于紧急修复部署和发布版本中的问题，完成后直接合并至主分支，再使用 cherry-pick 同步到生产分支和发布分支。

## 代码提交规范

1. 提交信息格式规范参考 [Vue Git Commit Message Convention](https://github.com/vuejs/core/blob/main/.github/commit-convention.md)。

2. 主分支原则上只允许 Pull Request。例外：过于平凡的提交（如修复 typo，格式化代码等）；完全独立于项目其它部分的提交。

3. 生产分支和发布分支只允许 Pull Request。

4. 主分支要求维护线性历史，合并 Pull Request 时使用 rebase 或 squash，不使用 merge。

   1. 创建 Pull Request 前先在本地执行 rebase 并处理合并冲突。
   2. 从远程分支拉取更改时总是使用 rebase 或 fast-forward，不使用 merge。

   例如，将本地功能分支与远程主分支同步，可以执行：
   ```bash
   $ git fetch origin
   $ git rebase origin/main
   ```
   或
   ```bash
   $ git pull --rebase origin main
   ```

5. 主分支、生产分支和发布分支禁止 force push。

6. 确有必要时，可以对功能分支 force push。场景：rebase 提交历史；移除包含敏感信息的提交等。

7. 尽量避免多人同时在同一功能分支上工作。

8. 所有 Pull Request 需要 Code Review 才能合并。

## 项目管理规范

1. 项目开发进度使用 GitHub Projects 追踪，视情况创建对应的 Draft / Issue / Pull Request。
2. 有关具体 Issue / Pull Request 的讨论在项目群内进行，GitHub 只用于进度追踪和事项备忘。

最后更新：2024 年 11 月 14 日
