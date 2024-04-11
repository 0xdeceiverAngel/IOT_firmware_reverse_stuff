
# websec







# xss
ref
- https://www.securityverse.tw/index.php/2023/03/30/elementor-632/
- https://ithelp.ithome.com.tw/articles/10313080
- https://yu-jack.github.io/2017/10/20/secure-header/

類型
- 反射型
    - URL中嵌入惡意的JavaScript腳本
- 儲存型
    - 留言板、評論區
- DOM
    - 在JS載入網頁時，直接在網頁中嵌入夾帶惡意程式碼的DOM物件進行攻擊


預防方法
- 驗 iput, cookie, string, forms
- encode
- Content-Security-Policy（CSP
    - 指定允許腳本從哪些來源加載，以防止外部惡意腳本的注入
- X-XSS-Protection
    - 基本上可以被 Content-Security-Policy 取代
    - 如果瀏覽器偵測到 XSS 的攻擊，會根據設置的屬性做不同的反應
- WAF

# csrf Cross-Site Request Forgery
ref
- https://www.explainthis.io/zh-hant/swe/what-is-csrf
- https://tech-blog.cymetrics.io/posts/jo/zerobased-cross-site-request-forgery/

攻擊步驟
- User 訪問並登入 A 網站
- User 獲得 Cookie 並存至 User 瀏覽器
- User 在未登出 A 網站的情況下瀏覽 B 網站，接著 Hacker 以 B 網站的 Domain 以 A 網站給 User 的 Cookie 對 A 網站發送請求

預防方法
- 圖形驗證碼、簡訊驗證碼等
- CSRF token，驗證不看 cookie，動態請求 session
- SameSite cookies，限定 cookie 只能被自己網站用

# ssrf Server-side request forgery
ref
- 

![](https://www.imperva.com/learn/wp-content/uploads/sites/13/2021/12/How-Server-SSRF-works.png)

預防方法
- server 要寫好(？？