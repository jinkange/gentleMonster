from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import random
import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import time

def chromeStart():
    try:
        # 크롬드라이버 옵션 설정
        options = Options()
        userCookieDir = os.path.abspath(f"./cookie")
        if os.path.exists(userCookieDir) == False:
          os.mkdir(userCookieDir)
          
        with open("./data/chrome.txt", "r+",encoding='utf-8') as chrome_dir:
          chrome = chrome_dir.readlines()
        
            
        if(chrome == ''):
          print("./data/chrome.txt 에 크롬의 위치를 입력 해주세요.")
          
        chrome_cmd = '\"'+chrome[0]+'\"  --remote-debugging-port=9224 --user-data-dir="'+str(userCookieDir)+'" --disable-gpu --disable-popup-blocking --disable-dev-shm-usage --disable-plugins --disable-background-networking'
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9224")
        p = subprocess.Popen(chrome_cmd, shell=True)

        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(e)
        input("아무키나 누르세요... ")
        
def htmlLoadingCheck(driver:webdriver, xpath):
    while 1:
        try:
            driver.execute_script("document.evaluate('"+xpath+"', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
            return
        except:
            time.sleep(1)
            try:
                driver.execute_script("document.evaluate('//*[@id=\"lastName\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")    
                return 1
            except:
                print()
                
def start():
  while True:
    goodUrl = input("구매할 상품 주소 : ")
    if goodUrl:
          print("주소 : ",goodUrl)
          break

  driver = chromeStart()

  #옵션값 확인 및 선택
  driver.get(goodUrl)
  print("로그인을 진행 해주세요.")
  try:
    option_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginBtn"]')))
    option_element.click()
  except Exception:
    print("로그인 확인..")


  # 로그인이 되길 기다려줘야하는데....
  #상품 주소일때 로그인 값이 없다면 그때 작동하도록
  while 1:
    if(driver.current_url in goodUrl):
      try : 
          element = driver.find_element(By.XPATH, '//*[@id="mypageBtn"]')
          if (element):
              #로그인되어있음
              driver.get(goodUrl)
              break
      except Exception:
          print()
      time.sleep(1)
  print("로그인 확인..")
  while 1:
    if(driver.current_url in goodUrl):
      try:
        # 해당 요소의 텍스트 가져오기
        element = driver.find_element(By.XPATH, "//*[contains(text(), '쇼핑백에 추가')]")
        print("상품 확인")
        element.click()
        break
      except:
        driver.refresh()
        time.sleep(3)


  while 1:
      try:
        # 해당 요소의 텍스트 가져오기
        element = driver.find_element(By.XPATH, "//*[contains(@class, 'cart_section_popup popup_wrap cart-layer open noti-type-scorll')]")
        print("쇼핑백 발견")
        break
      except:
        time.sleep(1)

  print("결제하기 클릭")
  element = driver.find_element(By.XPATH, "//*[contains(text(), '결제하기')]")
  element.click()
  
  while 1:
    try:
      # html 로딩 대기
      goods = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="go_to_payment"]')))
      if(goods):
        break
    except:
      time.sleep(1)
  
  #동의하기 클릭
  element = driver.find_element(By.XPATH, '//*[@id="privacy-policy"]')
  driver.execute_script("arguments[0].click();", element)
  
  #다음 단계로 클릭
  element = driver.find_element(By.XPATH, '//*[@id="go_to_payment"]')
  driver.execute_script("arguments[0].click();", element)
  
  while 1:
    try:
      # html 로딩 대기
      goods = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="payment-form"]/div[3]/div[4]/button[1]')))
      if(goods):
        break
    except:
      time.sleep(1)
  
  #네이버 페이 클릭
  element = driver.find_element(By.XPATH, '//*[@id="payment-naver"]')
  driver.execute_script("arguments[0].click();", element)
  
  #동의하기 클릭
  element = driver.find_element(By.XPATH, '//*[@id="privacy-policy"]')
  driver.execute_script("arguments[0].click();", element)
  
  #동의하기 클릭
  element = driver.find_element(By.XPATH, '//*[@id="payment-form"]/div[3]/div[4]/button[1]')
  driver.execute_script("arguments[0].click();", element)
  
  while 1:
    try:
      WebDriverWait(driver, 10).until(EC.url_contains('m.pay.naver.com'))
      print("원하는 주소가 포함된 페이지가 로드되었습니다.")
      break
    except:
      time.sleep(1)
  
  #카드 간편결제 클릭
  element = driver.find_element(By.XPATH, '//*[@id="card"]')
  driver.execute_script("arguments[0].click();", element)
  
  #결제 클릭
  element = driver.find_element(By.XPATH, '//*[@id="container"]/div[10]/div/div/a')
  driver.execute_script("arguments[0].click();", element)
  
  
  #새창 대기
  current_window = driver.current_window_handle
  # 새로운 창 핸들 찾기
  new_window = None
  while not new_window:
      for window_handle in driver.window_handles:
          if window_handle != current_window:
              new_window = window_handle
              driver.switch_to.window(window_handle)
              time.sleep(0.5)
              current_url = driver.current_url
              print("새창 찾기 창 주소: " + driver.current_url)
              if "https://new-m.pay.naver.com/"  in current_url:
                  print("찾는 주소가 열린 창입니다.")
                  break
              driver.switch_to.window(new_window)
          time.sleep(0.5)
  
  # iFrame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__tosspayments_connectpay_iframe__"]')))
  # driver.switch_to.frame(iFrame)
  
  # try:
  #     buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '바로구매')]")))
  #     #buy_button.click()
  #         # Click the element using JavaScript
  #     driver.execute_script("arguments[0].click();", buy_button)
  #     try:
  #       # 얼럿이 표시될 때까지 대기 (10초로 설정)
  #       WebDriverWait(driver, 0.1).until(EC.alert_is_present())
  #       # 얼럿 객체 가져오기
  #       alert = driver.switch_to.alert
  #       # 얼럿 텍스트 출력 (선택사항)
  #       print("Alert Text:", alert.text)
  #       # 얼럿 확인 버튼 클릭 (선택사항)
  #       alert.accept()
  #       # 옵션 선택 드롭다운을 찾음
  #       option_dropdown = driver.find_element(By.XPATH, "//select[@id='option1']")
  #       # '옵션 선택'을 제외한 옵션들을 찾아서 리스트에 저장
  #       available_options = option_dropdown.find_elements(By.XPATH, "./option[not(contains(text(), '옵션 선택'))]")
  #       # 재입고와 관련된 옵션을 제거
  #       available_options = [option for option in available_options if "재입고" not in option.text]
  #       # 랜덤으로 옵션 선택
  #       selected_option = random.choice(available_options)
  #       selected_option.click()
  #       buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '바로구매')]")))
  #       driver.execute_script("arguments[0].click();", buy_button)
  #       #buy_button.click()
  #     except Exception as e:
  #         # 얼럿이 표시되지 않은 경우 예외 처리
  #         print()
  # except Exception as e:
  #     print("바로구매 버튼을 클릭하는데 실패했습니다.")
  #     buy_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="buy_option_area"]/div[7]/div[1]/a')))
  #     buy_button.click()
  #     print(str(e))


  # while 1:
  #   try:
  #     # html 로딩 대기
  #     goods = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_pay"]')))
  #     if(goods):
  #       break
  #   except:
  #     time.sleep(1)
  
  # radio_button = driver.find_element(By.XPATH,'//*[@id="payment_btn0"]')
  #   # Click the radio button using JavaScript
  # driver.execute_script("arguments[0].click();", radio_button)
    
  
  # option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cardSwiper"]/div[2]')))
  # option_element.click()
  # time.sleep(1)
  # try:
  #   option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allCheckAgree"]')))
  #   option_element.click()
  # except:
  #   print()

  # option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_pay"]')))
  # option_element.click()    

  # try:
  #     # 얼럿이 표시될 때까지 대기 (10초로 설정)
  #     WebDriverWait(driver, 0.1).until(EC.alert_is_present())
  #     # 얼럿 객체 가져오기
  #     alert = driver.switch_to.alert
  #     # 얼럿 텍스트 출력 (선택사항)
  #     print("Alert Text:", alert.text)
  #     # 얼럿 확인 버튼 클릭 (선택사항)
  #     alert.accept()
  #     option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allCheckAgree"]')))
  #     option_element.click()
  #     option_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_pay"]')))
  #     option_element.click()    
  # except Exception as e:
  #     # 얼럿이 표시되지 않은 경우 예외 처리
  #     print("No alert found.", str(e))
  # #새창 대기
  # current_window = driver.current_window_handle
  # # 새로운 창 핸들 찾기
  # new_window = None
  # while not new_window:
  #     for window_handle in driver.window_handles:
  #         if window_handle != current_window:
  #             new_window = window_handle
  #             driver.switch_to.window(window_handle)
  #             time.sleep(0.5)
  #             current_url = driver.current_url
  #             print("새창 찾기 창 주소: " + driver.current_url)
  #             if "https://pay.musinsa.com/certify/req"  in current_url:
  #                 print("찾는 주소가 열린 창입니다.")
  #                 break
  #             driver.switch_to.window(new_window)
  #         time.sleep(0.5)

  # iFrame = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__tosspayments_connectpay_iframe__"]')))
  # driver.switch_to.frame(iFrame)
  # while 1:
  #   try:
  #     # html 로딩 대기
  #     goods = driver.find_elements(By.XPATH, '//*[@id="connectpay-portal-container"]/div/div/a[2]')
  #     if(goods):
  #       break
  #   except:
  #     time.sleep(0.1)

  # def click_number_keypad(driver, number):
  #     script = f"""
  #         var keypadElement = document.querySelector("#connectpay-portal-container > div > div");
  #         var numberButtons = keypadElement.querySelectorAll("a[data-virtual-keypad='{number}']");
  #         if (numberButtons.length > 0) {{
  #             var randomNumberButton = numberButtons[Math.floor(Math.random() * numberButtons.length)];
  #             randomNumberButton.dispatchEvent(new MouseEvent('mouseup', {{
  #                 bubbles: true,
  #                 cancelable: true,
  #                 view: window
  #             }}));
  #         }}
  #     """
  #     driver.execute_script(script)
  # script = f"""
  #         var keypadElement = document.querySelector("#connectpay-portal-container > div > div");
  #         return keypadElement.querySelectorAll("a");
  #     """
  # a_elements = driver.execute_script(script)
  # with open("./data/password.txt", "r", encoding='utf-8') as password_file:
  #   password_str = password_file.readline().strip()

  # for password in password_str:  
  #   for a_element in a_elements:
  #     virtual_keypad_value = a_element.get_attribute("data-virtual-keypad")
  #     if(password == a_element.text):
  #       click_number_keypad(driver, virtual_keypad_value)
  #       break

  # print("구매 완료...")
  time.sleep(60)
  
start()
