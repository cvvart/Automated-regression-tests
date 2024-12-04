#import curses
import functools
import subprocess
import win32api
import win32con
import time
from matplotlib.backend_bases import MouseEvent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By                         
from selenium.webdriver.support.ui import WebDriverWait   
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC    
import pyautogui 
import dis
from shutil import copyfile
import SimilarityIndex                  
import glob                    
from selenium.webdriver.chrome.options import Options
from PIL import Image 
import shutil
import os
import time
# from selenium.webdriver.common.touch_actions import TouchActions
import tkinter as tk
#from win32api import GetSystemMetrics
#import mouse
from multiprocessing import Process
import clipboard
import sys
from selenium.webdriver.common.keys import Keys
import skimage
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


pyautogui.FAILSAFE = False
hostServer =None
driver = None
ringName = None
webBrowser = ""
failsnapmax = 1
loadTime = None
maxWaitTime = 5
folder = None
model = None
beforeInnerHeight =0
beforeOuterHeight =0
navigatorFlyTime = 5

buttons =   { 
        "menu_open_hamburger": lambda : driver.find_element("id","Menu-id-visualization-toolbar"),
        "menu_close_hamburger": lambda : driver.find_elements("xpath","//div[contains(@class, 'visualization-main-menu__header__close')]")[0],
        "propcard_open_close_arrow": lambda : driver.find_elements("xpath","//div[contains(@class,'uxt-icon-button visualization-details-card__card__header__collapse')]")[0],
        "prop_open_close_arrow": lambda : driver.find_elements("xpath","//div[contains(@class,'uxt-property-section')]")[0],
        "propcard_close": lambda : driver.find_elements("xpath","//div[contains(@class,'uxt-icon-button visualization-details-card__card__header__close')]")[0] ,
        "signin_out" : lambda : driver.find_element_by_class_name("visualization-user-info__action"),
        "settings_back": lambda :driver.find_element("xpath",'//div[@id="Back-id-settings-menu"]'),           
        "settings_close_x" : lambda :driver.find_element("xpath",'//div[@id="visualization-settings-menu-close-icon"]'),
        "home_taskbar" : lambda : driver.find_elements("class",'uxt-list-item uxt-list-item--single-line')[1],
        "fit_taskbar" : lambda : driver.find_elements_by_class_name('uxt-list-item uxt-list-item--single-line')[2],
        "clip_taskbar" : lambda : driver.find_elements_by_class_name('uxt-list-item uxt-list-item--single-line')[3],
        "measurement_taskbar": lambda : driver.find_elements_by_class_name('uxt-icon__content__svg-wrapper')[4],
        "walk-view":lambda:driver.find_elements("xpath","//div[contains(@class, 'visualization-toggle-icon-button')]//*[name()='svg']")[0],
        "navigator-2d":lambda:driver.find_elements("xpath","//div[contains(@class, 'visualization-toggle-icon-button')]//*[name()='svg']")[1],
        "config_menu": lambda:  driver.find_elements("xpath","//img[@alt='my image']")[0],
        "file_storage": lambda:  driver.find_element("xpath",("//*[contains(text(), 'File Storage')]")),
        "connect": lambda: driver.find_element("xpath",("//div[contains(@class, 'sa-modal-footer')]//*[contains(text(), 'Connect')]")),
        "feature_menu": lambda : driver.find_element("id","menubutton")
        } 

environment_tab_buttons = {
        "presets": lambda: driver.find_elements("xpath","//div[contains(@class, 'environment-tabs')]//*[name()='svg']")[0],
        "lighting": lambda: driver.find_elements("xpath","//div[contains(@class, 'environment-tabs')]//*[name()='svg']")[1],
        "background": lambda: driver.find_elements("xpath","//div[contains(@class, 'environment-tabs')]//*[name()='svg']")[2],
        "surface": lambda: driver.find_elements("xpath","//div[contains(@class, 'environment-tabs')]//*[name()='svg']")[3],
        "environment_close": lambda: driver.find_element("xpath",("//div[contains(@class,'environment-tabs')]/span[contains(@class,'environment-close-container')]/div/div"))
    }

background_buttons= {
        "color": lambda: driver.find_elements("xpath","//div[contains(@class, 'background-content-item')]//*[name()='svg']")[0],
        "skybox": lambda: driver.find_elements("xpath","//div[contains(@class, 'background-content-item')]//*[name()='svg']")[1],
        "gradient": lambda: driver.find_elements("xpath","//div[contains(@class, 'background-content-item')]//*[name()='svg']")[2]
    }

setUpCount = 0

def connect(n = None):
    connect_base_xpath = "//div[contains(@class, 'visualization-connect-info-root')]//*[contains(text(), 'Connect')]/../.."
    if n!= None:
        menu_xpath =f"(//*[@id='Menu-id-visualization-toolbar'])[{n}]"
        file_storage= "//*[contains(text(), 'File Storage')]"
        connect_xpath="//div[contains(@class, 'visualization-connect-info-root')]//*[contains(text(), 'Connect')]/../.."
        connect_button_xpath="//div[contains(@class, 'sa-modal-footer')]//*[contains(text(), 'Connect')]"
    else:
        menu_xpath ="//*[@id='Menu-id-visualization-toolbar']"
        file_storage="//*[contains(text(), 'File Storage')]"
        connect_xpath="//div[contains(@class, 'visualization-connect-info-root')]//*[contains(text(), 'Connect')]/../.."
        connect_button_xpath="//div[contains(@class, 'sa-modal-footer')]//*[contains(text(), 'Connect')]"

    # Wait for the element to be present and click it
    menu = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, menu_xpath)))
    menu.click()
    time.sleep(5)
    connect = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, connect_xpath)))
    connect.click()
    time.sleep(1)
    file_storage = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, file_storage)))
    file_storage.click()
    time.sleep(2)
    connect_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, connect_button_xpath)))
    connect_button.click()
    # buttons['menu_open_hamburger']().click()
    # time.sleep(1)
    # #WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "visualization-connect-info"))).click()
    # item = driver.find_element("xpath",("//div[contains(@class, 'visualization-connect-info-root')]//*[contains(text(), 'Connect')]/../.."))                                  
    # item.click()
    # time.sleep(1)
    # buttons["file_storage"]().click()
    # time.sleep(1)
    # buttons["connect"]().click()


def toggleCustomOption(option):
    # driver.execute_script("document.getElementsByClassName('uxt-modal')[0].style.display = 'none';")
    if buttons['menu_close_hamburger']().is_displayed():
        buttons['menu_close_hamburger']().click()
    time.sleep(2)
    buttons["config_menu"]().click()
    time.sleep(.5)
    driver.find_elements("xpath","//div[contains(@class,'sidenav')]//*[contains(text(), '%s')]" % option)[0].click()
    buttons["config_menu"]().click()
    time.sleep(3)

def drag_walkview():
    walkview = driver.find_element("id","Walking-View-id-navigation")
    #walkview=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,"Walking-View-id-navigation")))
    time.sleep(5)
    ActionChains(driver).drag_and_drop(walkview,canvas).perform()
    time.sleep(5)

def measure_fab(function):
    measure_fab_buttons = {
        "close_fab":lambda : driver.find_elements("xpath","//div[contains(@class,'visualization-fab-toolbar-fab')]")[0],
        "open_fab":lambda :  driver.find_elements("id",'Measure-id-fab-toolbar-fab')[0],
        #"open_fab":lambda :  driver.find_elements("id","fabMeasureContainer"),
        "placementmode":lambda : driver.find_element("id","Place Point-id-Measure-fab-toolbar"),
        "delete":lambda : driver.find_element("id","Trash-id-Measure-fab-toolbar"),
        "hide":lambda : driver.find_element("id","Hide-id-Measure-fab-toolbar")
    }
    measure_fab_buttons[function]().click()

def clip_fab(function):
    clip_fab_buttons = {
        "close_fab":lambda : driver.find_elements("xpath","//div[contains(@class,'visualization-fab-toolbar-fab')]")[0],
        "open_fab":lambda :  driver.find_element("xpath",("//div[contains(@id,'Clip-id-fab-toolbar') ]")),
       # "open_fab":lambda :  driver.find_element("xpath",("//div[contains(@class,'visualization-fab-toolbar-fab visualization-fab-toolbar-fab--open') and contains(@title, 'Clip')]"),
        "invert":lambda : driver.find_element("id","Invert-id-Clip-fab-toolbar"),
        "delete":lambda : driver.find_element("id","Delete Plane-id-Clip-fab-toolbar"),
        "reset":lambda : driver.find_element("id","Reset-id-Clip-fab-toolbar")
    }
    clip_fab_buttons[function]().click()

def getModel():
    return model

def modelLoadWaitTime():
    global loadTime
    print("printloadTime: " + str(time.time()-loadTime))
    if(time.time()-loadTime > 150):
        print("program exited as the model is not loading fully")
        sys.exit(1)
    folder = getCurrentFolder()
    benchmark = "b_openModel.png"
    # check_GVC_window_size()
    ActionChains(driver).send_keys("g").perform() 
    time.sleep(3)
    for filename in os.listdir('%s/Results/' %folder):
        print(filename)
        root,ext = os.path.splitext(filename)
        if root.startswith('snapshot') and ext =='.png':
            similarity = SimilarityIndex.computeSSIM('%s\\Benchmark_images\\%s\\%s' % (folder,model,benchmark), '%s\\Results\\%s' % (folder,filename), False)
            print(similarity)
            if(similarity>0.98):
                os.remove('%s/Results/%s' %(folder,filename))
                time.sleep(1)
                return 0
            else:
                os.remove('%s/Results/%s' %(folder,filename))
                time.sleep(1)
                modelLoadWaitTime()
    
def getCurrentFolder():
	folder = dis.code_info(getCurrentFolder).split('\n')[1].split()[1:]
	folder = " ".join(folder)
	folder = os.path.dirname(folder)
	return folder

def start_browser(args):
    global webBrowser
    global buttons
    global driver
    global link
    folder = getCurrentFolder()

    # linkDefaults = {
    #             "canary":"http://argo.canary-staging.ingrnet.com/argoweb/",
    #             "ida":"http://argo.ida-staging.ingrnet.com/argoweb/",
    #             "external": "https://argostaging.hexagonppm.com/argoweb/"
    #             #"external":"http://localhost/projects/satya/"
    #             }
    # ring = args.ring
    # if(ring == None):
    #     link = args.link
    # else:
    #     link = linkDefaults[ring]
    if (args.link == None):
        version = args.version
        if "-RC" in version or "-HF" in version:
            officialVersion = re.sub("-RC.*|-HF.*", "", version)
            link= 'https://gvc.ingrnet.com/gvcreact/%s/%s/' % (officialVersion, version)
        else:
            link='https://gvc.ingrnet.com/gvcreact/%s/' % (version)
    else:
        link = args.link
    #if(args.webdriverpath == None):
        #driverlocation = "%s/tools/chromedriver.exe" %folder
    #else:
        #driverlocation = args.webdriverpath
    
    chrome_options = Options()
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--disable-extensions')
    # chrome_options.add_argument("touch-events")
    # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_experimental_option('w3c', False)

    prefs = {'download.default_directory': '%s\\Results' %folder, 'profile.default_content_setting_values.automatic_downloads': 1}
    chrome_options.add_experimental_option('prefs', prefs)
 
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option('useAutomationExtension', False)


    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    # driver.execute_script("document.body.style.zoom = 0.5")
    time.sleep(15)
    found = False

    for i in range(0,3):
        try:
            assert "GVC Test App" in driver.title      
        except Exception as e:
            print("Attempt failed, trying again. %s" % e)
            time.sleep(10)
            continue
        found = True
        break
    assert found, "Site failed to load. Attempted %d of %d times" % (i+1, 3)
    return driver

def setup(args):
    global driver
    global model
    model = args.modelName
    folder = getCurrentFolder()
    driver = start_browser(args)

def finishTests():
    if(driver != None):
        driver.close()
        driver.quit()

def check_GVC_window_size(driver):
    global canvas
    canvas=driver.find_element("xpath",('//*[@id="mycanvas-0"]'))
    new_width = 960
    new_height = 640
    driver.execute_script(f"window.innerWidth = {new_width}; window.innerHeight = {new_height};")#previously working for 16.4.8
    #driver.execute_script(f"document.getElementById('basicsContainer').style.width = '{new_width}px'; document.getElementById('basicsContainer').style.height = '{new_height}px';")
    time.sleep(1)
    
def open_model(wait=True):
    global loadTime
    check_GVC_window_size(driver)
    buttons['menu_open_hamburger']().click()
    time.sleep(2)
    WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
    time.sleep(2)

    if(model.startswith("3D")):
        time.sleep(3)
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="3D Models"]'))).click()
        try:
            element=driver.find_element("xpath",'//*[@title="%s"]'% model)
            element.click()
        except NoSuchElementException:
            find_model=driver.find_element("xpath",'//*[@title="3D-Refining (Pack-File)"]')
            driver.execute_script("arguments[0].scrollIntoView(true);",find_model) #scroll and make the element found to be visible on top of list
            time.sleep(.5)
            element=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="%s"]'% model)))
            element.click()
            time.sleep(3)

    if(model.startswith("2D")):
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="2D Drawings"]'))).click()
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="%s"]'% model))).click()
            time.sleep(2)

    if (wait):
        loadTime = time.time()
        modelLoadWaitTime()
    else:
        time.sleep(10)

