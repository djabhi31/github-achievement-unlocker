<div align="center">

# 🚀 GitHub Achievement Unlocker & Hunter
### *Autonomous CLI Tool & 1-Click GitHub Action to Unlock Individual Badges or the Full Suite*

[![GitHub Stars](https://img.shields.io/github/stars/djabhi31/github-achievement-unlocker?style=for-the-badge&color=ffd700&logo=github)](https://github.com/djabhi31/github-achievement-unlocker/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/djabhi31/github-achievement-unlocker?style=for-the-badge&color=blue&logo=github)](https://github.com/djabhi31/github-achievement-unlocker/network/members)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<p align="center">
  <b>Want a specific badge or the complete collection?</b><br>
  Unlock <b>Quickdraw</b>, <b>Pull Shark</b>, <b>Pair Extraordinaire</b>, <b>Galaxy Brain</b> (up to Diamond tier), or <b>YOLO</b> individually or all together with 1 click!
</p>

[🎯 Select Individual Badges](#-unlock-individual-badges) • [🚀 Quick Start](#-quick-start) • [🎖️ Trophy Cabinet](#️-badges-you-can-unlock) • [⭐ Star This Project](#-support--star)

---

</div>

## 🎯 Unlock Individual Badges or All at Once!

You have complete flexibility:

| Badge Option | Target Achievement | What It Does | Supported Tiers |
| :--- | :--- | :--- | :--- |
| ⚡ **`quickdraw`** | **Quickdraw** | Creates and closes an issue in < 2 seconds | Standard |
| 🧠 **`galaxy-brain`** | **Galaxy Brain** | Creates Q&A discussions & marks answers accepted | Bronze (x2), Silver (x8), **Diamond (x32)** |
| 👥 **`pair-extraordinaire`** | **Pair Extraordinaire** | Merges co-authored pull requests | Bronze (x1), Silver (x10), **Gold (x24)** |
| 🦈 **`pull-shark`** | **Pull Shark** | Merges multiple pull requests | Bronze (x2), Silver (x16), Max (x25+) |
| 🚀 **`yolo`** | **YOLO** | Merges pull request without code review | Standard |
| 👑 **`all`** | **ALL BADGES** | Unlocks the complete suite up to the maximum tiers | All Max Tiers |

---

## 🎖️ Badges You Can Unlock

<div align="center">
<table>
  <tr>
    <td align="center" width="20%">
      <img src="https://raw.githubusercontent.com/Schweinepriester/github-profile-achievements/main/images/galaxy-brain-default.png" width="95" alt="Galaxy Brain"/><br/>
      <b>Galaxy Brain</b><br/>
      <sub><kbd>💎 DIAMOND (x32)</kbd></sub>
    </td>
    <td align="center" width="20%">
      <img src="https://raw.githubusercontent.com/Schweinepriester/github-profile-achievements/main/images/pair-extraordinaire-default.png" width="95" alt="Pair Extraordinaire"/><br/>
      <b>Pair Extraordinaire</b><br/>
      <sub><kbd>🥇 GOLD (x24)</kbd></sub>
    </td>
    <td align="center" width="20%">
      <img src="https://raw.githubusercontent.com/Schweinepriester/github-profile-achievements/main/images/pull-shark-default.png" width="95" alt="Pull Shark"/><br/>
      <b>Pull Shark</b><br/>
      <sub><kbd>🥈 SILVER (x16)</kbd></sub>
    </td>
    <td align="center" width="20%">
      <img src="https://raw.githubusercontent.com/Schweinepriester/github-profile-achievements/main/images/quickdraw-default.png" width="95" alt="Quickdraw"/><br/>
      <b>Quickdraw</b><br/>
      <sub><kbd>⚡ STANDARD</kbd></sub>
    </td>
    <td align="center" width="20%">
      <img src="https://raw.githubusercontent.com/Schweinepriester/github-profile-achievements/main/images/yolo-default.png" width="95" alt="YOLO"/><br/>
      <b>YOLO</b><br/>
      <sub><kbd>🚀 STANDARD</kbd></sub>
    </td>
  </tr>
</table>
</div>

---

## 🚀 Quick Start: How to Run

### 🔹 Method 1: 1-Click GitHub Action *(Zero Installation)*

1. **Fork this repository:** Click the [**Fork** button](https://github.com/djabhi31/github-achievement-unlocker/fork) at the top right.
2. **Add Personal Access Token (PAT):** *(Mandatory)*
   - Create a GitHub PAT with `repo` and `workflow` scopes at [github.com/settings/tokens/new](https://github.com/settings/tokens/new?scopes=repo,workflow).
   - In your forked repo, go to **Settings** ➔ **Secrets and variables** ➔ **Actions** ➔ **New repository secret**.
   - Set Name as `PERSONAL_ACCESS_TOKEN` and paste your token value.
   > **Note:** GitHub Actions default token (`github-actions[bot]`) cannot unlock user profile badges. A PAT is required so GitHub attributes the activity to your account!
3. Navigate to the **Actions** tab in your fork.
4. Click on **"🏆 1-Click GitHub Achievement Unlocker"** on the left menu.
5. Click **Run workflow**:
   - **Select Badge:** Choose `all` OR pick a specific badge (e.g. `pull-shark`, `pair-extraordinaire`, `quickdraw`, `yolo`).
   - **Target Tier:** Choose `max` (Diamond/Gold), `silver`, or `bronze`.
6. Click **Run workflow** and wait ~1–3 minutes!
7. Check your GitHub profile in 15–30 minutes!

---

### 🔹 Method 2: Local Python CLI Tool

Run directly on your terminal (no dependencies required, pure Python standard library):

```bash
# 1. Clone this repository
git clone https://github.com/djabhi31/github-achievement-unlocker.git
cd github-achievement-unlocker

# 2. Run interactively (will show a menu to pick your badge!)
python unlocker.py
```

#### Interactive Menu Preview:
```text
Select which badge(s) you want to unlock:
  [1] ⚡ Quickdraw (Instant issue closure)
  [2] 🦈 Pull Shark (Merge PRs)
  [3] 👥 Pair Extraordinaire (Co-authored PRs)
  [4] 🧠 Galaxy Brain (Q&A discussions accepted answers)
  [5] 🚀 YOLO (Direct PR merge without review)
  [6] 👑 ALL BADGES (Complete Suite up to Diamond/Gold)

Enter choice [1-6] (default 6):
```

#### Direct CLI Flags:
```bash
# Unlock ONLY Quickdraw:
python unlocker.py --badge quickdraw

# Unlock ONLY Galaxy Brain (Diamond Tier):
python unlocker.py --badge galaxy-brain --tier max

# Unlock ONLY Pair Extraordinaire (Gold Tier):
python unlocker.py --badge pair-extraordinaire --tier max

# Unlock ONLY Pull Shark (Silver Tier):
python unlocker.py --badge pull-shark --tier silver

# Unlock ALL badges together:
python unlocker.py --badge all --tier max
```

---

## ❓ Frequently Asked Questions (FAQ)

<details>
<summary><b>1. Will this affect my existing repositories?</b></summary>
<br>
No! The tool creates and uses an isolated sandbox repository (default: <code>github-achievement-sandbox</code>). None of your personal or work repositories are modified.
</details>

<details>
<summary><b>2. Can I unlock only one badge if I already have the others?</b></summary>
<br>
Yes! Use the <code>--badge &lt;name&gt;</code> flag or select the badge from the interactive menu. You can unlock exactly what you need without touching other badges.
</details>

<details>
<summary><b>3. How long before badges appear on my profile?</b></summary>
<br>
GitHub evaluates achievements asynchronously in background workers. Badges typically appear on your profile within <b>15 to 45 minutes</b>.
</details>

<details>
<summary><b>4. Why is Galaxy Brain restricted by GitHub?</b></summary>
<br>
GitHub's achievement engine explicitly ignores questions where the author marks their own response as the accepted answer. Furthermore, GitHub has restricted automated Discussion achievements on freshly created sandbox repositories to prevent spam farming. To earn Galaxy Brain, participate in active public discussions where other users accept your helpful answers!
</details>

<details>
<summary><b>5. How does Pair Extraordinaire co-author attribution work?</b></summary>
<br>
GitHub requires co-authored commits to reference a verified GitHub user email or noreply address (such as <code>583231+octocat@users.noreply.github.com</code>) so GitHub can link the commit to a valid GitHub account. You can also specify your friend's or secondary account's name and email using <code>--coauthor-name</code> and <code>--coauthor-email</code>.
</details>

---

## ⭐ Support & Star

If this repository or tool helped you unlock your GitHub achievements, please consider giving it a **Star ⭐**! It helps others discover the project and helps the maintainer unlock the Starstruck badge!

<div align="center">

Crafted with ❤️ by [**@djabhi31**](https://github.com/djabhi31)

[![Follow @djabhi31](https://img.shields.io/github/followers/djabhi31?label=Follow%20%40djabhi31&style=social)](https://github.com/djabhi31)

</div>
