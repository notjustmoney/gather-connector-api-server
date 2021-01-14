from selenium import webdriver


def get_video_title_and_uri(keyword):
    target_uri = f'https://youtube.com/results?search_query={keyword}'
    driver_path = '/Users/jay/projects/gather-connector-api-server/lib/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')

    # singleton instance required
    driver = webdriver.Chrome(driver_path, options=options)

    driver.get(target_uri)
    target_elem = driver.find_element_by_css_selector('#video-title')
    video_title = target_elem.get_attribute('title')
    video_uri = target_elem.get_attribute('href')
    driver.quit()

    return video_title, video_uri