#To open any 3D model use this method by providing correct model name as argument value       
def open_3D_model(model_3d, n=None):
    global loadTime
    # check_GVC_window_size()
    if n!= None:
        menu_xpath =f"(//*[@id='Menu-id-visualization-toolbar'])[{n}]"
        open_xpath= f"(//*[@id='Open-id-main-menu'])[{n}]"
    else:
        menu_xpath ="//*[@id='Menu-id-visualization-toolbar']"
        open_xpath ="//*[@id='Open-id-main-menu']"
    menu = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, menu_xpath)))
    menu.click()  
    time.sleep(5)
    open_m = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, open_xpath)))
    open_m.click()
    time.sleep(2)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="3D Models"]'))).click()
    item = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="%s"]'% model_3d)))
    item.click()

#To open any 2D drawing use this method by providing correct drawing name as argument value  
def open_2D_drawing(drawing,n = None):
      #Opens main menu
    if n!= None:
        menu_xpath =f"(//*[@id='Menu-id-visualization-toolbar'])[{n}]"
        open_xpath= f"(//*[@id='Open-id-main-menu'])[{n}]"
    else:
        menu_xpath ="//*[@id='Menu-id-visualization-toolbar']"
        open_xpath ="//*[@id='Open-id-main-menu']"
    menu = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, menu_xpath)))
    menu.click()  
    time.sleep(5)
    open_m = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, open_xpath)))
    open_m.click()
      #listitems = driver.find_elements("xpath",'//div[contains(@id,"Models-id-main-menu")]//*[contains(text(), "Models")]')[0]
    time.sleep(2)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="2D Drawings"]'))).click()
    item =WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="%s"]'% drawing)))
    item.click()
    time.sleep(5)

def open_append(model,list_items=None):#list_items shall consists of list of models to be de-appended(ex: structure)
    buttons['menu_open_hamburger']().click()
    time.sleep(0.5)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
    time.sleep(0.5)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="APPEND"]'))).click()
    time.sleep(0.5)
    item = driver.find_element("xpath","//div[contains(@class, 'UxtRadioButton-label') and text()='%s']"% model)
    item.click()
    time.sleep(1)
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//div[contains(@class, 'UxtCheckbox-root-UxtTreeItem-checkbox')]"))).click()
    time.sleep(1)
    if(list_items != None):
        driver.find_element(By.XPATH, "//div[contains(@class, 'UxtIcon-root-UxtIcon-clickable-UxtTreeItem-chevron-UxtTreeItem-collapsible')]//*[name()='svg']").click()
        time.sleep(1)
        for i in list_items:
            time.sleep(3)
            driver.find_element(By.XPATH, "//div[contains(@class, 'UxtTreeItem-text') and contains(text(), '%s')]" % i).click()
    time.sleep(0.5)       
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'sa-modal-close-button') and text()='×']"))).click()
    time.sleep(5)

def initialize():
    print("under initialize")
    global beforeInnerHeight
    global beforeOuterHeight
    global innerWidth
    global innerHeight
    global folder

    folder = getCurrentFolder()
    beforeInnerHeight = driver.execute_script('return window.innerHeight')
    beforeOuterHeight = driver.execute_script('return window.outerHeight')
    print(beforeInnerHeight,beforeOuterHeight) #799 920
    innerWidth=driver.execute_script('return window.innerWidth')
    innerHeight=driver.execute_script('return window.innerHeight')
    print(innerWidth,innerHeight) #960 640
    time.sleep(10)
    #toggleCustomOption("3D Models Pack")
    #toggleCustomOption("2D Drawings Pack")
    connect()
    open_model(False)
    time.sleep(5)
    resize_window(driver)
    current_url = driver.current_url
    print("Current URL:", current_url)
    if current_url != link:
        raise WebDriverException("Window with title 'GVC Test APP' not found or has crashed.")
    ActionChains(driver).send_keys("g").perform()
    # check_GVC_window_size()
    time.sleep(1)
    for filename in os.listdir('%s/Results/' %folder):
        root,ext = os.path.splitext(filename)
        if root.startswith('snapshot') and ext =='.png':
            os.remove('%s/Results/%s' %(folder,filename))

def reload():
    driver.refresh()
    check_GVC_window_size(driver)
    resize_window(driver)
    time.sleep(3)
    connect()
  
def authenticate_SAM():
    buttons['menu_open_hamburger']().click()    
    time.sleep(3)
    buttons['signin_out']().click()
    if(webBrowser == 'safari'):
        time.sleep(15)
    try:
        WebDriverWait(driver,40).until(
            EC.title_contains(("Smart API"))      
            )
        if(webBrowser == 'safari'):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))) 
        else:        
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID, "username")))
    except: 
        assert False, "Failed to locate authentication elements on page." 
    else:
        clearlen = 30 
        for i in range(0,clearlen):
            driver.find_element("id","username").send_keys(Keys.BACKSPACE)

        time.sleep(.5)
        if(ringName == 'external'):
                driver.find_element("id","username").send_keys("hexagonlive")
        else:
                driver.find_element("id","username").send_keys("ArgoQA")
        time.sleep(.5)
        for j in range(0,clearlen):
            driver.find_element("id","password").send_keys(Keys.BACKSPACE)
        time.sleep(.5)
        if(ringName== 'external'):
                driver.find_element("id","password").send_keys("PPMArgo.1")
        else:
                driver.find_element("id","password").send_keys("Test.hard0")
        driver.find_element("id","password").send_keys(Keys.RETURN)
            

        WebDriverWait(driver,10).until(
            EC.title_contains(("Project Argo"))
            )    
        time.sleep(5)
        # check_GVC_window_size()

def logout():
    if buttons['menu_open_hamburger']().is_displayed() and not buttons['menu_close_hamburger']().is_displayed():
        buttons['menu_open_hamburger']().click()
    time.sleep(.5)
    buttons['signin_out']().click()
    try:
        WebDriverWait(driver,30).until(
            EC.title_contains(("Smart API"))        
            )
    finally:
        time.sleep(1)
        
def generateBenchmark(testcasename):
    if not (os.path.exists('%s/Results' % folder)):
	    os.mkdir("%s/Results" % folder)
    benchmark = "b_" + testcasename + ".png"
    ActionChains(driver).send_keys('g').perform()
    time.sleep(3)
    for filename in os.listdir("%s/Results" %folder):
        root,ext = os.path.splitext(filename)
        if root.startswith('snapshot') and ext =='.png':
            os.rename("%s/Results/%s" %(folder,filename),"%s/Results/%s" %(folder,benchmark))
    time.sleep(2)

# def rename_existing_screenshot(folder, output, attempt=1):
#     base, ext = os.path.splitext(output)
#     new_output = f"{base}_attempt_{attempt}{ext}"
#     while os.path.exists(os.path.join(folder, "Results", new_output)):
#         attempt += 1
#         new_output = f"{base}_attempt_{attempt}{ext}"
#     os.rename(os.path.join(folder, "Results", output), os.path.join(folder, "Results", new_output))
#     return new_output
def rename_existing_screenshot(folder, output, attempt=1):
    base, ext = os.path.splitext(output)
    original_output_path = os.path.join(folder, "Results", output)

    # Ensure the original file exists before renaming
    if not os.path.exists(original_output_path):
        print(f"Original file {output} not found in {folder}/Results. Cannot rename.")
        return output  # Return the original output name as fallback

    new_output = f"{base}_attempt_{attempt}{ext}"
    new_output_path = os.path.join(folder, "Results", new_output)

    # Increment attempt number until we find a unique name
    while os.path.exists(new_output_path):
        attempt += 1
        new_output = f"{base}_attempt_{attempt}{ext}"
        new_output_path = os.path.join(folder, "Results", new_output)

    try:
        # Rename the file to avoid conflict
        os.rename(original_output_path, new_output_path)
        print(f"Renamed {output} to {new_output}")
        return new_output  # Return the new output name
    except Exception as e:
        print(f"Error renaming file {output} to {new_output}: {e}")
        raise

#def snapCompare(testcasename,benchMark = None,threshold=.03):
    if(benchMark==None):
        benchmark = "b_" + testcasename + ".png"
    else:
        benchmark = "b_" + benchMark + ".png"
    output = "o_" + testcasename + ".png"
    folder = getCurrentFolder()
    for filename in os.listdir('%s/Results/' %folder):
        root,ext = os.path.splitext(filename)
        if root.startswith('snapshot') and ext =='.png':
            os.remove('%s/Results/%s' %(folder,filename))
    time.sleep(1)
    ActionChains(driver).send_keys('g').perform()
    time.sleep(3)
    for filename in os.listdir("%s/Results" %folder):
        root,ext = os.path.splitext(filename)
        if root.startswith('snapshot') and ext =='.png':
            os.rename("%s/Results/%s" %(folder,filename),"%s/Results/%s" %(folder,output))
    time.sleep(2)
    a = SimilarityIndex.computeSSIM('%s\\Benchmark_images\\%s\\%s' % (folder,model,benchmark), '%s\\Results\\%s' % (folder,output), False)
    SimilarityIndex.generateDiffImage('%s/Benchmark_images/%s/%s' % (folder,model,benchmark), '%s/Results/%s' % (folder,output), '%s/Difference/dif_%s.gif' % (folder,testcasename))
    print("a is ", 1-float(a))
    if 1-float(a) > threshold: 
        imageDif = Image.open('%s/Difference/dif_%s.gif' % (folder,testcasename))
        imageBench = Image.open('%s/Benchmark_images/%s/%s' % (folder,model,benchmark))
        imageSnap = Image.open('%s/Results/%s' % (folder,output))
        SimilarityIndex.generateCompareResultImg(imageBench,imageSnap,imageDif,float(1-float(a))*100,"Snapshot: %s" % output,'%s/Failures/compare_%s.png' % (folder,testcasename))
        assert False, ('%.2f percent structural inconsistencies found in image %s. This is larger than the set threshold.' %(float(1-float(a))*100, output))

def snapCompare(testcasename, benchMark=None, threshold=.00):
    if benchMark is None:
        benchmark = "b_" + testcasename + ".png"
    else:
        benchmark = "b_" + benchMark + ".png"
    output = "o_" + testcasename + ".png"
    folder = getCurrentFolder()

    # Remove old snapshots
    for filename in os.listdir('%s/Results/' % folder):
        root, ext = os.path.splitext(filename)
        if root.startswith('snapshot') and ext == '.png':
            os.remove('%s/Results/%s' % (folder, filename))

    time.sleep(1)
    ActionChains(driver).send_keys('g').perform()
    time.sleep(3)

    # Rename existing screenshot if it exists
    for filename in os.listdir("%s/Results" % folder):
        root, ext = os.path.splitext(filename)
        if root.startswith('snapshot') and ext == '.png':
            if os.path.exists(os.path.join(folder, "Results", output)):
                output = rename_existing_screenshot(folder, output)
            os.rename("%s/Results/%s" % (folder, filename), "%s/Results/%s" % (folder, output))

    time.sleep(2)
    a = SimilarityIndex.computeSSIM('%s\\Benchmark_images\\%s\\%s' % (folder, model, benchmark), '%s\\Results\\%s' % (folder, output), False)
    SimilarityIndex.generateDiffImage('%s/Benchmark_images/%s/%s' % (folder, model, benchmark), '%s/Results/%s' % (folder, output), '%s/Difference/dif_%s.gif' % (folder, testcasename))
    print("a is ", 1 - float(a))

    if 1 - float(a) > threshold:
        imageDif = Image.open('%s/Difference/dif_%s.gif' % (folder, testcasename))
        imageBench = Image.open('%s/Benchmark_images/%s/%s' % (folder, model, benchmark))
        imageSnap = Image.open('%s/Results/%s' % (folder, output))
        SimilarityIndex.generateCompareResultImg(imageBench, imageSnap, imageDif, float(1 - float(a)) * 100, "Snapshot: %s" % output, '%s/Failures/compare_%s.png' % (folder, testcasename))
        assert False, ('%.2f percent structural inconsistencies found in image %s. This is larger than the set threshold.' % (float(1 - float(a)) * 100, output))

def snapshot(output = None, advanceCounter = True): 
    folder = getCurrentFolder()
    output = output+".png"
    if(output == None):
        output = output+".png"
        snapshot.counter += 1
        assert driver.get_screenshot_as_file('%s/Results/Screenshot_%d.png' % (folder,snapshot.counter) ), "Failed to take screenshot and save into {}".format(folder)
    else: 
        if(advanceCounter):
            if(snapshot.failsnapcount < failsnapmax):
                snapshot.failsnapcount += 1
                assert driver.get_screenshot_as_file('%s/Failures/%s' % (folder,output) ), "Failed to take screenshot and save into {}".format(folder)
        else:
            assert driver.get_screenshot_as_file('%s/Failures/%s' % (folder,output) ), "Failed to take screenshot and save into {}".format(folder)            
snapshot.counter = 0
snapshot.failsnapcount = 0

def changeImageName(imageName):
    folder = getCurrentFolder()
    for filename in os.listdir(folder):
        root,ext = os.path.splitext(filename)
        if root.startswith('snapshot') and ext =='.png':
            os.rename("%s/%s" %(folder,filename),"%s/%s" %(folder,imageName))

# select the item from tool bar and perfroms a click
def selectFromToolbar(itemStr):
    item = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="%s"]' %itemStr)))                                   
    item.click()
    time.sleep(.5)

