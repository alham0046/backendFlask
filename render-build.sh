#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/.render

# Install Chrome
if [[ ! -d $STORAGE_DIR/chrome ]]; then
  mkdir -p $STORAGE_DIR/chrome
  echo "...Directory made"
  cd $STORAGE_DIR/chrome
  echo "...Downloading Chrome"
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
#   cd $HOME/project # Go back to the project root directory
else
  echo "...Using Chrome from cache"
fi

# Install ChromeDriver
if [[ ! -d $STORAGE_DIR/chromedriver ]]; then
  mkdir -p $STORAGE_DIR/chromedriver
  echo "...Made driver directory"
#   CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
  wget -P $STORAGE_DIR/chromedriver https://storage.googleapis.com/chrome-for-testing-public/149.0.7827.22/linux64/chromedriver-linux64.zip
  echo "...Downloaded ChromeDriver"
  unzip -o $STORAGE_DIR/chromedriver/chromedriver-linux64.zip -d $STORAGE_DIR/chromedriver
  mv $STORAGE_DIR/chromedriver/chromedriver-linux64/chromedriver $STORAGE_DIR/chromedriver/chromedriver
  rm -rf $STORAGE_DIR/chromedriver/chromedriver-linux64
  rm $STORAGE_DIR/chromedriver/chromedriver-linux64.zip
else
  echo "...Using ChromeDriver from cache"
fi

chmod +x /opt/render/project/.render/chromedriver/chromedriver
chmod +x /opt/render/project/.render/chrome/opt/google/chrome/chrome


# Add Chrome and ChromeDriver to the PATH
export PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome"
export PATH="${PATH}:/opt/render/project/.render/chromedriver"

# Set the path to the Chrome binary in Selenium
export CHROME_BIN="/opt/render/project/.render/chrome/opt/google/chrome/chrome"
export CHROMEDRIVER_PATH="/opt/render/project/.render/chromedriver/chromedriver"