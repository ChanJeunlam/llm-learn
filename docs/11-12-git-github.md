# 第 11–12 课：Git、GitHub 与代码管理

## 目标
掌握工作区、暂存区、本地仓库、远程仓库；用分支开发并通过 GitHub Actions 验证代码。

## 概念
- `git add`：把变化加入暂存区。
- `git commit`：生成本地快照；不会自动上传。
- `git push`：把本地提交推送到 GitHub。
- `git pull`：抓取并集成远程变化。
- `git switch -c feature/name`：新建并切换开发分支。

## 实操
```powershell
git clone https://github.com/ChanJeunlam/llm-learn.git
cd llm-learn
git status
git log --oneline -5
git switch -c feature/lesson-practice
# 修改 docs/ 中的练习记录
git add docs/
git commit -m "docs: finish lesson 11 practice"
git push -u origin feature/lesson-practice
```

在 GitHub 发起 Pull Request，确认 Actions 通过后再合并。不要提交 `.env`、密钥、真实个人聊天记录。

## 验收
1. 解释工作区/暂存区/本地仓库的区别。
2. 新建分支、提交一次练习、推送、打开 PR。
3. 查看 Actions 日志，说明代码未通过时如何定位错误。

官方参考：https://git-scm.com/docs ；https://docs.github.com/en/get-started