def selectFromMenu(menuItemStr):
    menuitem='"'+menuItemStr+'"'
    if buttons['menu_open_hamburger']().is_displayed() and not buttons['menu_close_hamburger']().is_displayed():
        buttons['menu_open_hamburger']().click()
    time.sleep(1)
    element=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'visualization-main-menu-contentCommands')]//div[@id=%s]" % menuitem)))
    element.click()
    time.sleep(1)

    if buttons['menu_close_hamburger']().is_displayed():
        buttons['menu_close_hamburger']().click()
    time.sleep(.5)
    
def multiple_clicks():
    for i in range(0,5):
        ActionChains(driver).click(canvas).perform()        
        time.sleep(0.2)

#This method performs mouse movement on the center of canvas
def move_to_center():
    ActionChains(driver).move_to_element(canvas).perform()

#This method performs mouse movement to the center of canvas and then by an offset
def move_to_offset(x,y):
    ActionChains(driver).move_to_element(canvas).perform()
    ActionChains(driver).move_by_offset(x,y).perform()

# This methods performs a mouse click on the center of canvas
def click_center(): # 480,320
    ActionChains(driver).click(canvas).perform()        
    time.sleep(2)

def left_click():
    ActionChains(driver).click().perform()        

def click_Offset(x,y):
    ActionChains(driver).move_to_element(canvas).perform()
    ActionChains(driver).move_by_offset(x,y).click().perform()

def object_click():
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"mycanvas-0"))).click()   

# This method creates a measurement by placing two points on th model. 
def createMeasure():
    click_center() # click on center of canvas to place a point
    for key in ['j','j']: # to change the position of the model and place a new point
        for i in range(1,4):
            ActionChains(driver).send_keys(key).perform()
        click_center() # click to place a new point

def createMeasure1(keys={},initial_measure=True):
    """
    @param keys: Input key strokes to be executed before creating measure
            to change the screen position
            Example: {'c':4,'j':3}
    @param initial_measure: Used to say the function if this is the first measure.
                    If set to False,    selectFromMenu('Measure') is not called.
    """
    for key,val in keys.items():    #Iterate through the input keys dictionary
        pressKey(key,val)
    if initial_measure : #Select Measure menu if this is the first measure
        selectFromToolbar('Measure-id-visualization-toolbar') # measure is selected from main menuu
    time.sleep(2)
    click_center() # click on center of canvas to place a point
    for key in ['j']: # to change the position of the model and place a new point
        for i in range(1,7):
            ActionChains(driver).send_keys(key).perform()
            time.sleep(0.1)
        click_center() # click to place a new point
    time.sleep(0.5)

# This method creates a measurement by using createMeasure() method and then hides it using hide icon from fab tool bar
def hideMeasure():
    time.sleep(2)
    measure_fab("hide") # hides measure
    time.sleep(0.5)
    measure_fab("close_fab") # close fab
    time.sleep(0.5)

# This method creates a measurement using createMeasure() method and disbles it.	
def disableMeasure():
    time.sleep(1)
    driver.find_element("id",'Measure-id-visualization-toolbar').click() #disables measure from ux tool at the top

# This methods creates a measurement and then deletes it
def deleteMeasure():
    driver.find_element("xpath",('//*[@id="Place Point-id-Measure-fab-toolbar"]')).click()
    time.sleep(0.5)
    for key in ['l']:  # to move the model, to select the created measurement
        for i in range(1,4):
            ActionChains(driver).send_keys(key).perform()
        click_center() # Click center to select the measure line
    driver.find_element("id","Hide-id-Measure-fab-toolbar").click() # clicks delete icon on the fab tool bar

def isolate():
    click_center() # clicks center to select the object
    selectFromMenu("Isolate-id-main-menu") # select isolate from main menu
    time.sleep(3)
    
# def touch():
#     action = TouchAction(driver)
#     action.tap(canvas).perform()
#     #TouchActions(driver).tap(canvas).perform()
#     TouchActions(driver).flick_element(canvas,50,50,1)
#     time.sleep(1)

def dragRotate():
    afterinnerHeight = driver.execute_script('return window.innerHeight')
    downloadbarHeight = beforeInnerHeight-afterinnerHeight
    start_height = beforeOuterHeight-afterinnerHeight-downloadbarHeight
    canvasHeight = canvas.size["height"]
    canvasWidth = canvas.size["width"]
    bitwidth = int(canvasWidth/4)   #bitWidth * 4 = canvasWidth
    start_x = bitwidth
    start_y = start_height + int(canvasHeight/2)
    end_x = bitwidth * 3
    pyautogui.moveTo(start_x,start_y)
    pyautogui.dragTo(end_x,start_y,duration=3)
    time.sleep(3)

# This method checks for undo functionality for chnage in camera positions using navigation keys
def undo():
    selectFromToolbar("Home-id-visualization-toolbar")
    keys = ['a','e','d','c']
    for key in keys:
            ActionChains(driver).send_keys(key).perform()
            time.sleep(1)
    for i in range(0,len(keys)):
        selectFromMenu("Undo-id-main-menu")
        time.sleep(3)
        position = "undoPosition-"+str(i+1)
        snapCompare(position)

# This method checks for redo functionality for chnage in camera positions using navigation keys
def redo():
    selectFromToolbar("Home-id-visualization-toolbar")
    keys = ['j','i','l','k']
    step = 1
    for key in keys: # chnages the state of the model
        ActionChains(driver).send_keys(key).perform()
        time.sleep(2)
        position  = "RedoState-" + str(step) 
    for i in range(0,len(keys)): # To perform undo
        selectFromMenu("Undo-id-main-menu")
        time.sleep(1)
    for i in range(0,len(keys)): # To perform Redo
        selectFromMenu("Redo-id-main-menu")
        time.sleep(3)
        position = "RedoPosition-"+str(i+1)
        snapCompare(position)

def sethome():
    selectFromToolbar("Home-id-visualization-toolbar")
    for i in range(1,10):
        ActionChains(driver).send_keys('a').perform()
        time.sleep(0.5)
    for i in range(1,10):
        ActionChains(driver).send_keys('w').perform()
        time.sleep(0.5)
    selectFromMenu("Set Home-id-main-menu")
    for i in range(1,10):
        ActionChains(driver).send_keys('d').perform()
        time.sleep(0.5)
    for i in range(1,10):
        ActionChains(driver).send_keys('s').perform()
        time.sleep(0.5)
    time.sleep(2)
    selectFromToolbar("Home-id-visualization-toolbar")
    time.sleep(5)

def resethome():
    sethome()
    selectFromMenu("Reset Home-id-main-menu")
    time.sleep(5)
        
def fit_to_model():
    WebDriverWait(driver,40).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="mycanvas-0"]')))
    pyautogui.moveTo(int(canvas.size["width"]/2),int(canvas.size["height"]/2))
    time.sleep(0.5)
    pyautogui.dragTo(int(canvas.size["width"]*3/4),int(canvas.size["height"]/3),duration=2,button='left')
    fit=driver.find_element("id","Fit-id-visualization-toolbar")
    WebDriverWait(driver,40).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="Fit-id-visualization-toolbar"]')))
    fit.click()
    time.sleep(5)

def clipping_plane_adjustment_plane1():
    time.sleep(1)
    pyautogui.moveTo(int(canvas.size["width"]/1.5),int(canvas.size["height"]/1.5+200))
    time.sleep(5)
    pyautogui.dragTo(int(canvas.size["width"]/2),int(canvas.size["height"]+85),duration=2,button='left')
        
def clipping_plane_adjustment_plane2():
    # for i in range(1,15):
    #     ActionChains(driver).send_keys('d').perform()
    pyautogui.moveTo(int(canvas.size["width"]/1.5+80),int(canvas.size["height"]/2+120))
    pyautogui.dragTo(int(canvas.size["width"]*1.8),int(canvas.size["height"]/8),duration=1,button='left')

def clipping_plane_adjustment_plane3():
    # for i in range(1,15):
    #     ActionChains(driver).send_keys('a').perform()
    pyautogui.moveTo(int(canvas.size["width"]/2-50),int(canvas.size["height"]/2+150))
    pyautogui.dragTo(int(canvas.size["width"]*1/7-120),int(canvas.size["height"]/2-100),duration=2,button='left')

def remove_clipping_plane_3_plane():
    selectFromToolbar("Clip-id-visualization-toolbar")
    time.sleep(2)
    for i in range(1,3):
        ActionChains(driver).send_keys('c').perform()
    click_center()
    clip_fab("delete")

def reset_clipping_adjustment_3plane():
    selectFromToolbar("Clip-id-visualization-toolbar")
    clipping_plane_adjustment_plane1()
    clipping_plane_adjustment_plane2()
    clipping_plane_adjustment_plane3()
    clip_fab("reset")
    time.sleep(1)
    # snapCompare("reset_clipping_adjustment_3_plane-i")
    clip_fab("delete")
    time.sleep(1)
    clip_fab("reset")
    time.sleep(1)
    # snapCompare("reset_clipping_adjustment_3_plane-ii")

def clipping_6_plane_single_object_selected():
    ActionChains(driver).move_to_element(canvas).perform()
    ActionChains(driver).move_by_offset(60,50).click().perform()
    selectFromToolbar("Fit-id-visualization-toolbar")
    time.sleep(5)
    selectFromToolbar("Clip-id-visualization-toolbar")

def clipping_plane_adjustment_6_plane():
    click_center()
    selectFromToolbar("Clip-id-visualization-toolbar")
    clipping_plane_adjustment_plane1()

def invert_clipping_6_plane():
    ActionChains(driver).move_to_element(canvas).perform()
    ActionChains(driver).move_by_offset(60,50).click().perform()
    selectFromToolbar("Fit-id-visualization-toolbar")
    time.sleep(3)
    selectFromToolbar("Clip-id-visualization-toolbar")
    time.sleep(1)
    clip_fab("invert")

def remove_clipping_plane_6_plane():
    click_center()
    selectFromToolbar("Clip-id-visualization-toolbar")
    click_center()
    object_click()
    clip_fab("delete")
    time.sleep(0.5)

def restore_clipping_plane_6_plane():
    remove_clipping_plane_6_plane()
    click_center()
    clip_fab("delete")
    time.sleep(0.5)
    clip_fab("reset")

def reset_clipping_adjustment_6_plane():
    click_center()
    selectFromToolbar("Clip-id-visualization-toolbar")
    time.sleep(1)
    click_center()
    time.sleep(1)
    pyautogui.moveTo(int(canvas.size["width"]/1.5),int(canvas.size["height"]/1.5+200))
    time.sleep(0.5)
    pyautogui.dragTo(-int(canvas.size["width"]*3/4),-int(canvas.size["height"]/3),duration=2,button='left')
    time.sleep(2)
    clip_fab("reset")
    time.sleep(1)
    clip_fab("delete")
    time.sleep(1)
    clip_fab("reset")

def fit_with_clipping():
    # Enable Clip
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@id="Clip-id-visualization-toolbar"]'))).click()
    time.sleep(2)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@id="Fit-id-visualization-toolbar"]'))).click()
    time.sleep(5)
    snapCompare("fitWithThreePlaneClip")
    # Disable Clip
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@id="Clip-id-visualization-toolbar"]'))).click()
    time.sleep(1)
    # Bring back to Home Position
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@id="Home-id-visualization-toolbar"]'))).click()
    time.sleep(5)
    click_center()
    # Enable 6 plane clip
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@id="Clip-id-visualization-toolbar"]'))).click()
    time.sleep(2)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@id="Fit-id-visualization-toolbar"]'))).click()
    time.sleep(5)
    snapCompare("fitWithSixPlaneClip")
    
def keyboard_navigation():
    selectFromToolbar("Home-id-visualization-toolbar")
    nav_keys1=['a','w','s','d','e','c']
    nav_keys2=['i','k','j','l']  
    for key in nav_keys1:
        try:
            for i in range(1,25):
                ActionChains(driver).send_keys(key).perform()
                time.sleep(0.1)
        except:
            snapshot("test_navkey_%s" %(key))
        finally:
            time.sleep(3)
            snapCompare('navkey_%s' %(key))
        selectFromToolbar("Home-id-visualization-toolbar")
        time.sleep(2)

    for key in nav_keys2:
        try:
            for i in range(1,10):
                ActionChains(driver).send_keys(key).perform()
        except:
            snapshot("test_navkey_%s" %(key))
        finally:
            time.sleep(3)
            snapCompare('navkey_%s' %(key))   
        selectFromToolbar("Home-id-visualization-toolbar")
        time.sleep(2)
    arrowkeys = {"up": Keys.UP, "down":Keys.DOWN, "left":Keys.LEFT , "right":Keys.RIGHT}
    nav_keys3=["up","down","left","right"]
    for key in nav_keys3:
        try:
            for i in range(1,15):
                ActionChains(driver).send_keys(arrowkeys[key]).perform()
                time.sleep(0.1)
        except:
            snapshot("test_navkey_%s" %(key))
        finally:
            snapCompare('navkey_%s' %(key))   
        selectFromToolbar("Home-id-visualization-toolbar")
        time.sleep(2)
    try:
        for i in range(1,10):
            ActionChains(driver).send_keys('w').perform()
        ActionChains(driver).send_keys('h').perform()
        time.sleep(5)
    except:
        snapshot("test_navkey_home")
    finally:
        snapCompare("Home") 
    
def keybaord_combination():
    selectFromToolbar("Home-id-visualization-toolbar")
    nav_keys1=['a','c','d','e']
    nav_keys2=['i','j','k','l']
    #nav_keys3=[Keys.LEFT,Keys.DOWN,Keys.RIGHT,Keys.UP]

    for key in nav_keys1:
        for i in range(1,15):
            ActionChains(driver).send_keys(key).perform()
            time.sleep(1)
    snapCompare("kcombHome1","Home",0.03) 
    for key in nav_keys2:
        for i in range(1,15):
            ActionChains(driver).send_keys(key).perform()
            time.sleep(1)
    snapCompare("kcombHome2","Home",0.03) 
     
