#!/usr/bin/env python3
"""
Chrome에서 인스타그램 쿠키를 추출하는 스크립트
"""

import browser_cookie3
import http.cookiejar

def export_instagram_cookies():
    try:
        print("Chrome에서 쿠키 추출 중...")
        
        # Chrome 쿠키 가져오기
        cookies = browser_cookie3.chrome(domain_name='instagram.com')
        
        # Netscape 형식으로 저장
        cookie_jar = http.cookiejar.MozillaCookieJar('instagram_cookies.txt')
        
        for cookie in cookies:
            cookie_jar.set_cookie(cookie)
        
        cookie_jar.save(ignore_discard=True, ignore_expires=True)
        
        print("✅ 쿠키가 'instagram_cookies.txt'에 저장되었습니다!")
        print("\n이제 서버를 실행하세요: python3 app.py")
        
    except Exception as e:
        print(f"❌ 에러: {e}")
        print("\n해결 방법:")
        print("1. Chrome에서 instagram.com에 로그인")
        print("2. pip install browser-cookie3 실행")
        print("3. 다시 이 스크립트 실행")

if __name__ == '__main__':
    export_instagram_cookies()
