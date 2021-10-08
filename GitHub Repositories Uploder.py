import time
import os
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Initializing options for selenium web driver
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])

# Give path to you chromedriver.exe here or Just put chromedriver.exe in same folder as your script.
driver = webdriver.Chrome(executable_path=os.path.join(sys.path[0], 'chromedriver.exe'), options=option)


def login(user_name, password):
    """ This function takes user name and password to login into Github account.
        Args:
            :param user_name: Github username
            :param password: Github password
        Returns:
            error_dict (dict): If it's logged in successfully or not with the error message.
    """
    driver.get('https://github.com/login')    # github login page
    username = driver.find_element_by_xpath('//*[@id="login_field"]')   # Input Username
    username.send_keys(user_name)
    time.sleep(2)
    pass_word = driver.find_element_by_xpath('//*[@id="password"]')  # Input Password
    pass_word.send_keys(password)
    sign_in = driver.find_element_by_xpath('//*[@id="login"]/div[4]/form/div/input[12]')    # Click on sig in button
    sign_in.click()
    input("Please enter your verification code then hit enter, if it's logged in without it just hit enter ...")
    error_dict = {'error': None, 'message': None}    # Check if it's logged in successfully

    try:
        error = driver.find_element_by_xpath('//*[@id="js-flash-container"]/div/div').text  # Check for login error
        error_dict['error'] = True
        error_dict['message'] = error

    except NoSuchElementException:
        error_dict['error'] = False
        error_dict['message'] = None

    return error_dict


def github_repo(repository_name, upload_folder_path, descriptions=False,
                private=False, readme=False):
    """ This function creates new repository name, upload folders in path and
        adds description, private and readme options if you want.
        Args:
            :param repository_name: repository name matches the folder name.
            :param upload_folder_path: folder path for repositories uploading.
            :param descriptions: add description.
            :param private: make it private or public.
            :param readme:  edit readme.
    """
    # Create new repository name.
    driver.implicitly_wait(10)
    new_repo = driver.find_elements_by_xpath('//*[@href="/new"]')
    new_repo[1].click()
    time.sleep(5)

    # Enter repository name
    repo_name = driver.find_element_by_xpath('//*[@id="repository_name"]')
    repo_name.send_keys(repository_name)
    time.sleep(5)

    # Optional
    time.sleep(5)
    # Enter Description
    if descriptions:
        description = driver.find_element_by_xpath(
            '//*[@id="repository_description"]')
        description.send_keys(descriptions)

    # Private Mode
    if private:
        private = driver.find_element_by_xpath(
            '//*[@id="repository_visibility_private"]')
        private.click()

    # Create ReadMe File
    if readme:
        readme = driver.find_element_by_xpath(
            '//*[@id="repository_auto_init"]')
        readme.click()

    time.sleep(2)

    # Create new repository here using above details
    create = driver.find_element_by_xpath('//*[@id="new_repository"]/div[4]/button')
    create.click()

    """
     The remote repository has been created, to upload content from our local folder to remote repository
     using OS module, we are executing git commands to initialize local repository, add content,
     do commit and finally push the content to remote repository
    """
    print(os.chdir(upload_folder_path + "\\" + repository_name))
    print(os.system('echo "# This repository is Uploaded with GITHUB Bot created by Omar AEH " >> README.md'))
    print(os.system('git init'))
    print(os.system('git add .'))
    print(os.system('git commit -m \"first commit\"'))
    print(os.system('git branch -M main'))

    # Convert general repository name into repository specific format ('-' instead of spaces)
    # replace YOUR-USER-NAME
    print(os.system(
        f'git remote add origin https://github.com/YOUR-USER-NAME/' + generate_repo_name(repository_name) + '.git'))
    print(os.system('git push -u origin main'))
    print(repository_name + " uploaded successfully.")
    driver.get("https://github.com/")   # Back to homepage to create next repository
    time.sleep(3)


def generate_repo_name(repo_name):
    """ This function for converting general string to github_repo_format_string.
        Args:
            :param repo_name: repository name.
        Returns:
            repo_name (str): Return a string as github repository correct format.
    """
    return repo_name.replace(" ", "-")    # Replace all spaces in name with '-'


def main(folder_path, username, password):
    """ This function to get all project directory names from the given path folder
        and handle the login to get hub account.
        Args:
            :param folder_path: Folder path to the projects.
            :param username: Github account username.
            :param password: Github account password.
    """
    os.chdir(folder_path)
    dirs = os.listdir()
    # Login then check if it's logged in successfully
    error_dict = login(username, password)
    if error_dict.get('error'):
        print(error_dict.get('message'))
        return
    # Loop through all directories one by one by creating their remote repositories
    for dir_name in dirs:
        github_repo(dir_name, folder_path)


if __name__ == '__main__':
    uploading_folder_path = (r'C:\replace\me')    # Directory path which you want to upload projects on Github
    github_username = 'replace this with your username'
    github_password = 'replace this with your password'
    main(uploading_folder_path, github_username, github_password)