# This methods checks for the functioning of undo and redo for home position functionality
def undoRedoHome():
    selectFromToolbar("Home-id-visualization-toolbar")
    for i in range(0,20):  # To change camera from home position (position-1)
       ActionChains(driver).send_keys('a').perform()
       time.sleep(0.5)  
    selectFromToolbar("Home-id-visualization-toolbar") # Brings the model back to home
    time.sleep(2)
    selectFromMenu("Undo-id-main-menu") # doing undo goes back to position-1
    time.sleep(3)
    snapCompare("undoHome")  # check whether position-1 is reached
    selectFromMenu("Redo-id-main-menu") # doing redo brings the model to home
    time.sleep(3)
    #snapCompare("redoHome",None,0.03) # check whether home position is reached
    snapCompare("redoHome") # check whether home position is reached


# This methods checks for the functioning of undo and redo for set home functionality
def undoRedoSetHome():
    selectFromToolbar("Home-id-visualization-toolbar")
    for i in range(0,10):  # To change camera from home position (position-2)
       ActionChains(driver).send_keys('j').perform()  
    selectFromMenu("Set Home-id-main-menu") # setting position-2 as home
    ActionChains(driver).send_keys('w').perform() # changing the position to position-3(home)
    time.sleep(3)
    selectFromMenu("Undo-id-main-menu") # Doing undo to get back to position-2
    time.sleep(3)
    #snapCompare("undoSetHome",None,0.03) # check whether position-2 is reached
    snapCompare("undoSetHome")
    selectFromMenu("Redo-id-main-menu") # To change camera from position-2 (position-3)
    time.sleep(3)
    # snapCompare("redoSetHome",None,0.03) # check whether position-3 (home) is reached
    snapCompare("redoSetHome")


# This methods checks for the functioning of undo and redo for reset home functionality
def undoRedoResetHome():
    selectFromToolbar("Home-id-visualization-toolbar")
    for i in range(0,10): # To change th eposition from home position
       ActionChains(driver).send_keys('k').perform()  
    selectFromMenu("Set Home-id-main-menu") # set the new posiition as home
    selectFromMenu("Reset Home-id-main-menu") #click on reset home
    time.sleep(3)
    selectFromMenu("Undo-id-main-menu") 
    time.sleep(3)
    snapCompare("undoResetHome")
    selectFromMenu("Redo-id-main-menu")
    time.sleep(3)
    snapCompare("redoResetHome","openModel",0.03)

# This methods checks for the functioning of undo and redo for fit functionality
def undoRedoFit():
    click_center() # select the center object
    selectFromToolbar("Fit-id-visualization-toolbar") # select fit
    time.sleep(5)
    selectFromMenu("Undo-id-main-menu")
    time.sleep(5)
    snapCompare("undoFit")
    selectFromMenu("Redo-id-main-menu")
    time.sleep(5)
    snapCompare("redoFit",None,0.03)

def moveMouse(x,y,duration):
    MouseEvent.move(x,y,True,2)

def middleClcik():
    start_Time = time.time()
    while (time.time() < start_Time+5):
        print("hello")
        pyautogui.click(button='middle',clicks=100,interval=0.01)
        
def undoRedoPan():
    afterinnerHeight = driver.execute_script('return window.innerHeight')
    dbar = beforeInnerHeight-afterinnerHeight
    start_height = beforeOuterHeight-afterinnerHeight-dbar
    # pyautogui.moveTo(0,start_height)
    # width = GetSystemMetrics(0)
    # height = GetSystemMetrics(1)
    
    canvasHeight = canvasHeight
    canvasWidth = canvasWidth
    start_x = 10
    start_y = start_height + int(canvasHeight/2)
    end_x = start_x + canvasWidth -10  
    #mouse.move(start_x,start_y,True,1)
    # mouse.drag(start_x,start_y,end_x,start_y,True,3)
    # pyautogui.click(button='middle')
    # mouse.drag(start_x,start_y,end_x,start_y,True,3)
    moveMouse(start_x,start_y,0)
    #middleClcik()
    p1 = Process(target=middleClcik())
    p2 = Process(target=moveMouse(end_x,start_y,4))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

# This methods checks for the functioning of undo and redo for isolate functionality
def undoRedoIsolate():
    for i in range(1,5):
        ActionChains(driver).send_keys('d').perform()
    click_center() # selects an object
    selectFromMenu("Isolate-id-main-menu")
    time.sleep(2)
    selectFromMenu("Undo-id-main-menu")
    time.sleep(2)
    snapCompare("undoIsolate")
    selectFromMenu("Redo-id-main-menu")
    time.sleep(2)
    snapCompare("redoIsolate",None,0.03)

# This methods checks for the functioning of undo and redo for compass functionality
def undoRedoCompass():
    compass=driver.find_element("xpath",("//div[contains(@class,'visualization-navigation-compass__content')]"))
    compass.click()
    time.sleep(3)
    selectFromMenu("Undo-id-main-menu")
    time.sleep(3)
    snapCompare("undoCompass")
    selectFromMenu("Redo-id-main-menu")
    time.sleep(3)
    snapCompare("redoCompass",None,0.03)


# This method performs model rotation using mouse and checks for undo redo functioning
def undoRedoRotate():
    afterinnerHeight = driver.execute_script('return window.innerHeight') # inner height of the chrome document pages
    downloadbarHeight = beforeInnerHeight-afterinnerHeight # height of download bar in chrome.
    start_height = beforeOuterHeight-afterinnerHeight-downloadbarHeight # mouse iniial point
    
    canvasHeight = canvas.size["height"] # canvas height
    canvasWidth = canvas.size["width"] # canvas width
    bitwidth = int(canvasWidth/4)   #bitWidth * 4 = canvasWidth
    start_x = bitwidth # start posiiton of mouse in x direction to perform rotate
    start_y = start_height + int(canvasHeight/2) # start posiiton of mouse in y direction to perform rotate
    end_x = bitwidth * 3 # end posiiton of mouse in x direction after performing rotate
    pyautogui.moveTo(start_x,start_y+100) # moves the mouse to start point
    pyautogui.dragTo(end_x,start_y+100,duration=3) # drag the mouse sing to destination point within 2 sec of time
    time.sleep(5)
    selectFromMenu("Undo-id-main-menu")
    time.sleep(2)
    snapCompare("undoRotate","Home")
    selectFromMenu("Redo-id-main-menu")
    time.sleep(2)
    # generateBenchmark("redoRotate")
    snapCompare("redoRotate",None,0.03)

# This method performs fly using mouse and checks for undo redo functioning
def undoRedoFly():
    selectFromToolbar("Fly-id-visualization-toolbar")
    time.sleep(1)
    startTime = time.time()
    ActionChains(driver).click_and_hold().perform()
    while (time.time()<startTime+3):
        continue
    ActionChains(driver).release().perform()
    ActionChains(driver).context_click().perform()
    time.sleep(1)
    selectFromMenu("Undo-id-main-menu")
    time.sleep(3)
    snapCompare("undoFly","openModel")
    selectFromMenu("Redo-id-main-menu")
    time.sleep(3)
    snapCompare("redoFly")

# This method perform a multi click to select two different objects using navigation
def selectMultipleObjects():
    click_center()
    #first click on center of canvas
    time.sleep(2)
    for i in range(1,5): # move the model a bit
        ActionChains(driver).send_keys('d').perform()
    ActionChains(driver).key_down(Keys.CONTROL).perform() # press control
    click_center() #click center again
    ActionChains(driver).key_up(Keys.CONTROL).perform() # release control
   
def navigator_2D():
    visual_settings(["Navigator"],"on")
    navigator_2d= driver.find_elements("xpath","//div[contains(@class, 'visualization-toggle-icon-button')]//*[name()='svg']")[1]
    navigator_2d.click()
    time.sleep(navigatorFlyTime)
    try:
        WebDriverWait(driver,maxWaitTime).until(EC.visibility_of_element_located((By.XPATH,"//div[contains(@class, 'visualizationToggleIconActive')]")))
        print('icon turned blue')
    except Exception as e:
        print(e)
        raise  
    snapCompare("Navigator_2D_click")
    navigator_2d.click()
    time.sleep(navigatorFlyTime)
    snapCompare('Navigator_Revert')
    
def Navigator_Step():
    plusicon=driver.find_element("id","Zoom-In-id-navigation")
    minusicon=driver.find_element("id","Zoom-Out-id-navigation")
    for i in range(1,10):
        plusicon.click()
        time.sleep(1)
    snapCompare('Navigator_plus')
    for i in range(1,10):
        minusicon.click()
        time.sleep(1)
    snapCompare('Navigator_minus')
    
def Navigator_Fit():
    WebDriverWait(driver,40).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="mycanvas-0"]')))
    canvas.click()
    fitbutton=driver.find_elements("xpath","//div[contains(@class,'uxt-visualization-controls-basics__navigatorContainer')]//div[contains(@class, 'visualization-icon-button')]")[0]
    fitbutton.click()
    time.sleep(navigatorFlyTime)
    snapCompare('navigatorfit_single')
    hometaskbar=driver.find_element("id","Home-id-visualization-toolbar")
    hometaskbar.click()
    time.sleep(navigatorFlyTime)
    click_center()
    selectMultipleObjects()
    fitbutton=driver.find_elements("xpath","//div[contains(@class,'uxt-visualization-controls-basics__navigatorContainer')]//div[contains(@class, 'visualization-icon-button')]")[0]
    fitbutton.click()
    time.sleep(navigatorFlyTime)
    snapCompare('navigatorfit_multiple')

def navigator_compass():
    WebDriverWait(driver,40).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="mycanvas-0"]')))
    compass=driver.find_element("xpath",("//div[contains(@class,'visualization-navigation-compass__content')]"))
    compass.click()
    time.sleep(3)
    snapCompare('Compass_north')
    # ActionChains(driver).move_to_element(canvas).perform()
    # time.sleep(2)
    # canvas=driver.find_element("xpath",('//*[@id="mycanvas-0"]')
    # ActionChains(driver).drag_and_drop(compass,canvas).perform()
    # time.sleep(5)
    # snapCompare('Compass_rotate')
    ActionChains(driver).move_to_element(compass).perform()
    ActionChains(driver).context_click(compass).perform()
    time.sleep(3)
    #ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    pyautogui.press('esc')
    time.sleep(2)
    click_center()
    snapCompare('Compass_home')

# This method checks for fly functionlity using mouse to perform look operation
def flyNavigation():
    try:
        selectFromToolbar("Home-id-visualization-toolbar")
        afterinnerHeight = driver.execute_script('return window.innerHeight') 
        downloadbarHeight = beforeInnerHeight-afterinnerHeight
        start_height = beforeOuterHeight-afterinnerHeight-downloadbarHeight
        canvasHeight = canvasHeight # retrieving the size of canvas
        canvasWidth = canvasWidth
        bitwidth = int(canvasWidth/4)   # bitWidth * 4 = canvasWidth
        bitHeight = int(canvasHeight/4)
        start_y = start_height + int(canvasHeight/2)  # Distance of canvas center from top of the screen
        pyautogui.moveTo(bitwidth*2,start_y) # moves to the centre of canvas
        ordinates=[[bitwidth,0],[-bitwidth,0],[0,bitHeight],[0,-bitHeight]] # coordinates for moving the mouse
        ActionChains(driver).send_keys("f").perform() # turn on fly mode
        num=1
        for ordinate in ordinates:
            position = "flyPosition"+str(num)
            time.sleep(1)
            pyautogui.moveRel(ordinate[0],ordinate[1])
            snapCompare(position) # check every position based on the mouse movement
            ActionChains(driver).send_keys("h").perform() # brings backs to home position after testing a single position such that next movement of the mouse can be done freshely
            time.sleep(5)
            num+=1
    finally:
        ActionChains(driver).context_click().perform() # right click mouse to disable fly mode

# ORTHOGRAPHIC METHODS #####
def ortho_mouse_limitation():
    afterinnerHeight = driver.execute_script('return window.innerHeight')
    downloadbarHeight = beforeInnerHeight-afterinnerHeight
    start_height = beforeOuterHeight-afterinnerHeight-downloadbarHeight
    canvasHeight = canvasHeight # retrieving the size of canvas
    canvasWidth = canvasWidth
    bitwidth = int(canvasWidth/4)   #bitWidth * 4 = canvasWidth
    bitHeight = int(canvasHeight/4)
    start_x = int(canvasWidth/2) # Distance of canvas center from the left side of the screen
    start_y = start_height + int(canvasHeight/2) # Distance of canvas from top of the screen
    ordinates=[[start_x+bitwidth,start_y],[start_x-bitwidth,start_y],[start_x,start_y+bitHeight],[start_x,start_y-bitHeight]] # coordinates to set the position of the mouse.
    num=1
    for ordinate in ordinates:
        pyautogui.moveTo(start_x,start_y)
        time.sleep(1) # moves the mouse to center of the canvas
        position = "dragPosition"+str(num)
        pyautogui.dragTo(ordinate[0],ordinate[1],duration=1) #drag the mouse to position within a second
        time.sleep(1)
        #generateBenchmark(position)
        snapCompare(position)
        ActionChains(driver).send_keys("h").perform()
        time.sleep(3)
        num+=1
   
