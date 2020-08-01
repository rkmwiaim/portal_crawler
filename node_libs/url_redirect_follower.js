const puppeteer = require('puppeteer');

async function follow(url) {
  const browser = await puppeteer.launch({
    headless : true
  });
  try {
    const [page] = await browser.pages();
    await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36');

    await page.goto(url, {waitUntil: 'networkidle2'});

    return Promise.resolve(page.url());
  } finally {
    await browser.close();
  }
}

async function followUrls(urls) {
  const browser = await puppeteer.launch({headless : true});

  let locations = {};
  try {
    await Promise.all(urls.map(async url => {
      console.log(`start ${url}`);
      const page = await browser.newPage();
      await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36');
      await page.goto(url, {waitUntil: 'networkidle2'});
      let location = await page.url();
      console.log(`end ${url}`);
      locations[url] = location;
    }));

    return locations;
  } finally {
    await browser.close();
  }
}

exports.follow = follow;
exports.followUrls = followUrls;


if (require.main === module) {
  (async() => {
    let followResult = await follow(process.argv[2]);
    console.log(followResult);
  })();
}