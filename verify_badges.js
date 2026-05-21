const { chromium } = require('playwright');
(async() => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 2000 } });
  await page.goto('https://emilydomm.github.io/sentiment-dashboard/', { waitUntil: 'networkidle', timeout: 40000 });
  await page.click('.tab-btn[data-tab="wechat"]');
  await page.waitForTimeout(1500);
  await page.evaluate(() => selectWechatDate('2026-05-04'));
  await page.waitForTimeout(2000);
  const state = await page.evaluate(() => ({
    label: document.getElementById('wechatDateLabel')?.innerText || '',
    total: document.getElementById('wechatTotalCount')?.innerText || '',
    brands: document.getElementById('wechatBrandCountInline')?.innerText || '',
    nav: [...document.querySelectorAll('#wechatBrandNav a')].map(a => a.innerText.trim()),
    cardText: (document.getElementById('wechatCardContainer')?.innerText || '').slice(0, 300),
    dataTarget: typeof wechatData !== 'undefined' && wechatData ? wechatData.target_date : null,
    dataPeriod: typeof wechatData !== 'undefined' && wechatData ? wechatData.display_period : null,
    dataBrandLen: typeof wechatData !== 'undefined' && wechatData && Array.isArray(wechatData.brands) ? wechatData.brands.length : null,
    availableDates: typeof wechatAvailableDates !== 'undefined' ? wechatAvailableDates : null,
    currentDate: typeof currentWechatDate !== 'undefined' ? currentWechatDate : null
  }));
  console.log(JSON.stringify(state, null, 2));
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