def ortho_keyborad_limitation():
    keys = ["i","k","j","l"] # keys which donot work for orthographic mode.
    for key in keys:
        for i in range(0,10):
            ActionChains(driver).send_keys(key).perform()
        snapCompare("look_key_%s" %key,"openModel",0.03) # check the position for each and every key:

# Opens settings, copies information and checks for presence of some keywords
def copyInformationData():
    select_setting_type('information')
    count = 0 
    copyButton = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//*[contains(@id,'Information-notes-id-settings-menu')]//*[name()='svg']")))
    copyButton.click()
    sInformationData = clipboard.paste()
    keywords = ["Product Information","Document Information","GVC version","mMap SDK version"]
    if all(value in sInformationData for value in keywords):
        count = 1          
    else:
        count = 0 
    assert (count != 0), "Missing Some of the Keys in Information Dialouge"  

def copyDiagnosticsData():
    select_setting_type('System Scan')
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Diagnostics')]"))).click()
    count = 0 
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "vds-memory-statistics-copy-to-clipboard-btn"))).click()
    # copyButton = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.ID,"vds-memory-statistics-copy-to-clipboard-btn")))
    # copyButton.click()
    sInformationData = clipboard.paste()
    keywords = ["Visualization Data Store Statistics","Server Name","Percentage", "Stats"]
    if all(value in sInformationData for value in keywords):
        count = 1          
    else:
        count = 0 
    assert (count != 0), "Missing Some of the Keys in Information Dialouge" 
    time.sleep(1)
    buttons["settings_back"]().click()
    time.sleep(.5)    
    buttons["settings_close_x"]().click() 
    time.sleep(1)

# Opens properties and checks to see if the properties card is displayed and undisplayed
def properties():
    click_center() #it will make object(slab) selection
    try:
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'visualization-details-card__card')]"))) #Checks to make sure properties display
    except TimeoutException:
        assert False, "Property card didn't show up after selection"
    click_center() #it will make object(slab) deselection
    try:
        WebDriverWait(driver,20).until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'visualization-details-card__card')]"))) #Checks to make sure properties card disappear after object is deselected
        time.sleep(5)
    except TimeoutException:
        assert False, "Property card didn't close after deselection"
    

def pressKey(key, loop):
    for i in range(0,loop):
        ActionChains(driver).send_keys(key).perform()
        time.sleep(0.1)
    
def fit_walkview():
    drag_walkview()
    ActionChains(driver).move_by_offset(0,120).click().perform()
    selectFromToolbar("Fit-id-visualization-toolbar")
    time.sleep(3)
    snapCompare("fitwithWalkView")
    pressKey("e",10)
    snapCompare("checkelevationLockwith-key-e","fitwithWalkView")
    pressKey("c",10)
    snapCompare("checkelevationLockwith-key-c","fitwithWalkView")	

def select_setting_type(type):
    buttons['menu_open_hamburger']().click()
    time.sleep(3)
    driver.find_element("id","Settings-id-main-menu").click()
    time.sleep(1.5)
    if(type=='visual'):
        driver.find_element("id","visualization-settings-Visual-list-item").click()
    elif(type=='information'):
        driver.find_element("id","visualization-settings-Information-list-item").click()
    elif(type=='cameralocks'):
        driver.find_element("id","visualization-settings-Camera Locks-list-item").click()
    elif(type=='System Scan'):
        driver.find_element("id","visualization-settings-SystemScan-list-item").click()
    elif(type=='diagnostics'):
        driver.find_element("id","visualization-settings-Diagnostics-list-item").click()
    elif(type=='aspects'):
        driver.find_element("id","visualization-settings-Aspects-list-item").click()
    time.sleep(2)

def camera_locks(settings,status):
    select_setting_type('cameralocks')
    time.sleep(1)
    for setting in settings:
        if(status == 'on'):
            try:
                driver.find_element("xpath",("//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]//div[not(contains(@class,'visualization-switch-on'))]" % setting)).click()
            except:
               raise 
        else:
            try:
                driver.find_element("xpath",("//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]//div[contains(@class,'visualization-switch-on')]" % setting)).click()
            except:
                raise
        time.sleep(1)
    buttons["settings_back"]().click()
    time.sleep(.5)    
    buttons["settings_close_x"]().click() 
    time.sleep(2)

def environment(featureType, setting=None, internalSetting=None):
    selectFromMenu('Environment-id-main-menu')
    if(featureType=='presets'):
        environment_tab_buttons["presets"]().click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='%s']"% setting))).click()
    elif(featureType=='lighting'):
        environment_tab_buttons["lighting"]().click()
    elif(featureType=='background'):
        environment_tab_buttons["background"]().click()
        if(setting=='gradient'):
            background_buttons["gradient"]().click()
        elif(setting=='color'):
            background_buttons["color"]().click()
        elif(setting=='skybox'):
            if(internalSetting=='midday'):
                driver.find_element("xpath",("//img[@alt='Midday']").click())
            time.sleep(5)
            for i in range(0,30):
                ActionChains(driver).send_keys('i').perform()
                time.sleep(0.1)
            for i in range(0,40):
                ActionChains(driver).send_keys('c').perform()
                time.sleep(0.1)
    else:
        environment_tab_buttons["surface"]().click()

def visual_settings(settings,status):
    select_setting_type('visual')
    for setting in settings:
        if(status == 'on'):
            try:
                driver.find_element("xpath",("//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]//div[contains(@class,'visualization-switch-on')]" % setting))
            except:
                driver.find_element("xpath",("//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]" % setting)).click()
        else:
            try:
                driver.find_element("xpath",("//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]//div[contains(@class,'visualization-switch-on')]" % setting))
                driver.find_element("xpath",("//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]" % setting)).click()
            except:
                pass
        time.sleep(1)
    buttons["settings_back"]().click()
    time.sleep(.5) 
    buttons["settings_close_x"]().click() 
    time.sleep(5)

def set_projection_mode(setting):
    select_setting_type('visual')
    driver.find_element("xpath",'//div[@id="visualization-settings-Projection-dropdownlist"]').click()
    time.sleep(0.5)
    time.sleep(3)
    driver.find_element("xpath",('//*[@id="%s-id-settings-menu"]' %setting)).click()
    time.sleep(1)
    buttons["settings_back"]().click()
    time.sleep(.5)
    buttons["settings_close_x"]().click()
    time.sleep(2)

def get_environment_settings(setting):
    disabled = True
    switchON = True
    if(setting=='gradient'):
        selectFromMenu('Environment-id-main-menu')
        environment_tab_buttons["background"]().click()
        try:
            driver.find_elements("xpath","//div[contains(@class, 'background-content-item')]//*[name()='svg']")[2].click()
        except:
            switchON = False
        time.sleep(2)
        try:
            driver.find_elements("xpath","//div[contains(@class, 'background-content-item')]//*[name()='svg']")[0].click()
            disabled = False
            time.sleep(1)
        except:
            pass
        environment_tab_buttons["environment_close"]().click()
    return disabled,switchON

def get_visual_settings(setting):
    select_setting_type('visual')
    disabled = True
    switchON = True
    try:
        driver.find_element("xpath",("//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]//div[contains(@class,'visualization-switch-on')]" % setting))
    except:
        switchON = False  
    try:
        driver.find_element("xpath",("//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]//div[contains(@class,'UxtSwitch-disabled')]" % setting))
    except:
        disabled = False  
    buttons["settings_back"]().click()
    time.sleep(.5)     
    buttons["settings_close_x"]().click()
    time.sleep(2)
    return disabled,switchON

# This method used to get the switch_on , disabled status of the UI options present in visual settings
def get_visual_settings_element_status(setting):
    try:
        disabled = True
        switch_on = True
        buttons['menu_open_hamburger']().click()
        time.sleep(.5)
        driver.find_element("xpath",('//*[@id="Settings-id-main-menu"]')).click()
        time.sleep(.5)
        driver.find_element("xpath",('//*[@id="visualization-settings-Visual-list-item"]')).click() 
        try :
            driver.find_elements("xpath","//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]//div[contains(@class,'UxtSwitch-disabled')]" % setting)[0]
        except IndexError: #Index error pops up if no web elements are retuned from the above find_elements_by_xpath .
            disabled = False
        try :
            driver.find_elements("xpath","//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]//div[contains(@class,'UxtSwitch-on')]" % setting)[0]
        except IndexError:
            switch_on = False
        buttons["settings_back"]().click()
        time.sleep(.5)
        buttons["settings_close_x"]().click()
        time.sleep(.5)
        return disabled,switch_on
    except:
        raise

def get_Camera_Locks_status(lock):
    try:
        disabled = True
        switch_on = True
        buttons['menu_open_hamburger']().click()
        time.sleep(.5)
        driver.find_element("xpath",('//*[@id="Settings-id-main-menu"]')).click()
        time.sleep(.5)
        driver.find_element("xpath",('//*[@id="visualization-settings-Camera Locks-list-item"]')).click() 
        try :
            driver.find_elements("xpath","//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]//div[not(contains(@class,'UxtSwitch-on'))]" % lock)[0]
        except IndexError: #Index error pops up if no web elements are retuned from the above find_elements_by_xpath .
            disabled = False
        try :
            driver.find_elements("xpath","//div[contains(text(),'%s')]/parent::div//*[contains(@class,'uxt-visualization-settings-item__boolean__control')]//div[contains(@class,'UxtSwitch-on')]" % lock)[0]
        except IndexError:
            switch_on = False
        buttons["settings_back"]().click()
        time.sleep(.5)
        buttons["settings_close_x"]().click()
        time.sleep(.5)
        return disabled,switch_on
    except:
        raise

def get_main_menu_command_status(element):
    try:
        disabled = True
        enabled = True
        buttons['menu_open_hamburger']().click()
        time.sleep(.5)
        
        try :
            driver.find_element("xpath","//div[contains(normalize-space(@class), 'UxtListItem-disabled')]//div[contains(text(),'%s')]" % element)
        except : 
            disabled = False
        try :
            driver.find_element("xpath","//div[contains(normalize-space(@class), 'UxtListItem-root-UxtListItem-singleLine')]//div[contains(text(),'%s')]" % element)
        except :
            enabled = False
        time.sleep(.5)
        buttons['menu_close_hamburger']().click()
        time.sleep(1)
        return disabled,enabled
    except:
        raise

def get_WalkmanView_status(status): #pass 'status' value as 'applicable' for models where walkman can be used and 'inapplicable' for models where walkman can't be used
    if status=="applicable":
        try:
            disabled = True
            enabled= True
            try :
                driver.find_element("xpath","//div[contains(@class,'visualization-navigation-walking-view-content')]//*[contains(@class, 'visualization-toggle-icon-button-root') and not(contains(@class, 'visualizationToggleIconActive'))]")
            except :
                disabled = False
            try :
                driver.find_element("xpath","//div[contains(@class,'visualization-navigation-walking-view-content')]//div[contains(@class, 'visualizationToggleIconActive')]")
            except :
                enabled = False
            return disabled,enabled
        except:
            raise
    elif status=="inapplicable":
        try:
            disabled = True
            enabled= True
            try :
                driver.find_element("xpath","//div[contains(@class,'visualization-navigation-walking-view-content')]//div[contains(@class, 'UxtToggleIconButton-disabled')]")
            except :
                disabled = False
            try :
                driver.find_element("xpath","//div[contains(@class,'visualization-navigation-walking-view-content')]//div[contains(@class, 'visualizationToggleIconActive')]")
            except :
                enabled = False
            return disabled,enabled
        except:
            raise
    
def get_projection_mode_status(mode):
    try:
        disabled = True
        enabled = True
        select_setting_type('visual')
        driver.find_element("xpath",'//div[@id="visualization-settings-Projection-dropdownlist"]').click()
        time.sleep(0.5)
        try :
            driver.find_element("xpath","//div[contains(@class, 'UxtDropdownList-choices')]//div[contains(@class, 'UxtListItem-disabled') and contains(@id, '%s')]" % mode)
        except: 
            disabled = False
        try :
            driver.find_element("xpath","//div[contains(@class, 'UxtDropdownList-choices')]//div[not(contains(@class, 'UxtListItem-disabled')) and contains(@id, '%s')]" % mode)
        except:
            enabled = False
            time.sleep(2)
        driver.find_element("xpath",('//*[@id="Orthographic-id-settings-menu"]')).click() #To close the dropdown by choosing selecting Orhographic mode
        time.sleep(0.5)
        buttons["settings_back"]().click()
        time.sleep(.5)
        buttons["settings_close_x"]().click() 
        time.sleep(.5)
        return disabled,enabled
    except:
        raise

def checkSettingsMenu():
    try:
        buttons["settings_close_x"]()
        return True
    except:
        return False

def set_default_settings():
    visual_settings(["Ambient Occlusion","Anti-Aliasing","Transparency","Navigator","Optimize Performance"],"on")
    visual_settings(["Outline","Display Axis","Fly-To"],"off")
    environment('background','color')

def isolateandMeasure():
    isolate()
    selectFromToolbar("Measure-id-visualization-toolbar")
    time.sleep(2)
    createMeasure()
    snapCompare("measurementsinIsolateSingleObject_1")#checking measurement of single object in isolated view
    isolate()
    time.sleep(5)
    pressKey("j",2)
    pressKey("c",7)
    measure_fab("open_fab")
    time.sleep(2)
    measure_fab("placementmode")
    time.sleep(2)
    for i in range(0,2):
        click_center()
        measure_fab("delete")
    time.sleep(2)
    snapCompare("measurementsinIsolateSingleObject_2")

