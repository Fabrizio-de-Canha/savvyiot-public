import urequests # type: ignore
import os
import json
import machine # type: ignore

class OTAUpdater:
    """ This class handles OTA updates. It connects to the Wi-Fi, checks for updates, downloads and installs them."""
    def __init__(self, wifi_client, repo_url, filenames):
        self.wifi_client = wifi_client
        self.filename = filenames
        self.repo_url = repo_url
        if "www.github.com" in self.repo_url :
            print(f"Updating {repo_url} to raw.githubusercontent")
            self.repo_url = self.repo_url.replace("www.github","raw.githubusercontent")
        elif "github.com" in self.repo_url:
            print(f"Updating {repo_url} to raw.githubusercontent'")
            self.repo_url = self.repo_url.replace("github","raw.githubusercontent")            
        self.version_url = self.repo_url + '/version.json'
        print(f"version url is: {self.version_url}")
        for i in filenames:
            self.firmware_urls.append(self.repo_url + '/' + i)

        # get the current version (stored in version.json)
        if 'version.json' in os.listdir():    
            with open('version.json') as f:
                self.current_version = int(json.load(f)['version'])
            print(f"Current device firmware version is '{self.current_version}'")

        else:
            self.current_version = 0
            # save the current version
            with open('version.json', 'w') as f:
                json.dump({'version': self.current_version}, f)
        
    def fetch_latest_code(self)->bool:
        """ Fetch the latest code from the repo, returns False if not found."""
        
        # Fetch the latest code from the repo.
        for i in self.firmware_urls:
            response = urequests.get(i)
            res = False
            if response.status_code == 200:
                print(f'Fetched latest firmware code, status: {response.status_code}, -  {response.text}')
        
                # Save the fetched code to memory
                self.latest_codes.append(response.text)
                res = True
            
            elif response.status_code == 404:
                print(f'Firmware not found - {i}.')
                self.latest_codes.append('')
                res = False

        return res

    def update_no_reset(self):
        """ Update the code without resetting the device."""

        # Save the fetched code and update the version file to latest version.
        count = 0
        for i in self.filenames:
            with open(f'latest_code_{i}', 'w') as f:
                if self.latest_codes[count] != '':
                    f.write(self.latest_codes[count])

            count += 1
        
        # update the version in memory
        self.current_version = self.latest_version

        # save the current version
        with open('version.json', 'w') as f:
            json.dump({'version': self.current_version}, f)
        
        # free up some memory
        self.latest_codes = None

        # Overwrite the old code.
#         os.rename('latest_code.py', self.filename)

    def update_and_reset(self):
        """ Update the code and reset the device."""

        print(f"Updating device... (Renaming latest_code.py to {self.filename})", end="")

        # Overwrite the old code.
        count = 0
        for i in self.filenames:
            if self.latest_codes[count] != '':
                os.rename(f'latest_code_{i}.py', i)  
            count += 1

        # Restart the device to run the new code.
        print('Restarting device...')
        machine.reset()  # Reset the device to run the new code.
        
    def check_for_updates(self):
        """ Check if updates are available."""

        print(f'Checking for latest version... on {self.version_url}')
        response = urequests.get(self.version_url)
        
        data = json.loads(response.text)
        
        print(f"data is: {data}, url is: {self.version_url}")
        print(f"data version is: {data['version']}")
        # Turn list to dict using dictionary comprehension
#         my_dict = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
        
        self.latest_version = int(data['version'])
        print(f'latest version is: {self.latest_version}')
        
        # compare versions
        newer_version_available = True if self.current_version < self.latest_version else False
        
        print(f'Newer version available: {newer_version_available}')    
        return newer_version_available
    
    def download_and_install_update_if_available(self):
        """ Check for updates, download and install them."""
        if self.check_for_updates():
            if self.fetch_latest_code():
                self.update_no_reset() 
                self.update_and_reset() 
        else:
            print('No new updates available.')