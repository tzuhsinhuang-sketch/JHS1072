# 企劃書工具環境設定 SOP

本文件說明如何設定環境，開始使用 Slot 企劃書工具。

---

## 一、申請 GitHub 帳號

1. 前往 [https://github.com](https://github.com)，點擊 Sign up
2. 填入 Email、密碼、用戶名後完成註冊
3. 把你的 GitHub 用戶名告知 **子馨**，由她將你加入 repo

---

## 二、安裝 GitHub Desktop

1. 前往 [https://desktop.github.com](https://desktop.github.com) 下載並安裝
2. 開啟後點擊 **Sign in to GitHub.com**，登入你的帳號

---

## 三、Clone Repo（取得工具與模板）

1. 開啟 GitHub Desktop
2. 點擊上方選單 **File → Clone repository**
3. 選擇 **URL** 分頁，貼入以下網址：
   ```
   https://github.com/tzuhsinhuang-sketch/JHS1072
   ```
4. 選擇你想存放的資料夾（例如 `D:\Claude Project\Slot-Spec`）
5. 點擊 **Clone**

Clone 完成後，資料夾內會有所有工具與模板。

---

## 四、安裝 Python

1. 前往 [https://www.python.org/downloads](https://www.python.org/downloads)，下載 **Python 3.11**
2. 安裝時勾選 **Add Python to PATH**，再點 Install Now
3. 安裝完成後，開啟命令提示字元（搜尋「cmd」），輸入：
   ```
   python --version
   ```
   看到版本號代表安裝成功

4. 安裝必要套件，在 cmd 輸入：
   ```
   pip install markdown watchdog
   ```

---

## 五、安裝 Claude Code

依照公司提供的 Claude Code 安裝方式完成安裝，並以你的帳號登入。

---

## 六、開始撰寫企劃書

1. 用 Claude Code 開啟 Clone 下來的資料夾
2. 在對話框輸入 `/slot-spec`，AI 會引導你逐步建立新企劃書
3. 企劃書建立後，可在資料夾內找到 `{代號}.md` 和 `{代號}.html` 兩個檔案
4. 用瀏覽器開啟 HTML 檔確認內容

---

## 七、同步更新（取得最新模板與工具）

當模板或工具有更新時，在 GitHub Desktop 中：

1. 確認左上角顯示的是這個 repo
2. 點擊上方 **Fetch origin**
3. 如果有更新，會出現 **Pull origin** 按鈕，點擊後即可取得最新版本

---

## 八、上傳你的企劃書

寫完或更新企劃書後，透過 GitHub Desktop 上傳：

1. 左側 **Changes** 欄會顯示你修改的檔案（打勾代表會上傳）
2. 左下角填入簡短說明（例如：`新增 JHS1075 初稿`）
3. 點擊 **Commit to main**
4. 點擊右上角 **Push origin** 完成上傳

---

## 常見問題

**Q：push 時出現錯誤，說沒有權限？**
確認子馨有將你的 GitHub 帳號加入 Collaborator。

**Q：HTML 沒有更新？**
在 Claude Code 對話中輸入「重建 HTML」，AI 會幫你執行。

**Q：Python 找不到？**
確認安裝時有勾選「Add Python to PATH」，或重新安裝一次。