def EnableNavigator2D():
    try:
        visual_settings(["Navigator"],"on")
        enable=driver.find_elements("xpath","//div[contains(@class,'uxt-visualization-controls-basics__navigatorContainer')]")
        if enable:
            return True
        else :
            return False
    except:
        raise

def clip_box_fit():
    click_center()
    pressKey("l",2)
    ActionChains(driver).key_down(Keys.CONTROL).perform()
    click_center()
    ActionChains(driver).key_up(Keys.CONTROL).perform()
    selectFromToolbar("Clip-id-visualization-toolbar")
    time.sleep(2)
    selectFromToolbar("Fit-id-visualization-toolbar")
    time.sleep(4)

def moveclipPlane(x_factor,y_factor,timeofmotion):
    initial_x = int(canvas.size["width"]/2)
    initial_y = int(canvas.size["height"]/2)
    pyautogui.moveTo(initial_x,initial_y+250)
    time.sleep(0.5)
    pyautogui.dragTo(initial_x+initial_x*x_factor,initial_y+initial_y*y_factor+150,duration=timeofmotion,button='left')

def featureMenu_buttons(option):
    buttons['feature_menu']().click()
    WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,"//div[contains(@class,'sidenav')]//*[contains(text(), '%s') or self::button[contains(text(), '%s')]]" % (option, option)))).click()
    time.sleep(2)
    buttons['feature_menu']().click() #close features menu
    time.sleep(2)

def selectMultipleObjects_using_offset(ax,ay,bx,by): #pass x,y coordinates of two objects
    click_Offset(ax,ay)
    time.sleep(2)
    ActionChains(driver).key_down(Keys.CONTROL).perform() # press control
    click_Offset(bx,by) #click center again
    ActionChains(driver).key_up(Keys.CONTROL).perform() # release control

def selection_with_custom_color(hex_code):
    selectFromMenu('Selection Color-id-main-menu')
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="%s"]' % hex_code))).click()
    ActionChains(driver).move_to_element(canvas).perform()
    ActionChains(driver).move_by_offset(60,50).click().perform()
    time.sleep(5)

def zoom_area():
    selectFromToolbar("Zoom Area-id-visualization-toolbar")
    time.sleep(1)
    pyautogui.moveTo(int(canvas.size["width"]/1.5),int(canvas.size["height"]/1.5))
    pyautogui.dragTo(int(canvas.size["width"]),int(canvas.size["height"]),duration=1,button='left')
    time.sleep(2)
    

def dismiss_activate_zoomarea():
    zoom_area()
    time.sleep(2)
    snapCompare("zoomArea_UIworkflow","zoom_area")
    time.sleep(2)
    ActionChains(driver).context_click(canvas).perform()#To Right-click
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()#To clear the list displayed on webpage when right click is given
    time.sleep(3)
    ActionChains(driver).send_keys("z").perform()#reactivate Zoom area
    time.sleep(2)
    ActionChains(driver).send_keys("z").perform()#dismiss Zoomarea

def pan_using_mouse_wheel():
    action = ActionChains(driver)
    action.move_to_element(canvas)
    # 1. Perform the move to the canvas element
    action.perform()
    # 2. Simulate a middle mouse button press using JavaScript
    driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mousedown', {button: 1}));", canvas)
    time.sleep(5)
    # 3. Create a new ActionChains instance for mouse movement
    action = ActionChains(driver)
    # 4. Move the mouse cursor to a specific offset position
    action.move_by_offset(36, -104)
    # 5. Perform the mouse movement actions
    action.perform()
    time.sleep(2)
    # 6. Release the middle mouse button using JavaScript
    driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseup', {button: 1}));", canvas)

def scroll_wheel_zoom():
    pyautogui.moveTo(canvas.size["width"]/2,canvas.size["height"]/2, duration=0.5)
    for _ in range(0,25):
        pyautogui.scroll(50)
        time.sleep(1)
    
    
def resize_window(driver):
    time.sleep(1)
    # Minimize the browser window
    driver.set_window_size(800, 600)
    time.sleep(6)  # Add a delay if needed
    # Maximize the browser window again
    driver.maximize_window()

def left_Click_and_move(x,y):
    pyautogui.moveTo(int(canvas.size["width"]/2),int(canvas.size["height"]/2))
    time.sleep(2)
    pyautogui.dragTo(x,y,duration=3,button='left')

def mouse_navigation():
    destination_coordinates=[(canvas.size["width"]/4,canvas.size["height"]/2),(canvas.size["width"]/1.5,canvas.size["height"]/2),(canvas.size["width"]/2,canvas.size["height"]/4),(canvas.size["width"]/2,canvas.size["height"]/1.5)]
    n=1
    for x,y in destination_coordinates:
        print(x,y)
        left_Click_and_move(x,y)
        time.sleep(2)
        generateBenchmark("mouse_navigation_2D_"+str(n))
        selectFromToolbar("Home-id-visualization-toolbar")
        n+=1

def style(choice):                             
    element=driver.find_element("xpath","//div[contains(@class, 'UxtRadioGroup')]//div[contains(@class, 'UxtRadioButton-root')]//div[contains(text(),'%s')]" % choice)
    element.click()

def model_selected_to_style(model):
    driver.find_element("xpath","//input[contains(@value, '%s')]"% model)

def select_palette_filler_icon():
    button=driver.find_element("xpath","//div[@style='display: inline-block;']//button[contains(@class, 'UxtButton') and contains(@style, 'background-color:')]")
    button.click()

def palette_select_materials_using_icon(x,y): #provide offset values of the object to select
    select_palette_filler_icon()
    time.sleep(2)
    #check if the button color changed to light blue after selected
    driver.find_element("xpath","//div[@style='display: inline-block;']//button[contains(@class, 'UxtButton') and @style='background-color: lightblue;']")
    click_Offset(x,y)
    time.sleep(2)
    
def palette_select_materials_using_dropdown(number):
    button=driver.find_element("xpath","//div[contains(text(),' Palette Styles: ')]/following::div[contains(@class, 'UxtDropdownList-input')]")
    button.click()
    time.sleep(5)
    element_found = False
    arrow=Keys.ARROW_DOWN
    max_time=60
    start_time=time.time()

    while not element_found:
        actions = ActionChains(driver)
        actions.send_keys(arrow)
        actions.perform()
        try:
            element = driver.find_element("xpath",f"//div[contains(text(),'{number} - Material_{number}')]")
        except:
            element = None
        time.sleep(.5)

        # Check if the element is found after scrolling
        if element:
            try:
                time.sleep(2)
                element.click()
                time.sleep(1)
                click_Offset(0,300)
                element_found = True
                break
            except:
                pass
        # elapsed_time = time.time() - start_time
        # if elapsed_time >= max_time:
        #     arrow=Keys.ARROW_UP
    time.sleep(2)

def styles_defined(x,name=None): #provide x value as button name if its button or the value name if its an input. and name value only if you are creating a new bucket
    new_bucket_btn = driver.find_element("xpath","//div[contains(text(),' Defined Styles: ')]/following::div[contains(text(), '%s')]" % x)
    time.sleep(1)
    new_bucket_btn.click()
    if x==" New Bucket":
        pyautogui.write(name)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)

def create_bucket_add_objects(name,type): #provide name of the new bucket and type of the model 3D or 2D
    time.sleep(.5)
    styles_defined(" New Bucket",name)
    time.sleep(3)
    select_bucket(name)
    time.sleep(2)
    #selecting objects into the bucket
    if type=="3D":
        selectMultipleObjects_using_offset(-103,-4,-49,-26)
    if type=="2D":
        selectMultipleObjects_using_offset(36,-104,40,-25)
    #adding the selected objects into the bucket
    styles_defined("Add Selected Objects")

def select_bucket(name):
    time.sleep(.5)
    dropdown=driver.find_element("xpath","//div[contains(text(),' Defined Styles: ')]/following::div[contains(@class, 'UxtDropdownList-icon')]")
    time.sleep(.5)
    dropdown.click()
    time.sleep(.5)
    bucket=driver.find_element("xpath","//div[contains(text(),' Defined Styles: ')]/following::div[contains(@title, '%s')]" % name)
    # bucket=driver.find_element("xpath","//div[@title='%s']"% name)
    # bucket = driver.find_element("xpath", "//div[contains(@title, '%s')]" % name)
    time.sleep(.5)
    bucket.click()

def styles_slider_selection(name,percent):
    slider=driver.find_element("xpath","//div[contains(text(),'%s')]/following::div[contains(@class, 'react-draggable')]"% name)
    x_offset = percent
    y_offset = 0

    # Use JavaScript instead of available built in methods in python to simulate a drag-and-drop action, as styles are not within GVC window after resizing
    driver.execute_script("""
    var source = arguments[0];
    var offsetX = arguments[1];
    var offsetY = arguments[2];

    // Calculate the new position based on the offsets
    var newLeft = source.getBoundingClientRect().left + offsetX;
    var newTop = source.getBoundingClientRect().top + offsetY;

    // Create a new MouseEvent for mousedown
    var event = new MouseEvent('mousedown', {
        bubbles: true,
        cancelable: true,
        view: window,
        clientX: newLeft,
        clientY: newTop
    });

    // Dispatch the 'mousedown' event on the source element
    source.dispatchEvent(event);

    // Simulate mousemove
    event = new MouseEvent('mousemove', {
        bubbles: true,
        cancelable: true,
        view: window,
        clientX: newLeft,
        clientY: newTop
    });
    source.dispatchEvent(event);

    // Simulate mouseup
    event = new MouseEvent('mouseup', {
        bubbles: true,
        cancelable: true,
        view: window,
        clientX: newLeft,
        clientY: newTop
    });
    source.dispatchEvent(event);
                          """, slider, x_offset, y_offset)
    time.sleep(2)

def use_PBR():
    toggle_btn=driver.find_element("xpath","//div[contains(text(),'Use PBR: ')]/following::div[contains(@class, 'UxtSwitch-root')]")
    toggle_btn.click()

def reset_remove_styles(name):
    xpath_expression = f"//button[contains(., '{name}')]"
    try:
        button = driver.find_element(By.XPATH, xpath_expression)
        button.click()
    except Exception as e:
        print(f"Error: {e}")

def close_Styles():
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'sa-modal-close-button')]"))).click()

def color_picker(name,r=None,g=None,b=None):
    button=driver.find_element("xpath","//div[text()='%s']/following::div[contains(@class, 'UxtColorPickerDropdown-root')]"% name)
    button.click()
    colors={'R': r, 'G': g, 'B': b}
    filtered_colors = {key: value for key, value in colors.items() if value is not None}
    for key, value in filtered_colors.items():
        # slider_xpath= driver.find_element("xpath", "//div[contains(@class, 'UxtRGBSlider-root')]//div[contains(@class, 'UxtRGBSlider-label') and contains(text(), '%s')]/following::input[contains(@class, 'UxtSlider-input')]" % key)
        input_box= driver.find_element("xpath", "//div[contains(@class, 'UxtRGBSlider-root')]//div[contains(@class, 'UxtRGBSlider-label') and contains(text(), '%s')]/following::input[contains(@class, 'UxtSlider-input')]" % key)
        # input_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, slider_xpath)))
        time.sleep(2)
        # input_box.click()  # or input_box.send_keys(Keys.RETURN)
        # input_box.clear()
        # input_box.send_keys(str(value))
        # time.sleep(2)
        # try:
        #     input_box.send_keys(str(value))
        # except Exception as e:
        #     print(f"An unexpected error occurred: {e}")
        input_box.clear()

        # Wait for input box to be visible
        WebDriverWait(driver, 10).until(EC.visibility_of(input_box))
        input_box.send_keys(str(value))
    click_center() #to exit the colorPicker

def find_import_export_text_box():
    text_box= driver.find_element("xpath","//div[contains(text(), ' Import/Export JSON:  ')]/following::input[contains(@class, 'UxtInput-input')]")
    time.sleep(1)
    text_box.click()

def find_import_export_buttons(name):
    button=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'%s')]"% name)))
    button.click()

def export_style_palette(name):
    #click the export styles/palette button
    find_import_export_buttons(name)
    #identify the text box and copy the text
    find_import_export_text_box()
    ActionChains(driver).key_down(Keys.CONTROL).perform() # press control
    pressKey('a',1)#click center again
    time.sleep(.5)
    pressKey('c',1)
    ActionChains(driver).key_up(Keys.CONTROL).perform() # release control
    json_text = clipboard.paste()
    target_text="name" #'name' occurs only once in the copied json string if 'Export style' is clicked, and 'name' occurs more than once in the copied json string if 'Export palette' is clicked.
    count = json_text.count(target_text)
    a=0 
    if count > 1 and name=="Export Palette":
        a=1
    elif count == 1 and name=="Export Style":
        a=1
    else:
        a=0
    assert (a != 0), "JSON text contains none or unexpected number of 'name' strings"

def import_style_palette(name): #give name as import style/import palette
    find_import_export_text_box()
    time.sleep(.2)
    ActionChains(driver).key_down(Keys.CONTROL).perform() # press control
    ActionChains(driver).send_keys('v').perform()
    ActionChains(driver).key_up(Keys.CONTROL).perform() # release control
    time.sleep(.2)
    find_import_export_buttons(name)
   
