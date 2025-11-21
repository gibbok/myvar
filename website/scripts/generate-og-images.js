const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function generateOGImages() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.setViewport({ width: 1200, height: 630 });
  
  const contentDir = path.join(__dirname, '../content');
  const publicDir = path.join(__dirname, '../static/images');
  
  if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
  }
  
  const template = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {
          margin: 0;
          padding: 60px;
          width: 1200px;
          height: 630px;
          background: white;
          font-family: Arial, sans-serif;
          display: flex;
          align-items: center;
          justify-content: center;
          box-sizing: border-box;
        }
        .title {
          color: black;
          font-size: 64px;
          font-weight: bold;
          text-align: center;
          line-height: 1.2;
          word-wrap: break-word;
        }
      </style>
    </head>
    <body>
      <div class="title">{{TITLE}}</div>
    </body>
    </html>
  `;
  
  const defaultHTML = template.replace('{{TITLE}}', 'MyVar.dev');
  await page.setContent(defaultHTML);
  await page.screenshot({ path: path.join(publicDir, 'og-default.png') });
  
  const findMarkdownFiles = (dir) => {
    let files = [];
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
      const fullPath = path.join(dir, item);
      if (fs.statSync(fullPath).isDirectory()) {
        files = files.concat(findMarkdownFiles(fullPath));
      } else if (item.endsWith('.md') && item !== '_index.md') {
        files.push(fullPath);
      }
    }
    return files;
  };
  
  const markdownFiles = findMarkdownFiles(contentDir);
  
  for (const file of markdownFiles) {
    const content = fs.readFileSync(file, 'utf8');
    const titleMatch = content.match(/^title:\s*["'](.+)["']/m);
    
    if (titleMatch) {
      const title = titleMatch[1];
      const relativePath = path.relative(contentDir, file);
      const imageName = relativePath.replace(/\.md$/, '').replace(/\//g, '-') + '.png';
      
      const html = template.replace('{{TITLE}}', title);
      await page.setContent(html);
      await page.screenshot({ path: path.join(publicDir, imageName) });
      
      console.log(`Generated: ${imageName}`);
    }
  }
  
  await browser.close();
}

generateOGImages().catch(console.error);