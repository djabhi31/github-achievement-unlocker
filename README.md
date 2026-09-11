<div align="center">

# 🚀 GitHub Achievement Unlocker & Hunter
### *Autonomous CLI Tool & 1-Click GitHub Action to Unlock All GitHub Profile Badges*

[![GitHub Stars](https://img.shields.io/github/stars/djabhi31/github-achievement-unlocker?style=for-the-badge&color=ffd700&logo=github)](https://github.com/djabhi31/github-achievement-unlocker/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/djabhi31/github-achievement-unlocker?style=for-the-badge&color=blue&logo=github)](https://github.com/djabhi31/github-achievement-unlocker/network/members)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<p align="center">
  <b>Tired of having an empty GitHub Achievements section?</b><br>
  Unlock <b>Quickdraw</b>, <b>Pull Shark</b>, <b>Pair Extraordinaire</b>, and <b>Galaxy Brain</b> (up to Diamond tier) with a single click or command!
</p>

[🚀 Quick Start](#-quick-start-how-to-unlock) • [🎖️ Badges You Can Unlock](#️-badges-you-can-unlock) • [❓ FAQ](#-frequently-asked-questions-faq) • [⭐ Star This Project](#-support--star)

---

</div>

## 🎖️ Badges You Can Unlock

<div align="center">
<table>
  <tr>
    <td align="center" width="20%">
      <img src="https://raw.githubusercontent.com/Schweinepriester/github-profile-achievements/main/images/galaxy-brain-default.png" width="95" alt="Galaxy Brain"/><br/>
      <b>Galaxy Brain</b><br/>
      <sub><kbd>💎 DIAMOND TIER (x32)</kbd></sub>
    </td>
    <td align="center" width="20%">
      <img src="https://raw.githubusercontent.com/Schweinepriester/github-profile-achievements/main/images/pair-extraordinaire-default.png" width="95" alt="Pair Extraordinaire"/><br/>
      <b>Pair Extraordinaire</b><br/>
      <sub><kbd>🥇 GOLD TIER (x24)</kbd></sub>
    </td>
    <td align="center" width="20%">
      <img src="https://raw.githubusercontent.com/Schweinepriester/github-profile-achievements/main/images/pull-shark-default.png" width="95" alt="Pull Shark"/><br/>
      <b>Pull Shark</b><br/>
      <sub><kbd>🥈 SILVER TIER (x16)</kbd></sub>
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

## 🚀 Quick Start: How to Unlock

You can unlock all these achievements in **under 3 minutes** using either method:

### 🔹 Method 1: 1-Click GitHub Action *(Zero Installation)*

1. **Fork this repository:** Click the [**Fork** button](https://github.com/djabhi31/github-achievement-unlocker/fork) at the top right of this page.
2. Go to your forked repo's **Actions** tab.
3. Click on **"🏆 1-Click GitHub Achievement Unlocker"** in the left sidebar.
4. Click **Run workflow** -> select target tier (e.g. `max` for Diamond & Gold) -> Click **Run workflow**.
5. Wait ~2 minutes for the workflow to complete.
6. Check your GitHub profile in 15–30 minutes!

*(Note: For Galaxy Brain and full permissions, you can optionally add a PAT with `repo` scope under Settings -> Secrets and variables -> Actions as `PERSONAL_ACCESS_TOKEN`).*

---

### 🔹 Method 2: Local Python CLI Tool

Run it directly on your machine without installing any dependencies (uses standard Python library):

```bash
# 1. Clone this repository
git clone https://github.com/djabhi31/github-achievement-unlocker.git
cd github-achievement-unlocker

# 2. Run the unlocker script
python unlocker.py
```

The script will automatically detect your git credentials or prompt for your GitHub Token, create an isolated sandbox repository, and unlock all badges automatically!

#### CLI Flags:
```bash
# Unlock up to maximum Diamond & Gold tiers
python unlocker.py --level max

# Unlock up to Silver tiers
python unlocker.py --level silver

# Run in automated CI mode
python unlocker.py --automated --level max --repo my-achievements-sandbox
```

---

## 📊 Criteria & Tiers Unlocked

| Badge | Highest Tier | Criteria Required | Tool Automation |
| :--- | :--- | :--- | :--- |
| 💎 **Galaxy Brain** | **Diamond (x32)** | 32 accepted answers in Q&A Discussions | GraphQL API creates 32 Q&A discussions & marks answers accepted. |
| 🥇 **Pair Extraordinaire** | **Gold (x24)** | 24 co-authored merged pull requests | Automates 25 PRs with RFC-compliant co-authorship commit trailers. |
| 🥈 **Pull Shark** | **Silver (x16)** | 16 merged pull requests | Automatically generates branches, files, and merges 27 PRs. |
| ⚡ **Quickdraw** | **Standard** | Close issue/PR within 5 minutes | Opens an issue and closes it within < 2 seconds. |
| 🚀 **YOLO** | **Standard** | Merge PR without review | Direct PR merge without review requirement. |

---

## ❓ Frequently Asked Questions (FAQ)

<details>
<summary><b>1. Will this affect my existing repositories?</b></summary>
<br>
No! The tool creates and uses a dedicated sandbox repository (e.g., <code>github-achievement-sandbox</code>). None of your existing repositories or code are touched.
</details>

<details>
<summary><b>2. How long before badges appear on my profile?</b></summary>
<br>
GitHub evaluates achievements asynchronously in background queues. Badges typically appear on your profile within <b>15 to 45 minutes</b>. Refresh your profile achievements page after some time.
</details>

<details>
<summary><b>3. What should I do with the sandbox repository afterwards?</b></summary>
<br>
Do <b>not</b> delete it immediately! GitHub may revoke badges if the underlying repository is deleted before or during calculation. Best practice is to leave it public or <b>Archive</b> it once badges appear.
</details>

<details>
<summary><b>4. How do I get the Starstruck badge?</b></summary>
<br>
The <b>Starstruck</b> badge requires 16 stars from other unique GitHub users on one of your repositories. By sharing this open-source tool with others, you can earn stars organically!
</details>

---

## ⭐ Support & Star

If this repository or tool helped you unlock your GitHub achievements, please consider giving it a **Star ⭐**! It helps others discover the project and helps the maintainer unlock the Starstruck badge!

<div align="center">

Crafted with ❤️ by [**@djabhi31**](https://github.com/djabhi31)

[![Follow @djabhi31](https://img.shields.io/github/followers/djabhi31?label=Follow%20%40djabhi31&style=social)](https://github.com/djabhi31)

</div>