def fence_select_fab(function):
    fence_buttons = {
        "close_fab":lambda : driver.find_elements("xpath","//div[contains(@class, 'visualization-fab-toolbar-fab')]")[0],
        "open_fab":lambda :  driver.find_elements("id",'Select-id-fab-toolbar')[0],
        "fenceselect":lambda : driver.find_element("id","Fence Select-id-Select-fab-toolbar"),
        "inside":lambda : driver.find_element("id","Inside Select-id-Select-fab-toolbar"),
        "overlap":lambda : driver.find_element("id","Overlap Select-id-Select-fab-toolbar"),
        "cancel":lambda : driver.find_element("id","Cancel-id-Select-fab-toolbar")
    }
    fence_buttons[function]().click()  

def Lighting_switch_ON(text):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//h4[contains(text(), '%s')]/following::div[contains(@class,'UxtSwitch-root')]" % text))).click()

def Lighting():
    Lighting_switch_ON("Direction Lights")
    Lighting_switch_ON("Shadows")
    time.sleep(1)
    Lighting_switch_ON("Light Rays")
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sun-icon"))).click()
    time.sleep(1)
    properties_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'lighting-form-row-two-toggle') and contains(@class, 'select') and .//h4[text()='Properties']]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", properties_element)
    driver.find_element("xpath",".//h4[text()='Properties']").click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "moon-icon"))).click()
    time.sleep(2)
    input_element= driver.find_element("xpath","//div[contains(@class, 'lighting-form-row')]//h4[text()='Rotation']/following-sibling::div//input[contains(@class, 'lightingPropertyInput')]") 
    input_element.clear()
    input_element.send_keys("100")
    time.sleep(2)
    
def Surface():
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Visible-switch-id-settings-menu"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Ground-id-icon-tabs"))).click()
    driver.find_element("xpath","//div[contains(text(), 'Grass')]").click()
    time.sleep(10)

def get_environment_preset():
    environment_tab_buttons["presets"]().click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='Sunrise']"))).click()
    preset_selected = True
    try:
        driver.find_element("xpath",("//div[contains(@class='UxtCallOut-root')]//div[contains(@class='UxtCallOut-anchorWrapper')]//div[contains(@class='image-card-selected-color')]"))
    except:
        preset_selected = False

    environment_tab_buttons["environment_close"]().click()
    time.sleep(1)
    return preset_selected

def get_environment_Lighting(text):
    disabled = True
    switchON = True
    try:
        driver.find_element("xpath","//h4[contains(text(), '%s')]/following::div[contains(@class,'UxtSwitch-on')]"% text)
    except:
        switchON = False  
    try:
        driver.find_element("xpath","//h4[contains(text(), '%s')]/following::div[contains(@class,'UxtSwitch-disabled')]" % text)
    except:
        disabled = False 
    time.sleep(2)
    return disabled,switchON

def get_environment_Surface():
    disabled = True
    switchON = True
    try:
        driver.find_element("xpath","//div[contains(@id,'Visible-switch-id-settings-menu') and contains(@class, 'UxtSwitch-on')]")
    except:
        switchON = False  
    try:
        driver.find_element("xpath","//div[contains(@id,'Visible-switch-id-settings-menu') and contains(@class, 'UxtSwitch-disabled')]")
    except:
        disabled = False 
    time.sleep(2)
    return disabled,switchON


def lookup_select(api,input_value,object_index=None):
    time.sleep(2)
    selectFromMenu('Object Lookup & Select-id-main-menu')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'UxtDropdownList-unEditableInput')]"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="%s"]' % api))).click()
    click_center()
    time.sleep(3)
    input_box = driver.find_element("xpath","//div[contains(@class, 'commandSideBar')]//div[contains(@class, 'UxtInput-innerContainer')]//input[contains(@class, 'UxtInput-input') and contains(@id, 'Input') and not(contains(@class, 'UxtDropdownList'))]")
    input_box.clear()
    input_box.send_keys(str(input_value))
    time.sleep(1)
    if(api=='NoLookup'):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'UxtButton-root') and .//div[contains(text(), 'Batch Select All')]]"))).click()
    else:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(text(), 'Call API')]]"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'UxtButton-root')]//div[contains(@class, 'UxtButton-children') and contains(text(), 'Batch Select All')]"))).click()
        elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@id, 'collapsible-trigger') and contains(text(), 'Object')]")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(elements[object_index])).click()
        time.sleep(1)
    driver.find_element("xpath",("//span[contains(@class, 'sa-modal-close-button')]")).click()
    time.sleep(1)

def append_basic():
    buttons['menu_open_hamburger']().click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@title="APPEND"]'))).click()
    driver.find_element(By.XPATH, "//div[contains(@class, 'UxtIcon-root-UxtIcon-clickable-UxtTreeItem-chevron-UxtTreeItem-collapsible')]//*[name()='svg']").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//div[contains(@class, 'UxtTreeItem-text') and contains(text(), 'structure')]").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'sa-modal-close-button') and text()='×']"))).click()
    click_center()
    pressKey('w',10)

# def sheet_from(option,sample,target = None):
#     buttons['feature_menu']().click()
#     time.sleep(2)
#     WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[contains(@class,'sidenav')]//*[contains(text(), '%s') or self::button[contains(text(), '%s')]]" % (option, option)))).click()
#     time.sleep(5)
#     wait = WebDriverWait(driver, 10)
#     wait.until(EC.alert_is_present(),'Alert did not pop out')
#     time.sleep(0.5)
#     obj = driver.switch_to.alert
#     obj.send_keys(sample)
#     obj.accept()
#     try:
#         wait.until(EC.alert_is_present(), 'Another alert did not pop out')
#         time.sleep(0.5)
#         obj = driver.switch_to.alert
#         alert_text = obj.text
#         if "input" in alert_text.lower():  # This is a simple heuristic to check for text input
#             time.sleep(5)
#             obj.send_keys(target)
#         obj.accept()
#     except:
#         pass 
#     buttons['feature_menu']().click()

def edit_measure():
    createMeasure1()
    measure_fab("placementmode")
    selectFromToolbar("Home-id-visualization-toolbar")
    click_center()
    time.sleep(2)
    actions = ActionChains(driver)
    # Click and hold at the current mouse position
    actions.click_and_hold().perform()
    time.sleep(5)
    # Move the mouse to the center of the canvas
    actions.move_by_offset(30,100).perform()
    # Release the mouse button
    actions.release().perform()
    time.sleep(5)

def alert_text_validation(text):
    new_alert = WebDriverWait(driver, 10).until(EC.alert_is_present())    
    # Switch to the new alert box    
    new_alert = driver.switch_to.alert    
    # Get the text from the new alert box  
    alert_text = new_alert.text    
    # Validate the text (this can be customized as needed)    
    expected_text = text
    assert alert_text == expected_text, f"Alert text does not match. Expected: '{expected_text}', but got: '{alert_text}'"
    # Accept the alert to close it
    new_alert.accept()
 
def feature_menu_options_with_alerts(option,sample,target = None):
    buttons['feature_menu']().click()
    time.sleep(2)
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//div[contains(@class,'sidenav')]//*[contains(text(), '%s') or self::button[contains(text(), '%s')]]" % (option, option)))).click()
    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.alert_is_present(),'Alert did not pop out')
    time.sleep(0.5)
    obj = driver.switch_to.alert
    obj.send_keys(sample)
    obj.accept()
    if target!=None:
        try:
            wait.until(EC.alert_is_present(), 'Another alert did not pop out')
            time.sleep(0.5)
            obj = driver.switch_to.alert
            alert_text = obj.text
            if "input" in alert_text.lower():  # This is a simple heuristic to check for text input
                time.sleep(5)
                obj.send_keys(target)
            obj.accept()
        except:
            pass
    # buttons['feature_menu']().click()

def multiple_two_click_center(id): # 480,320
    ActionChains(driver).click(canvas).perform() 
    canvas1 = driver.find_element("xpath", f"//*[@id='mycanvas-{id}']")
    ActionChains(driver).click(canvas1).perform()        
    time.sleep(2)


def selectFromToolbar_two_multiple(itemStr, n=None):
    base_xpath =f"//*[@id='{itemStr}']"
    element=f"({base_xpath})[{n}]"
    item = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, element)))                                   
    item.click()
    time.sleep(.5)

def resize_canvas(n):
    script = f'document.getElementById("mycanvas-{n}").width = 680; document.getElementById("mycanvas-{n}").height = 420;'
    driver.execute_script(script)

def call_common_view_target(value):
    for val in range(value):
        buttons['feature_menu']().click()
        time.sleep(10)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//label[@class='label' and contains(text(), 'Set Common Views Target')]"))).click()
        option_xpath = f"//label[@class='label' and contains(text(), 'Set Common Views Target')]/select/option[@value='{val}']"
        dropdown_option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, option_xpath)))
        dropdown_option.click()
        click_Offset(-420, -260)
        snapCompare(f"common_view_target_{val}")
        time.sleep(10)
        buttons['feature_menu']().click()

def common_view_camera(value):
    for val in range(value):
        buttons['feature_menu']().click()
        time.sleep(10)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//label[@class='label' and contains(text(), 'Set Common Views Camera')]"))).click()
        option_xpath = f"//label[@class='label' and contains(text(), 'Set Common Views Camera')]/select/option[@value='{val}']"
        dropdown_option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, option_xpath)))
        dropdown_option.click()
        selectFromToolbar("Fit-id-visualization-toolbar")
        snapCompare(f"common_view_camera_{val}")
        time.sleep(10)
        buttons['feature_menu']().click()
    
def measure_settings(option_text):
    dropdown = driver.find_element(By.XPATH, '//div[contains(@class, "UxtDropdownList-input")]')
    dropdown.click()
    time.sleep(10)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'UxtDropdownList-choices-MeasurementSettings-choices')]")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ".//div[contains(@class, 'UxtListItemText-primary') and text()='%s']" %option_text))).click()
    # option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "UxtListItemText-primary")] and text()= "%s"]'% option_text))).click()
    # option = driver.find_element(By.XPATH, "//div[contains(@class, 'UxtListItemText-primary') and text()='%s']" % option_text)
    # option = driver.find_element("xpath",("//div[contains(text(), '%s')]"% option_text))
    # option.click()
    time.sleep(10)

def open_2D_drawing_with_json1(drawing):
    # Open main menu
    buttons['menu_open_hamburger']().click()
    time.sleep(2)
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
    # Go to customs tab
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="CUSTOM"]'))).click()    
    # Click on the dropdown to reveal options
    dropdown_element = driver.find_element("xpath", "//*[contains(@class,'UxtDropdownList-icon')]//*[name()='svg']")
    dropdown_element.click()
    time.sleep(10)
    # Select the option with the title "JSON File Path"
    json_file_path_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="JSON File Path"]')))
    json_file_path_option.click()
    time.sleep(10)
    # Pass the URL to the input field
    # input_element= driver.find_element("xpath", "//body[1]/div[6]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/input[1]")
    input_element = driver.find_element("xpath", "//div[contains(@class, 'UxtInput-root')]//div[contains(@class, 'UxtInput-innerContainer')]//div[contains(@class, 'sa-modal-label') and text()='JSON_PATH']/preceding-sibling::input[contains(@class, 'UxtInput-input')]")
    #input_element.click
    input_element.clear()
    input_element.send_keys("https://gvc.ingrnet.com/AcceptanceJSONs/AcceptanceJSON1.json")
    # Click on Import JSON
    import_json_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Import JSON")]')))
    import_json_button.click()    
    # Wait for some time for the import to finish
    time.sleep(15)
    item = driver.find_element(By.XPATH, '//*[@title="%s"]' % drawing)
    item.click()
    time.sleep(30)

def open_2D_drawing_with_json2(drawing):
    # Open main menu
    buttons['menu_open_hamburger']().click()
    time.sleep(2)
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
    # Go to customs tab
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="CUSTOM"]'))).click()    
    # Click on the dropdown to reveal options
    dropdown_element = driver.find_element("xpath", "//*[contains(@class,'UxtDropdownList-icon')]//*[name()='svg']")
    dropdown_element.click()
    time.sleep(10)
    # Select the option with the title "JSON File Path"
    json_file_path_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="JSON File Path"]')))
    json_file_path_option.click()
    time.sleep(10)
    # Pass the URL to the input field
    # input_element= driver.find_element("xpath", "//body[1]/div[6]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/input[1]")
    input_element = driver.find_element("xpath", "//div[contains(@class, 'UxtInput-root')]//div[contains(@class, 'UxtInput-innerContainer')]//div[contains(@class, 'sa-modal-label') and text()='JSON_PATH']/preceding-sibling::input[contains(@class, 'UxtInput-input')]")
    #input_element.click
    input_element.clear()
    input_element.send_keys("https://gvc.ingrnet.com/AcceptanceJSONs/AcceptanceJSON2.json")
    # Click on Import JSON
    import_json_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Import JSON")]')))
    import_json_button.click()    
    # Wait for some time for the import to finish
    time.sleep(15)
    item = driver.find_element(By.XPATH, '//*[@title="%s"]' % drawing)
    item.click()
    time.sleep(30)
    
def open_2D_drawing_with_json3(drawing):
    # Open main menu
    buttons['menu_open_hamburger']().click()
    time.sleep(2)
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
    # Go to customs tab
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="CUSTOM"]'))).click()    
    # Click on the dropdown to reveal options
    dropdown_element = driver.find_element("xpath", "//*[contains(@class,'UxtDropdownList-icon')]//*[name()='svg']")
    dropdown_element.click()
    time.sleep(10)
    # Select the option with the title "JSON File Path"
    json_file_path_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="JSON File Path"]')))
    json_file_path_option.click()
    time.sleep(10)
    # Pass the URL to the input field
    # input_element= driver.find_element("xpath", "//body[1]/div[6]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/input[1]")
    input_element = driver.find_element("xpath", "//div[contains(@class, 'UxtInput-root')]//div[contains(@class, 'UxtInput-innerContainer')]//div[contains(@class, 'sa-modal-label') and text()='JSON_PATH']/preceding-sibling::input[contains(@class, 'UxtInput-input')]")
    input_element.clear()
    input_element.send_keys("https://gvc.ingrnet.com/AcceptanceJSONs/AcceptanceJSON3.json")
    # Click on Import JSON
    import_json_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Import JSON")]')))
    import_json_button.click()    
    # Wait for some time for the import to finish
    time.sleep(15)
    item = driver.find_element(By.XPATH, '//*[@title="%s"]' % drawing)
    item.click()
    time.sleep(30)

# def open_2D_drawing_with_Native(drawing):
#     # Open main menu
#     buttons['menu_open_hamburger']().click()
#     time.sleep(1)
#     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
#     # Go to customs tab
#     time.sleep(3)
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="CUSTOM"]'))).click()    
#     # Click on the dropdown to reveal options
#     dropdown_element = driver.find_element("xpath", "//*[contains(@class,'UxtDropdownList-icon')]//*[name()='svg']")
#     dropdown_element.click()
#     time.sleep(5)
#     # Select the option with the title "JSON File Path"
#     json_file_path_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="JSON File Path"]')))
#     json_file_path_option.click()
#     time.sleep(3)
#     # Pass the URL to the input field
#     # input_element= driver.find_element("xpath", "//body[1]/div[6]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/input[1]")
#     input_element = driver.find_element("xpath", "//div[contains(@class, 'UxtInput-root')]//div[contains(@class, 'UxtInput-innerContainer')]//div[contains(@class, 'sa-modal-label') and text()='JSON_PATH']/preceding-sibling::input[contains(@class, 'UxtInput-input')]")
#     input_element.clear()
#     input_element.send_keys("https://gvc.ingrnet.com/AcceptanceJSONs/Native12.json")
#     # Click on Import JSON
#     import_json_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Import JSON")]')))
#     import_json_button.click()    
#     # Wait for some time for the import to finish
#     time.sleep(5)
#     item = driver.find_element(By.XPATH, '//*[@title="%s"]' % drawing)
#     item.click()
#     time.sleep(20)

# def open_2D_drawing_with_DWG1(drawing):
#     # Open main menu
#     buttons['menu_open_hamburger']().click()
#     time.sleep(1)
#     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
#     # Go to customs tab
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="CUSTOM"]'))).click()    
#     # Click on the dropdown to reveal options
#     dropdown_element = driver.find_element("xpath", "//*[contains(@class,'UxtDropdownList-icon')]//*[name()='svg']")
#     dropdown_element.click()
#     time.sleep(5)
#     # Select the option with the title "JSON File Path"
#     json_file_path_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="JSON File Path"]')))
#     json_file_path_option.click()
#     time.sleep(5)
#     # Pass the URL to the input field
#     # input_element= driver.find_element("xpath", "//body[1]/div[6]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/input[1]")
#     input_element = driver.find_element("xpath", "//div[contains(@class, 'UxtInput-root')]//div[contains(@class, 'UxtInput-innerContainer')]//div[contains(@class, 'sa-modal-label') and text()='JSON_PATH']/preceding-sibling::input[contains(@class, 'UxtInput-input')]")
#     input_element.clear()
#     input_element.send_keys("https://gvc.ingrnet.com/AcceptanceJSONs/DWG12.json")
#     # Click on Import JSON
#     import_json_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Import JSON")]')))
#     import_json_button.click()    
#     # Wait for some time for the import to finish
#     time.sleep(5)
#     item = driver.find_element(By.XPATH, '//*[@title="%s"]' % drawing)
#     item.click()
#     time.sleep(20)

# def open_2D_drawing_with_DGN1(drawing):
#     # Open main menu
#     buttons['menu_open_hamburger']().click()
#     time.sleep(1)
#     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
#     # Go to customs tab
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="CUSTOM"]'))).click()    
#     # Click on the dropdown to reveal options
#     dropdown_element = driver.find_element("xpath", "//*[contains(@class,'UxtDropdownList-icon')]//*[name()='svg']")
#     dropdown_element.click()
#     time.sleep(5)
#     # Select the option with the title "JSON File Path"
#     json_file_path_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="JSON File Path"]')))
#     json_file_path_option.click()
#     time.sleep(5)
#     # Pass the URL to the input field
#     # input_element= driver.find_element("xpath", "//body[1]/div[6]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/input[1]")
#     input_element = driver.find_element("xpath", "//div[contains(@class, 'UxtInput-root')]//div[contains(@class, 'UxtInput-innerContainer')]//div[contains(@class, 'sa-modal-label') and text()='JSON_PATH']/preceding-sibling::input[contains(@class, 'UxtInput-input')]")
#     input_element.clear()
#     input_element.send_keys("https://gvc.ingrnet.com/AcceptanceJSONs/DGN12.json")
#     # Click on Import JSON
#     import_json_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Import JSON")]')))
#     import_json_button.click()    
#     # Wait for some time for the import to finish
#     time.sleep(5)
#     item = driver.find_element(By.XPATH, '//*[@title="%s"]' % drawing)
#     item.click()
#     time.sleep(20)      

# def open_2D_drawing_with_Server_Native(drawing):
#     # Open main menu
#     buttons['menu_open_hamburger']().click()
#     time.sleep(2)
#     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
#     # Go to customs tab
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="CUSTOM"]'))).click()    
#     # Click on the dropdown to reveal options
#     dropdown_element = driver.find_element("xpath", "//*[contains(@class,'UxtDropdownList-icon')]//*[name()='svg']")
#     dropdown_element.click()
#     time.sleep(10)
#     # Select the option with the title "JSON File Path"
#     json_file_path_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="JSON File Path"]')))
#     json_file_path_option.click()
#     time.sleep(10)
#     # Pass the URL to the input field
#     # input_element= driver.find_element("xpath", "//body[1]/div[6]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/input[1]")
#     input_element = driver.find_element("xpath", "//div[contains(@class, 'UxtInput-root')]//div[contains(@class, 'UxtInput-innerContainer')]//div[contains(@class, 'sa-modal-label') and text()='JSON_PATH']/preceding-sibling::input[contains(@class, 'UxtInput-input')]")
#     input_element.clear()
#     input_element.send_keys("https://gvc.ingrnet.com/AcceptanceJSONs/NativeS12.json")
#     # Click on Import JSON
#     import_json_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Import JSON")]')))
#     import_json_button.click()    
#     # Wait for some time for the import to finish
#     time.sleep(15)
#     item = driver.find_element(By.XPATH, '//*[@title="%s"]' % drawing)
#     item.click()
#     time.sleep(35)

# def open_2D_drawing_with_Server_DWG1(drawing):
#     # Open main menu
#     buttons['menu_open_hamburger']().click()
#     time.sleep(2)
#     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
#     # Go to customs tab
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="CUSTOM"]'))).click()    
#     # Click on the dropdown to reveal options
#     dropdown_element = driver.find_element("xpath", "//*[contains(@class,'UxtDropdownList-icon')]//*[name()='svg']")
#     dropdown_element.click()
#     time.sleep(10)
#     # Select the option with the title "JSON File Path"
#     json_file_path_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="JSON File Path"]')))
#     json_file_path_option.click()
#     time.sleep(10)
#     # Pass the URL to the input field
#     # input_element= driver.find_element("xpath", "//body[1]/div[6]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/input[1]")
#     input_element = driver.find_element("xpath", "//div[contains(@class, 'UxtInput-root')]//div[contains(@class, 'UxtInput-innerContainer')]//div[contains(@class, 'sa-modal-label') and text()='JSON_PATH']/preceding-sibling::input[contains(@class, 'UxtInput-input')]")
#     input_element.clear()
#     input_element.send_keys("https://gvc.ingrnet.com/AcceptanceJSONs/DWGS12.json")
#     # Click on Import JSON
#     import_json_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Import JSON")]')))
#     import_json_button.click()    
#     # Wait for some time for the import to finish
#     time.sleep(15)
#     item = driver.find_element(By.XPATH, '//*[@title="%s"]' % drawing)
#     item.click()
#     time.sleep(35)

# def open_2D_drawing_with_Server_DGN1(drawing):
#     # Open main menu
#     buttons['menu_open_hamburger']().click()
#     time.sleep(2)
#     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
#     # Go to customs tab
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="CUSTOM"]'))).click()    
#     # Click on the dropdown to reveal options
#     dropdown_element = driver.find_element("xpath", "//*[contains(@class,'UxtDropdownList-icon')]//*[name()='svg']")
#     dropdown_element.click()
#     time.sleep(10)
#     # Select the option with the title "JSON File Path"
#     json_file_path_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="JSON File Path"]')))
#     json_file_path_option.click()
#     time.sleep(10)
#     # Pass the URL to the input field
#     # input_element= driver.find_element("xpath", "//body[1]/div[6]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/input[1]")
#     input_element = driver.find_element("xpath", "//div[contains(@class, 'UxtInput-root')]//div[contains(@class, 'UxtInput-innerContainer')]//div[contains(@class, 'sa-modal-label') and text()='JSON_PATH']/preceding-sibling::input[contains(@class, 'UxtInput-input')]")
#     input_element.clear()
#     input_element.send_keys("https://gvc.ingrnet.com/AcceptanceJSONs/DGNS12.json")
#     # Click on Import JSON
#     import_json_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Import JSON")]')))
#     import_json_button.click()    
#     # Wait for some time for the import to finish
#     time.sleep(15)
#     item = driver.find_element(By.XPATH, '//*[@title="%s"]' % drawing)
#     item.click()
#     time.sleep(35) 

# def retry(retries=3, delay=5):
#     def decorator_retry(func):
#         @functools.wraps(func)
#         def wrapper_retry(*args, **kwargs):
#             for attempt in range(retries):
#                 try:
#                     return func(*args, **kwargs)
#                 except Exception as e:
#                     if attempt < retries - 1:
#                         print(f"Attempt {attempt + 1} failed with error: {e}. Retrying in {delay} seconds...")
#                         time.sleep(delay)
#                     else:
#                         print(f"Attempt {attempt + 1} failed with error: {e}. No more retries left.")
#                         raise
#         return wrapper_retry
#     return decorator_retry

def retry(retries=3, delay=5):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < retries - 1:
                        print(f"Attempt {attempt + 1} failed with error: {e}. Retrying in {delay} seconds...")
                        time.sleep(delay)
                        
                        # Call tearDown or cleanup method in case of failure
                        try:
                            if hasattr(args[0], 'tearDown'):  # Checking if tearDown exists
                                args[0].tearDown()
                            else:
                                FunctionList.reload()  # Assuming a fallback if tearDown is not available
                        except Exception as teardown_error:
                            print(f"Error during tearDown: {teardown_error}")
                    else:
                        print(f"Attempt {attempt + 1} failed with error: {e}. No more retries left.")
                        raise
        return wrapper_retry
    return decorator_retry


def clear_browser_cache():
    driver.delete_all_cookies()  # Delete all cookies
    time.sleep(7)  # Wait 7 seconds to clear cookies

def open_2D_drawing(drawing, json_url):
    # Open main menu
    buttons['menu_open_hamburger']().click()
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "Open-id-main-menu"))).click()
    # Go to customs tab
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@title="CUSTOM"]'))).click()    
    # Click on the dropdown to reveal options
    dropdown_element = driver.find_element("xpath", "//*[contains(@class,'UxtDropdownList-icon')]//*[name()='svg']")
    dropdown_element.click()
    time.sleep(5)
    # Select the option with the title "JSON File Path"
    json_file_path_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="JSON File Path"]')))
    json_file_path_option.click()
    time.sleep(3)
    # Pass the URL to the input field
    input_element = driver.find_element("xpath", "//div[contains(@class, 'UxtInput-root')]//div[contains(@class, 'UxtInput-innerContainer')]//div[contains(@class, 'sa-modal-label') and text()='JSON_PATH']/preceding-sibling::input[contains(@class, 'UxtInput-input')]")
    input_element.clear()
    input_element.send_keys(json_url)
    # Click on Import JSON
    import_json_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(),"Import JSON")]')))
    import_json_button.click()    
    # Wait for some time for the import to finish
    time.sleep(5)
    item = driver.find_element(By.XPATH, '//*[@title="%s"]' % drawing)
    item.click()
    time.sleep(10)

def open_2D_drawing_with_Native(drawing):
   
    open_2D_drawing(drawing, "https://gvc.ingrnet.com/AcceptanceJSONs/Native12.json")

def open_2D_drawing_with_DWG1(drawing):
    
    open_2D_drawing(drawing, "https://gvc.ingrnet.com/AcceptanceJSONs/DWG12.json")

def open_2D_drawing_with_DGN1(drawing):
   
    open_2D_drawing(drawing, "https://gvc.ingrnet.com/AcceptanceJSONs/DGN12.json")

def open_2D_drawing_with_Server_Native(drawing):
    
    open_2D_drawing(drawing, "https://gvc.ingrnet.com/AcceptanceJSONs/NativeS12.json")

def open_2D_drawing_with_Server_DWG1(drawing):
    open_2D_drawing(drawing, "https://gvc.ingrnet.com/AcceptanceJSONs/DWGS12.json")

def open_2D_drawing_with_Server_DGN1(drawing):
    open_2D_drawing(drawing, "https://gvc.ingrnet.com/AcceptanceJSONs/DGNS12.json")



    








    
    



    
